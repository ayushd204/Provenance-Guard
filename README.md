# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. The caller sends text as JSON to `POST /submit`, along with a
   `creator_id` so the submission can be associated with its writer.
2. Flask receives the request in `app.py`, checks that `text` and `creator_id`
   are non-empty strings, and rejects text that is too short.
3. The model signal in `detector.py` tokenizes the text and asks the local
   GPT-2 model how predictable it is. It adds a `model_score` from 0 to 1;
   higher means more AI-like according to this model.
4. The style signal in `stylometry.py` measures sentence-length variation,
   vocabulary repetition, and punctuation patterns. It adds a `style_score`
   from 0 to 1, also intended to run higher for more AI-like style.
5. `scoring.py` averages the two signal scores with equal weights and rounds
   the result to two decimal places. It maps the combined score to a guess and
   reader-facing label. The response's confidence is the distance from 0.50,
   scaled from 0 to 1.
6. The label step maps the combined score to one of three reader-facing
   outcomes: high-confidence human, unsure, or high-confidence AI.
7. The service records and returns the decision. `audit.py` appends the
   scores and label to the audit log; Flask returns a JSON response containing
   the result for the caller to show the writer.

The appeal route accepts the returned `content_id`, records the writer's
reasoning beside the original decision, and marks the appeal `under_review`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
It measures how predictable the text is to the local GPT-2 language model.
The detector maps predictability to a `model_score` from 0 to 1; higher scores
mean the text is more predictable to that model and are treated as more
AI-like.

**Why that might differ between human and AI writing:**
AI-generated text often follows common, likely word sequences, which can make
it more predictable to a language model. People also write predictable text,
so this is only a tendency.

**What it can't see:**

It cannot tell who wrote the text or why it was written. It measures how
surprising the words are to GPT-2, not authorship. Plain, conventional human
writing can be predictable and receive an AI-like score; unusual or ornate AI
writing can surprise the model and receive a more human-like score. The result
also depends on the model, topic, and text length.

### Signal two — the style signal

**What it measures:**

The `stylometry.py` signal measures the coefficient of variation in sentence
length, the unique-word-to-total-word ratio, and the fraction of non-whitespace
characters that are punctuation. It treats even sentence lengths, repeated
vocabulary, and sparse punctuation as AI-like tendencies, combines those three
scaled measures equally, and returns a 0–1 `style_score`.

**Why that might differ between human and AI writing:**

Generated prose can settle into similar sentence lengths and reuse words.
Human writing can vary more, with a short sentence beside a long one and a
broader vocabulary. These are tendencies, not reliable rules about authorship.

**What it can't see:**

It cannot understand the meaning, truth, context, or authorship of the text.
It only sees measurable form. Editing sentence breaks, adding typos, changing
punctuation, or including a quotation can shift those measurements without
changing who wrote the underlying ideas. Short texts and changes in length can
also distort measures such as type-token ratio.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** I average the model and style scores using equal weights. When
they disagree, the combined score lands between them; a strong disagreement
therefore pulls the result toward the unsure range instead of letting either
signal decide on its own.

**The numbers:** `model_score` weight = 0.50, `style_score` weight = 0.50.
The combined score is rounded to two decimal places. The label cutoffs are
`HUMAN_THRESHOLD = 0.49` and `AI_THRESHOLD = 0.66`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** If the
model score is 0.90 and the style score is 0.10, the weighted average is 0.50.
That is between 0.50 and 0.65, so the result is unsure.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label                 | Score range | The exact text a reader sees                                 |
| --------------------- | ----------- | ------------------------------------------------------------ |
| high-confidence human | 0.00–0.49   | We think this was written by a person.                       |
| unsure                | 0.50–0.65   | We can't tell whether this was written by a person or an AI. |
| high-confidence AI    | 0.66–1.00   | We think this was written by an AI.                          |

**Why I worded the "unsure" one this way:**

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It states the uncertainty plainly and does not accuse the writer of using AI.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text":"In todays rapidly evolving digital landscape, it is crucial to leverage innovative, cutting-edge solutions to unlock new opportunities, foster meaningful connections, and drive impactful outcomes. By harnessing the power of technology, we can navigate thecomplexities of an ever changing world and pave the way toward a brighter, more sustainable future.","creator_id":"74883647243"}'

RESPONSE:

{
"combined_score": 0.69,
"confidence": 0.38,
"content_id": "e1334cc5-d183-4e7e-8d85-a662614281c1",
"guess": "ai",
"label": "We think this was written by an AI.",
"model_score": 0.7514,
"style_score": 0.6345
}

```

**An appeal**

curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"reasoning":"I wrote this content by myself","content_id":"80edce45-fb3a-4050-86a9-63694a92770d"}'

RESPONSE:

{
  "content_id": "80edce45-fb3a-4050-86a9-63694a92770d",
  "ok": true,
  "status": "under_review"
}



**What the log shows afterwards**

{"timestamp": "2026-11-01T17:40:42+00:00", "content_id": "e1334cc5-d183-4e7e-8d85-a662614281c1", "creator_id": "74883647243", "guess": "ai", "model_score": 0.7514, "style_score": 0.6345, "combined_score": 0.69, "label": "We think this was written by an AI.", "status": "decided"}
{"timestamp": "2026-11-01T17:51:39+00:00", "content_id": "80edce45-fb3a-4050-86a9-63694a92770d", "creator_id": "4545", "event": "appeal", "status": "under_review", "reasoning": "I wrote this content by myself"}

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked AI to format the README for better
  readability.
- *What came back:* It organized the material with clearer headings, tables,
  and code examples.
- *What I changed:* I reviewed the wording and kept the formatting that made
  the signal descriptions, score ranges, and sample requests easier to scan.

**Moment 2**

- *What I asked for:* I asked AI to help with the `scoring.py` script,
  especially combining the two scores and mapping the result to a label.
- *What came back:* It helped implement a weighted average using the weights
  in `config.py` and label selection using the configured cutoffs.
- *What I changed:* I set the weights to 0.50 each, chose the 0.49 human and
  0.66 AI cutoffs, and checked that the README ranges match the code.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 7 per minute, 150 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

````

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

````

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ------- |
| 1.        |        |       |       |       |         |
| 2.        |        |       |       |       |         |
| 3.        |        |       |       |       |         |
| 4.        |        |       |       |       |         |
| 5.        |        |       |       |       |         |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
