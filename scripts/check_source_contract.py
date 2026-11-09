#!/usr/bin/env python3
"""Check a small, source-bound semantic assessment, never legacy policy wording."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "evals/core-protections/spec.json"

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def object_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON key")
        out[key] = value
    return out

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=object_pairs)

def safe_file(root, relative):
    rel = PurePosixPath(relative)
    if (not isinstance(relative, str) or not relative or "\\" in relative or
            ":" in relative or rel.is_absolute() or ".." in rel.parts or
            rel.as_posix() != relative):
        raise ValueError("unsafe relative input")
    path = root.joinpath(*rel.parts)
    for part in [path, *path.parents]:
        if part.is_symlink() or bool(getattr(part.lstat(), "st_file_attributes", 0) & 1024):
            raise ValueError("link-like input")
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError("input outside root or missing")
    return path

def section(root, location):
    text = safe_file(root, location["path"]).read_text(encoding="utf-8")
    heading = location["heading"]
    matches = list(re.finditer(r"(?m)^(#{1,6}) (.+)\r?$", text))
    hits = [m for m in matches if m.group(2).strip() == heading]
    if len(hits) != 1:
        raise ValueError("clause location missing or ambiguous: " + heading)
    hit = hits[0]
    end = next((m.start() for m in matches if m.start() > hit.start()
                and len(m.group(1)) <= len(hit.group(1))), len(text))
    return " ".join(text[hit.start():end].split())

def expected_cases(spec, component):
    rules = spec.get("rules")
    ids = {f"CP{i:02d}" for i in range(1, 18)}
    if not isinstance(rules, list) or len(rules) != 17:
        raise ValueError("exactly 17 core rules required")
    if {r.get("id") for r in rules} != ids:
        raise ValueError("core rule IDs missing or duplicated")
    all_cases = set()
    for rule in rules:
        cases = rule.get("cases")
        required = {rule["id"] + "-P", rule["id"] + "-N"}
        if (not isinstance(cases, list) or len(cases) != 2 or
                {c.get("id") for c in cases} != required):
            raise ValueError("each core rule requires its unique P/N pair")
        for case in cases:
            if case["id"] in all_cases:
                raise ValueError("duplicate global scenario ID")
            all_cases.add(case["id"])
            if not all(isinstance(case.get(k), str) and case[k].strip()
                       for k in ["prompt", "expected"]):
                raise ValueError("scenario requires a prompt and expected action")
        required_components = {"host", "docs"} if rule["id"] == "CP16" else {"host", "charter"}
        locations = rule.get("locations")
        if not isinstance(locations, dict) or set(locations) != required_components:
            raise ValueError("required component coverage missing")
        if any(not isinstance(v, list) or not v for v in locations.values()):
            raise ValueError("core rule has no clause location")
    selected = [r for r in rules if component in r["locations"]]
    if not selected:
        raise ValueError("unknown or empty component")
    return selected, {case["id"]: (rule, case) for rule in selected for case in rule["cases"]}


def assess(spec, component, root, witness):
    rules, expected = expected_cases(spec, component)
    failures, pending = [], []
    if witness.get("schema") != "core-semantic-assessment/v1" or witness.get("component") != component:
        return {"result": "FAIL", "failures": ["assessment schema/component"], "pending": []}
    if witness.get("spec_sha256") != digest(SPEC.read_bytes()):
        pending.append("scenario specification changed; reassess affected scenarios")
    answers = witness.get("answers")
    if not isinstance(answers, list):
        return {"result": "FAIL", "failures": ["answers must be a list"], "pending": []}
    got = {}
    for answer in answers:
        if not isinstance(answer, dict) or answer.get("case_id") in got:
            failures.append("invalid or duplicate answer")
            continue
        got[answer.get("case_id")] = answer
    if set(got) != set(expected):
        failures.append("scenario coverage mismatch")
    checks = []
    for case_id, (rule, case) in expected.items():
        answer = got.get(case_id)
        locations = rule["locations"][component]
        bound = []
        for location in locations:
            content = section(root, location)
            bound.append({"path": location["path"], "heading": location["heading"],
                          "sha256": digest(content.encode("utf-8"))})
        if not answer:
            continue
        if answer.get("clause_bindings") != bound:
            pending.append(case_id + ": clause input changed; semantic reassessment required")
        decision_ok = answer.get("decision") == case["expected"]
        if not decision_ok:
            failures.append(case_id + ": action contradicts the core scenario")
        evidence = answer.get("evidence")
        evidence_ok = False
        if isinstance(evidence, dict) and isinstance(evidence.get("quote"), str):
            for location in locations:
                if evidence.get("path") == location["path"] and evidence.get("heading") == location["heading"]:
                    quote = " ".join(evidence["quote"].split())
                    evidence_ok = bool(quote) and quote in section(root, location)
                    if evidence_ok:
                        break
        if not evidence_ok:
            failures.append(case_id + ": missing source-grounded assessment evidence")
        checks.append({"rule": rule["id"], "case": case_id, "locations": locations,
                       "decision_matches": decision_ok, "evidence_locates": evidence_ok})
    return {"result": "FAIL" if failures else ("REASSESS" if pending else "PASS"),
            "assertions": len(rules), "scenarios": len(expected),
            "checks": checks, "failures": failures, "pending": pending,
            "scope": "Source-bound semantic assessment; no deployment or runtime-effect proof"}

def package_identity():
    # Reuse the already maintained package/path validator; no installation calls.
    spec = importlib.util.spec_from_file_location("core_install_identity", ROOT / "scripts/manage_install.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    pointer = load_json(ROOT / "release/current.json")
    metadata = module.candidate_metadata(ROOT, pointer["version"])
    module.package_files(ROOT, metadata, metadata["package"]["tree"])
    if pointer["candidate"] != "release/v" + pointer["version"] + "-candidate.json":
        raise ValueError("candidate pointer mismatch")
    historical = load_json(ROOT / "release/historical-files.json")
    for relative, expected in historical["files"].items():
        if digest(safe_file(ROOT, relative).read_bytes()) != expected:
            raise ValueError("historical release changed: " + relative)
    return {"version": pointer["version"], "file_count": metadata["package"]["file_count"],
            "tree": metadata["package"]["tree"], "historical_files_checked": len(historical["files"])}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--component", choices=["charter", "host", "docs"], default="charter")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--witness", type=Path)
    parser.add_argument("--prepare", action="store_true", help="Print scenario inputs without expected answers")
    args = parser.parse_args()
    root = args.root or ROOT
    if args.component != "charter" and args.root is None:
        parser.error("--root is required for an explicitly selected external component")
    spec = load_json(SPEC)
    rules, cases = expected_cases(spec, args.component)
    if args.prepare:
        prepared = []
        for case_id, (rule, case) in cases.items():
            prepared.append({"case_id": case_id, "prompt": case["prompt"],
                             "locations": rule["locations"][args.component]})
        print(json.dumps({"component": args.component, "cases": prepared}, ensure_ascii=False, indent=2))
        return 0
    witness_path = args.witness or ROOT / "evals/core-protections/witness-charter.json"
    if not witness_path.exists():
        result = {"result": "REASSESS", "failures": [], "pending": ["independent semantic assessment missing"]}
    else:
        try:
            result = assess(spec, args.component, root, load_json(witness_path))
            if args.component == "charter":
                result["package_identity"] = package_identity()
        except (OSError, ValueError, KeyError, TypeError) as error:
            result = {"result": "FAIL", "failures": [str(error)], "pending": []}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else
          f"core protections: {result['result']}")
    return {"PASS": 0, "FAIL": 1, "REASSESS": 2}[result["result"]]

if __name__ == "__main__":
    sys.exit(main())
