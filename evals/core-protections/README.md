# Core safeguard source assessment

Seventeen logical safeguards have positive and negative scenarios in spec.json.
The checker uses only those rules, not the restriction-classification table.

Run check_source_contract.py --prepare to obtain prompts without expected actions.
An independent reader uses the named clauses and returns action decisions plus
short verbatim evidence. The maintained witness records those observations and
normalized clause hashes. The checker verifies coverage, action semantics,
grounded evidence, clause identity and package identity.

A missing or changed semantic input returns REASSESS (exit 2), not a claim that a
wording change violated policy. Re-evaluate the affected core scenarios; whitespace
changes normalize away. A contradictory action or bad evidence returns FAIL.
A bound assessment and valid package return PASS. No phrase list is matched.

The host and Project Docs components run only when their root and witness are
explicitly supplied. Standalone Charter checks do not require either installation.
These are static semantic scenarios, not production-effect or general efficacy tests.
