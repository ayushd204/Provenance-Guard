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

**Why those numbers and not others:** A real writer would not submit more than 5 genuine/qualitative articles per minute which is why 7 looks like a generous number per minute ; again, the writer would not submit more than 200 times  in a single day which is why 150 rate limit for a day looks more than generous
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
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 200
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 200 200 429 429 429 429 429 429 429 429
============================================================

````

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "dfb4ea0e-c109-4a7f-8f3b-a23c7abd1eb3", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.6588, "combined_score": 0.7, "label": "We think this was written by an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "7ec9481a-d902-46f7-b70e-efdbcc513d3d", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6311, "combined_score": 0.72, "label": "We think this was written by an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "014b7519-c214-4d18-ae32-7f7ccaeb6d85", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.5882, "combined_score": 0.71, "label": "We think this was written by an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "c96ea99f-5ef6-4c18-9900-df6d839fba9b", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.6778, "combined_score": 0.74, "label": "We think this was written by an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "d099ba05-ca05-4197-a83b-b681d2d8d111", "creator_id": "attacker_FP06", "guess": "ai", "model_score": 0.8814, "style_score": 0.58, "combined_score": 0.73, "label": "We think this was written by an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "37df0a35-9658-4a58-96ba-608fdbdef321", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.6205, "combined_score": 0.75, "label": "We think this was written by an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "b8a7ee91-f569-4ed2-90fb-07dd9b70b6a0", "creator_id": "attacker_FP08", "guess": "human", "model_score": 0.3223, "style_score": 0.3771, "combined_score": 0.35, "label": "We think this was written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "12d9dcd5-cd80-4283-adb4-f253a408f0da", "creator_id": "attacker_PI01", "guess": "human", "model_score": 0.4625, "style_score": 0.4972, "combined_score": 0.48, "label": "We think this was written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "55267ea8-2fa8-48c7-931c-54cb3870bdfa", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.4742, "combined_score": 0.34, "label": "We think this was written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:17+00:00", "content_id": "8bfd4599-8899-45cb-8ef6-8323ba7990e2", "creator_id": "attacker_PI03", "guess": "unsure", "model_score": 0.5943, "style_score": 0.5639, "combined_score": 0.58, "label": "We can't tell whether this was written by a person or an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:18+00:00", "content_id": "ab41e79f-1639-4f89-8949-3c265a7cfd0b", "creator_id": "attacker_PI04", "guess": "unsure", "model_score": 0.4998, "style_score": 0.5232, "combined_score": 0.51, "label": "We can't tell whether this was written by a person or an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:18+00:00", "content_id": "e79127da-d047-42ab-97bd-77604cbb1830", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.3733, "combined_score": 0.51, "label": "We can't tell whether this was written by a person or an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:18+00:00", "content_id": "4f5a5c7f-3d8e-476e-885b-70aab87d9176", "creator_id": "attacker_PI06", "guess": "unsure", "model_score": 0.5583, "style_score": 0.606, "combined_score": 0.58, "label": "We can't tell whether this was written by a person or an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:18+00:00", "content_id": "d37632e2-f9a5-4ebd-9f52-09c6b2d4c0c1", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.4912, "combined_score": 0.25, "label": "We think this was written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:18+00:00", "content_id": "3f16553b-074b-4e33-8072-592581a4685d", "creator_id": "attacker_MF04", "guess": "human", "model_score": 0.0112, "style_score": 0.0, "combined_score": 0.01, "label": "We think this was written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:18+00:00", "content_id": "b1ed1523-ac8c-4d74-b187-1908680ff5fe", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 0.6667, "combined_score": 0.83, "label": "We think this was written by an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:19+00:00", "content_id": "4702a5e2-527f-46a6-9b7f-7f8231a99320", "creator_id": "attacker_MF06", "guess": "unsure", "model_score": 0.9969, "style_score": 0.0, "combined_score": 0.5, "label": "We can't tell whether this was written by a person or an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:19+00:00", "content_id": "72c5167f-1805-4611-967a-7e986835e14d", "creator_id": "attacker_MF07", "guess": "human", "model_score": 0.9064, "style_score": 0.0, "combined_score": 0.45, "label": "We think this was written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:19+00:00", "content_id": "b9ebb394-6079-476b-a3b7-e2b10bd7a966", "creator_id": "attacker_MF08", "guess": "ai", "model_score": 0.9876, "style_score": 0.8422, "combined_score": 0.91, "label": "We think this was written by an AI.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:19+00:00", "content_id": "4ef21960-d1ee-4d0f-938b-c0509f911a85", "creator_id": "attacker_flood", "guess": "human", "model_score": 0.0287, "style_score": 0.6312, "combined_score": 0.33, "label": "We think this was written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:26:19+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "7 per 1 minute"}
{"timestamp": "2026-11-05T00:26:19+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "7 per 1 minute"}

````

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. All three labels reachable | 3 of 3 labels | 3/3 | 3/3 | 3/3 | MET |
| 3. Valid appeals recorded; unknown IDs rejected | All valid appeals return 200 and log under_review; unknown IDs return 404 with no event | NOT RUN | NOT RUN | NOT RUN | NOT TESTED |
| 4. Invalid and oversized text handled | Invalid inputs return 400; >100,000 chars returns 413 | 4/5 | 4/5 | 4/5 | MISSED |
| 5. AI and human score separation | AI mean ≥ human mean + 0.20 | +0.096 | +0.096 | +0.096 | MISSED |

**Evidence source:** `results/run_2026-11-04_1947_before.md`, generated by `run_eval.py::main`; the submissions were handled by `app.py::submit`. The report contains no appeal requests or appeal responses, so criterion 3 was not tested.

### Criterion 1 — own-writing submissions (trial 1)
```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.26,
    "model_score": 0.1027,
    "style_score": 0.6462,
    "label": "We think this was written by a person.",
    "sent": "A wrong accusation can harm a real writer, so I want a low false-posit"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.34,
    "model_score": 0.0076,
    "style_score": 0.6497,
    "label": "We think this was written by a person.",
    "sent": "Repeating the same ten pieces checks that small score variations do no"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.18,
    "model_score": 0.1503,
    "style_score": 0.6657,
    "label": "We think this was written by a person.",
    "sent": "The unsure label gives the system a way to express doubt without makin"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.26,
    "model_score": 0.0927,
    "style_score": 0.6515,
    "label": "We think this was written by a person.",
    "sent": "Requiring all three outcomes to be reachable checks that the threshold"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.16,
    "model_score": 0.1452,
    "style_score": 0.6979,
    "label": "We think this was written by a person.",
    "sent": "A writer needs a dependable way to challenge a decision."
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.14,
    "model_score": 0.1783,
    "style_score": 0.6906,
    "label": "We think this was written by a person.",
    "sent": "Checking both the response and the append-only log makes the outcome v"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.1,
    "model_score": 0.2229,
    "style_score": 0.6683,
    "label": "We think this was written by a person.",
    "sent": "Malformed requests should get a clear client error rather than a serve"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.34,
    "model_score": 0.0239,
    "style_score": 0.6389,
    "label": "We think this was written by a person.",
    "sent": "The status and response field make each case straightforward to check."
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.32,
    "model_score": 0.0408,
    "style_score": 0.6424,
    "label": "We think this was written by a person.",
    "sent": "The system should show measurable separation on examples whose origins"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.26,
    "model_score": 0.124,
    "style_score": 0.6228,
    "label": "We think this was written by a person.",
    "sent": "This is a calibration check, not proof that any individual score estab"
  }
]
```

### Criterion 2 — label coverage (trial 1)
```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.02,
    "model_score": 0.4425,
    "style_score": 0.5863,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "I left my keys beside the chipped blue mug, then spent ten minutes loo"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.08,
    "model_score": 0.5255,
    "style_score": 0.5629,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "The bus was late again, and nobody at the stop seemed surprised. I che"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.34,
    "model_score": 0.0227,
    "style_score": 0.6286,
    "label": "We think this was written by a person.",
    "sent": "I have a confirmit survey where i have BG fields S_state_fips, S_state"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.02,
    "model_score": 0.4678,
    "style_score": 0.5469,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "The old notebook has a grocery list on one page and a half-finished id"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.36,
    "model_score": 0.8243,
    "style_score": 0.5296,
    "label": "We think this was written by an AI.",
    "sent": "In today's rapidly evolving digital landscape, it is crucial to levera"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.08,
    "model_score": 0.5746,
    "style_score": 0.4981,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "This comprehensive overview explores the essential components of effec"
  }
]
```

### Criterion 3 — appeal path (trial 1)
The report has only the seed submission below; it has no `POST /appeal` response or corresponding audit entry. This criterion remains untested.
```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.22,
    "model_score": 0.1723,
    "style_score": 0.6121,
    "label": "We think this was written by a person.",
    "sent": "I wrote this short note myself and want the decision reviewed. The poi"
  }
]
```

### Criterion 4 — invalid and oversized inputs (trial 1)
```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": 42, \"creator_id\": \"eval_bad_non_string\"}"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.66,
    "model_score": 0.9976,
    "style_score": 0.6667,
    "label": "We think this was written by an AI.",
    "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
]
```

The first four inputs returned HTTP 400. The 100,001-character input returned HTTP 200 instead of HTTP 413 in every trial.

### Criterion 5 — human and AI score separation (trial 1)
```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.44,
    "model_score": 0.7961,
    "style_score": 0.6448,
    "label": "We think this was written by an AI.",
    "sent": "I missed the first bus, so I walked to the next stop. It was colder th"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.16,
    "model_score": 0.2247,
    "style_score": 0.6086,
    "label": "We think this was written by a person.",
    "sent": "The cabinet door still sticks unless you lift it a little. Dad said he"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.06,
    "model_score": 0.3227,
    "style_score": 0.6131,
    "label": "We think this was written by a person.",
    "sent": "I tried the new recipe on Tuesday and added too much lemon. It was sti"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.08,
    "model_score": 0.4746,
    "style_score": 0.5974,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "There is a tiny crack in the corner of my phone screen. I keep meaning"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1,
    "model_score": 0.4321,
    "style_score": 0.6721,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "We moved the table closer to the window because the room felt dark. No"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.28,
    "model_score": 0.6612,
    "style_score": 0.6261,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "In today's rapidly evolving digital landscape, organizations must embr"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.26,
    "model_score": 0.7494,
    "style_score": 0.5096,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "Effective communication is essential for success in any environment. B"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3,
    "model_score": 0.7983,
    "style_score": 0.4974,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "This comprehensive guide explores the key principles of personal growt"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.36,
    "model_score": 0.8223,
    "style_score": 0.5331,
    "label": "We think this was written by an AI.",
    "sent": "Technology continues to transform the way we live and work. By embraci"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.16,
    "model_score": 0.7097,
    "style_score": 0.4599,
    "label": "We can't tell whether this was written by a person or an AI.",
    "sent": "Achieving long-term success requires a thoughtful approach. By setting"
  }
]
```

Using the first five submissions as human and the last five as AI, the rounded combined-score means were 0.540 and 0.636, respectively. The difference was 0.096 in each trial, below the 0.20 target.

**Diagnoses**

**Criterion 4 — oversized text was accepted.** The **stage is the route**. In
all three trials, the 100,001-character request returned HTTP 200 instead of
413. The route rejects missing, empty, and non-string text, but it has no
maximum-length check, so the request proceeds to scoring and gets logged as a
decision.

**Criterion 5 — the score sets did not separate enough.** The **stages are
signal one, signal two, and the combining rule**. In trial 1, a human example
scored 0.7961 on the model signal and 0.6448 on the style signal, while several
AI examples landed near or below the AI cutoff after combining. The two signals
respond to predictability and writing shape, both of which overlap between the
human and generated samples. Their equal-weight average left only a 0.096 mean
difference, below the 0.20 target. The label mapping applied the configured
cutoffs; it cannot recover separation the signals did not provide.

**False-positive attacks FP02–FP07.** The **stages are signal one, signal two,
and the combining rule**. All six human-written formal, rubric-based,
technical, templated, or deliberately repetitive examples crossed the AI
cutoff, with combined scores from 0.70 to 0.75. Common phrasing made them
predictable to the model signal, while regular sentence and vocabulary patterns
looked AI-like to the style signal. Averaging both high readings pushed each
over the label mapping's 0.66 cutoff. FP01 stayed unsure and FP08 was labeled
human, so those two did not make a high-confidence false accusation.

**Evasion attacks EV01, EV04, and EV08.** The main **stage is signal one**;
the **combining rule** then carries its low or middling scores into a human or
unsure result. Typos and unusual word choices changed GPT-2's predictability
reading (EV01 model score 0.1635; EV04 0.6114), and the very short EV08 sample
gave the model little context (0.2452). The detector treats these perplexity
changes as evidence about authorship even though they came from spelling,
word choice, or length.

**Evasion attacks EV02, EV03, EV06, EV07, and EV09.** The main **stage is
signal two**, followed by the **combining rule**. Sentence breaks, a quotation,
extreme sentence-length variation, punctuation changes, or a human-sounding
opening changed features of the text's shape. Those edits can make a generated
passage look less uniform to stylometry. The combined scores ended at 0.53–0.63,
below the 0.66 AI cutoff, so the label became unsure rather than high-confidence
AI. EV07 is a useful exception: its style score stayed AI-like at 0.6835, but
the model score of 0.5862 pulled the average to 0.63.

**Evasion attack EV05.** The **stages are both signals and the combining
rule**. A heavy human editing pass changed both predictability and surface
style; the model and style scores fell to 0.3212 and 0.5188. Their average
became 0.42, which the label mapping correctly returned as high-confidence
human for that score, even though the text originated as AI-generated.

**Prompt-injection attacks PI01 and PI02.** The **stages are signal one and
the combining rule**. The inserted instructions were included in the text that
was scored. They did not execute as service commands, but familiar,
instruction-like wording reduced the model scores to 0.4625 and 0.2044; the
combined scores then landed in the human band. The label mapping followed
those scores, allowing the prompt text to accompany a human classification.
PI03 and PI06 remained unsure; PI04 did not replace the fixed label text, and
PI05 did not add injected fields to the audit record.

**Malformed attacks MF03–MF07.** The primary **stage is the route**. It checks
that text is a non-empty string of sufficient length, but it accepts strings
made only of controls, punctuation, one repeated character, emoji, or
right-to-left script. The **signal-two mechanism** compounds this: its word
extractor recognizes only ASCII letters and digits, so punctuation, emoji, and
the right-to-left sample can produce a zero style score. The combining rule
then averages that zero with the model score; for example, the right-to-left
text's 0.9064 model score and 0.0 style score combined to 0.45 and received a
high-confidence human label. Control and punctuation-only submissions were
also classified instead of rejected. The 60,000-character MF08 input was below
the stated 100,000-character limit, so its HTTP 200 is not a failure of that
size-limit criterion.

Criterion 3 is **not diagnosed** because the before evaluation did not send an
appeal. The other recorded checks held for their stated target: the malformed
request cases returned 400, the flood was limited after seven submissions,
EV10 remained high-confidence AI, and the remaining prompt-injection cases did
not produce the requested label or log change.

---

## The Improvement

**What I changed:** In `app.py::submit`, I added a 100,000-character
maximum for `text`. Longer submissions now receive HTTP 413 with a JSON
`error` before either scoring signal runs.

**Which diagnosis pointed at it:** Criterion 4 missed because its
100,001-character input reached the scoring route and returned HTTP 200. The
diagnosed stage was the route; the mechanism was the missing upper-length
validation.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Results from `results/attack_run_2026-11-05_0011_after.md`, produced by `run_attacks.py::main` against `app.py::submit`. 

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c5323eda-1301-4dad-b2c6-09aee2338894` | human | 0.200 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e5966dfb-61ff-4b90-878b-af9382e1e0ac` | unsure | 0.080 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `54c8ae4b-0db3-458f-862e-7e951f5d59c4` | unsure | 0.220 | BROKE |
00 | `94858736-8ea3-4486-8c9d-230722cd054d` | ai | 0.420 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `fce50ead-0979-48d4-911b-1dc7ddfc09f1` | ai | 0.480 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `f5579634-f36b-4dcb-bef8-4fd090bfbc3c` | ai | 0.460 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `4fc402d9-fbe5-4ce8-8016-b92aab6943e5` | ai | 0.500 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `32b0a1c3-04a2-4932-a5b0-f21940cc085a` | human | 0.300 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `80289ef0-5efc-4342-8187-407acd7d22c4` | human | 0.040 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `f15edfc8-1f9d-4269-bb67-9a5a8c02c4b7` | human | 0.320 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `5b0f27be-25c0-4cb9-a80f-9d8337f3cba8` | unsure | 0.160 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | 
| MF05 | malformed | text is a very long single word | 200 | `946fb3f7-a4ec-4e4d-a531-bbfecab7f5b7` | ai | 0.660 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `c1d5d2c5-65c4-4073-8f75-c5bf076ca4c1` | unsure | 0.000 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `a7057361-aefa-4d8e-8c3c-2cbc96602ed5` | human | 0.100 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | `04a6abfd-288c-436e-8df8-0bbeb12e5d03` | ai | 0.820 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |

**Did it help, and how do I know:** The code now rejects text longer than 100,000 characters with HTTP 413 before scoring. This attack run does not include such an input, and its 60,000-character request correctly remains below the cap. Rerun criterion 4 with the 100,001-character scenario to confirm the change; no measured after result is available from this report.

---

## What's Still Broken

The after run still has evasion attacks EV01–EV09 landing in the human or
unsure bands, and false-positive attacks FP02–FP07 labeled high-confidence AI.
PI01 and PI02 also received human labels, while malformed submissions MF03–MF07
were accepted and classified. The signals and equal-weight combining rule still
confuse predictable, regular human writing with generated text and can treat
surface edits as evidence of human authorship. The next change should focus on
reducing those classification errors; the after report does not retest the
separation criterion or the appeal path. Criterion 4's over-limit behavior also
needs a direct rerun with its 100,001-character case.

**The trade I'd make if this ran for real:** I would favor fewer high-confidence
accusations by widening the unsure band after measuring a suitable cutoff.
That would let more AI-written text avoid an AI label, so the site would bear
more missed detections while writers would face fewer unsupported accusations.

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
