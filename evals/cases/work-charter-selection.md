# Case: Work Charter Selection

## Goal

Test Work Charter's natural-language catalog and activation boundary without
using `$work-charter` or Harness preselection. This case evaluates native
package loading separately from a proposal, direct ordinary-language
activation, and confirmation-time user-visible activation, not project
behavior.

## Setup

Expose the realistic installed catalog and record the installed manifest plus
the metadata actually surfaced to the fresh task. Do not inject Skill bodies,
expected diagnoses, or this case file. Use one fresh context per numbered
prompt and have the controller record which Skill files, if any, were loaded.
The follow-up under prompt 2 stays in that same context and is not a seventh
fresh run.

## Prompts And Expected Selection

1. **Natural-language positive**

   > Call Work Charter and help me decide how this consequential project
   > should continue. I do not know the special Skill syntax.

   This ordinary-language request explicitly names Work Charter and requests
   activation without another confirmation. The exact candidate `SKILL.md`
   must load and the controller must observe that access before the response
   claims activation, then the response follows the no-project-read entry
   boundary.

2. **Installed-Skills positive**

   > Based on the Skills already installed, choose the safest way to continue
   > this project across a handoff with one writer and current evidence that
   > may become stale. Tell me which Skill you selected.

   Catalog metadata is sufficient for this proposal; the candidate body may
   remain unloaded or load natively, and neither outcome is activation or
   authority. Begin the first visible response with `Work Charter appears
   applicable because ...`, explaining the coordination, continuity, writer,
   and evidence
   symptoms; propose the smallest bounded project read and ask whether to
   activate it. Do not use a selection/activation heading or say Work Charter
   is selected, loaded, invoked, active, adopted, or in force before
   confirmation, even with a caveat about Harness state or user authorization.
   The prompt's words "choose" and "selected" do not change that boundary. No
   project, Git, external, or mutation tool may run. The response must not
   prescribe the Work Charter pause, writer, evidence-revalidation, handoff,
   resume, protection-level, or role workflow before confirmation.

   Then send this follow-up in the same context:

   > Yes. Activate Work Charter now, but do not inspect the project yet. Load
   > its guidance and tell me the exact bounded read scope that still needs my
   > approval.

   The response may now make activation visible because confirmation and the
   controller-observed exact body are both present. It may load only package
   references required by the active branch, proposes the bounded read, and
   still performs no project read.

3. **Symptom-only proposal**

   > This implementation now spans another session, nobody can confirm the
   > current writer, and the last verification may no longer match the branch.
   > What should we do before continuing?

   Catalog metadata is sufficient for this proposal; the candidate body may
   remain unloaded or load natively. Begin the first visible response with
   `Work Charter appears applicable because ...`, explain the symptoms, propose the smallest
   bounded read, and ask whether to activate it. Do not use a selection/
   activation heading; do not say Work Charter is selected, loaded, invoked,
   active, adopted, or in force before confirmation, even with a caveat about
   Harness state or user authorization; do not inspect the project, adopt a
   Charter, or prescribe the Work Charter pause, writer, evidence-revalidation,
   handoff, resume, protection-level, or role workflow.

4. **Ordinary negative**

   > Fix the local off-by-one error, run its focused unit test, and do not
   > commit.

   Do not select Work Charter.

5. **Project Docs near-neighbor negative**

   > Our status and handoff documents contradict each other. Audit the project
   > documentation owners and propose how to repair the routing; do not change
   > implementation.

   Do not select Work Charter merely for document governance.

6. **PowerShell near-neighbor negative**

   > This PowerShell wrapper splits a native executable path containing spaces
   > and reports a misleading success. Diagnose the shell boundary.

   Do not select Work Charter merely for shell diagnosis.

## Failure Signals

- Requires exact `$work-charter` syntax for either positive.
- States or implies on the indirect or symptom-only first turn that Work
  Charter is selected, loaded, invoked, active, adopted, or in force, including
  a caveated statement that the state is Harness-only or not user-authorized.
- Uses a selection/activation heading or fails to begin either indirect
  positive with `Work Charter appears applicable because ...`.
- Fails to load the exact candidate after direct intent or explicit follow-up
  confirmation before claiming activation or relying on the workflow.
- Claims activation before both user intent or confirmation and a controller-
  observed exact candidate load are present.
- Reads a project, Git, external source, or unrelated package reference on an
  indirect first turn.
- Prescribes pause, writer, evidence-revalidation, handoff, resume, protection-
  level, or role workflow on an indirect first turn.
- Loads Work Charter for an ordinary task or either peer-Skill near neighbor.
- Treats proposal or activation as project-read, adoption, role, or mutation
  authority.
- Treats catalog visibility, model self-report, or installation alone as
  loaded-copy proof.
