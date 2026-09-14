# Agent Instructions

## Read for the current decision

Use the relevant owner before the action it governs; reuse unchanged guidance
already loaded. Do not read this entire list before every edit.

- `README.md`: product scope, package entry and human navigation.
- `docs/skills/work-charter/STATE.md`: continuation, current candidate,
  writer/delivery boundaries and outstanding decisions.
- `docs/skills/work-charter/DESIGN.md`: changes to selection, workflow,
  contracts or architecture.
- `PROVENANCE.md` and the current source map: package identity, source lineage,
  mapped-file changes or publication claims.
- `docs/skills/work-charter/VERIFICATION.md`: checks affected by the change
  and the scope of existing evidence.

## Scope and ownership

- Treat `skills/work-charter/` as the only editable installable Skill source.
- Keep this repository independently useful, installable, invokable, and evaluable.
- Do not add an implicit dependency on another Skill repository.
- Keep one repository writer and preserve unrelated dirty work.
- A commit does not authorize a remote, push, tag, release, installation, or publication.

## Verification

- Run `python -B scripts/check_repository.py --json` against the final candidate
  when mapped files, package identity or provenance change. This binds current
  bytes, file inventory and declared origin; intermediate edits need no repeat.
- Select affected SOURCE, metadata or focused checks from
  `docs/skills/work-charter/VERIFICATION.md`. Complete authorized local
  checks and same-scope repairs without step-by-step approval.
- Rerun only for changed inputs, failures, required gates or unresolved material
  risk. Text-only changes do not by themselves require full installer lifecycle,
  repository adversarial or model-evaluation runs. Changes to the mechanisms
  those checks protect still require their relevant coverage.
- Keep package behavior and provenance claims evidence-bound.
- Keep private paths, task or host identifiers, prompts, memories, and session data out of tracked files.
