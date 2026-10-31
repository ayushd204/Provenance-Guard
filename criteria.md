# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Limit false positives on my own writing

<!-- Your criterion. It must name a number. -->

Across three evaluation trials, no more than 1 of 10 distinct pieces of my own
writing may receive the **high-confidence AI** label in any trial.

Why this target:

A wrong accusation can harm a real writer, so I want a low false-positive rate
even if that means some AI writing lands in the unsure band. Repeating the same
ten pieces checks that small score variations do not keep flipping human work
into an accusation.


## 2. Keep all three labels reachable

<!-- Your criterion. -->

In each of three evaluation trials, a fixed calibration set containing at
least one clearly human, one borderline, and one clearly AI text must produce
at least one **high-confidence human**, one **unsure**, and one
**high-confidence AI** result.

Why this target:

The unsure label gives the system a way to express doubt without making an
accusation. Requiring all three outcomes to be reachable checks that the
thresholds and scores are not effectively collapsing into one label.

## 3. Record valid appeals and reject unknown submissions

<!-- Your criterion. -->

For every valid appeal to an existing `content_id`, `POST /appeal` returns
HTTP 200 and the audit log contains a later entry for that same ID with
`event: "appeal"` and `status: "under_review"`. An appeal for an unknown ID
returns HTTP 404 and adds no appeal event.

Why this target:

A writer needs a dependable way to challenge a decision. Checking both the
response and the append-only log makes the outcome visible and traceable

## 4. Return clear errors for invalid or oversized text

<!-- Your criterion. -->

Requests with a missing, null, non-string, or empty `text` field return HTTP
400 with a JSON `error` field and do not return HTTP 500. A request with more
than 100,000 characters returns HTTP 413, also with a JSON `error` field.

Why this target:

Malformed requests should get a clear client error rather than a server crash,
and a fixed size limit prevents an unexpectedly large submission from
consuming unbounded time or memory. The status and response field make each
case straightforward to check.

## 5. Separate clearly human and AI text scores

<!-- Your criterion. -->

For a fixed set of five clearly human texts and five clearly AI-generated
texts, the mean combined score for the AI set is at least **0.20 higher** than
the mean combined score for the human set in each of three trials.

Why this target:

The system should show measurable separation on examples whose origins are
known, while the 0.20 margin avoids treating a tiny average difference as
useful. This is a calibration check, not proof that any individual score
establishes authorship.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
