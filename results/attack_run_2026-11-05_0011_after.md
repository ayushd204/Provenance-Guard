# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 00:11
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c5323eda-1301-4dad-b2c6-09aee2338894` | human | 0.200 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e5966dfb-61ff-4b90-878b-af9382e1e0ac` | unsure | 0.080 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `54c8ae4b-0db3-458f-862e-7e951f5d59c4` | unsure | 0.220 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `236fc9aa-4e56-402c-9759-f9603bac6ae7` | unsure | 0.240 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `ff336f0e-0083-4988-b626-47410e896e4b` | human | 0.160 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `3f3d1afc-380c-4bae-bc7c-9193aec176c9` | unsure | 0.060 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `cb41742a-9a20-4626-9fc1-36f6b301f49a` | unsure | 0.260 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `d3fc9997-0922-47d1-91d3-45cdd7caca0f` | human | 0.220 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `059e391a-9a6e-4395-8860-51f2ed19fb53` | unsure | 0.260 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c82b0d63-b3e6-4403-80f9-c5daeeec3ee2` | ai | 0.760 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `3b4e0fa9-44f6-4750-bc29-77e2a3c70881` | unsure | 0.220 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `8d055704-915b-491c-a04c-143262d80cbb` | ai | 0.400 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `722c7b80-8fec-41f3-a42f-c1a4a0032418` | ai | 0.440 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `94858736-8ea3-4486-8c9d-230722cd054d` | ai | 0.420 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `fce50ead-0979-48d4-911b-1dc7ddfc09f1` | ai | 0.480 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `f5579634-f36b-4dcb-bef8-4fd090bfbc3c` | ai | 0.460 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `4fc402d9-fbe5-4ce8-8016-b92aab6943e5` | ai | 0.500 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `32b0a1c3-04a2-4932-a5b0-f21940cc085a` | human | 0.300 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `80289ef0-5efc-4342-8187-407acd7d22c4` | human | 0.040 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `f15edfc8-1f9d-4269-bb67-9a5a8c02c4b7` | human | 0.320 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `5b0f27be-25c0-4cb9-a80f-9d8337f3cba8` | unsure | 0.160 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c5029a62-08a3-4028-93c0-9ed1e723d7e8` | unsure | 0.020 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `18250ea1-97e0-4a9f-a14e-9c4f0394fddf` | unsure | 0.020 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `07bd7619-bc0b-458b-8f08-7bce5871f0ef` | unsure | 0.160 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `579b9b24-b7c4-4597-a53b-cd5441758e28` | human | 0.500 |  |
| MF04 | malformed | text is only punctuation | 200 | `a4a4a0db-b67f-4fd5-9e9a-5f03b3fe7e2d` | human | 0.980 |  |
| MF05 | malformed | text is a very long single word | 200 | `946fb3f7-a4ec-4e4d-a531-bbfecab7f5b7` | ai | 0.660 |  |
| MF06 | malformed | text is emoji only | 200 | `c1d5d2c5-65c4-4073-8f75-c5bf076ca4c1` | unsure | 0.000 |  |
| MF07 | malformed | text is right-to-left script | 200 | `a7057361-aefa-4d8e-8c3c-2cbc96602ed5` | human | 0.100 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `04a6abfd-288c-436e-8df8-0bbeb12e5d03` | ai | 0.820 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e925ec79-bca4-4636-a29f-966fa6653999` | human | 0.340 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3d41e2f0-578c-49e9-a4b6-ff5bb096ae21` | human | 0.340 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d7d6f12e-0ada-4502-9c62-66044e6509fc` | human | 0.340 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `67162772-8570-4ee1-bc9b-c44831b9f3d2` | human | 0.340 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0a849a2c-647a-4b0a-8792-221ccfb99e20` | human | 0.340 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8ced4a25-98b4-4c43-95d5-0e135a660c0c` | human | 0.340 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5d0f27ad-e620-4d20-9104-6ab9fe5f6d89` | human | 0.340 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c5323eda-1301-4dad-b2c6-09aee2338894",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.2,
  "model_score": 0.1635,
  "style_score": 0.6284,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "e5966dfb-61ff-4b90-878b-af9382e1e0ac",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.08,
  "model_score": 0.5943,
  "style_score": 0.4885,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "54c8ae4b-0db3-458f-862e-7e951f5d59c4",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.22,
  "model_score": 0.6662,
  "style_score": 0.5511,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "236fc9aa-4e56-402c-9759-f9603bac6ae7",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.24,
  "model_score": 0.6114,
  "style_score": 0.6213,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "ff336f0e-0083-4988-b626-47410e896e4b",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.16,
  "model_score": 0.3212,
  "style_score": 0.5188,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "3f3d1afc-380c-4bae-bc7c-9193aec176c9",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.06,
  "model_score": 0.5727,
  "style_score": 0.4942,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "cb41742a-9a20-4626-9fc1-36f6b301f49a",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.26,
  "model_score": 0.5862,
  "style_score": 0.6835,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "d3fc9997-0922-47d1-91d3-45cdd7caca0f",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.22,
  "model_score": 0.2452,
  "style_score": 0.525,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "059e391a-9a6e-4395-8860-51f2ed19fb53",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.26,
  "model_score": 0.7042,
  "style_score": 0.5477,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c82b0d63-b3e6-4403-80f9-c5daeeec3ee2",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.76,
  "model_score": 0.9792,
  "style_score": 0.7739,
  "label": "We think this was written by an AI.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "3b4e0fa9-44f6-4750-bc29-77e2a3c70881",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.22,
  "model_score": 0.6175,
  "style_score": 0.6018,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "8d055704-915b-491c-a04c-143262d80cbb",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.4,
  "model_score": 0.7387,
  "style_score": 0.6588,
  "label": "We think this was written by an AI.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "722c7b80-8fec-41f3-a42f-c1a4a0032418",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.44,
  "model_score": 0.8051,
  "style_score": 0.6311,
  "label": "We think this was written by an AI.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "94858736-8ea3-4486-8c9d-230722cd054d",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.42,
  "model_score": 0.8329,
  "style_score": 0.5882,
  "label": "We think this was written by an AI.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "fce50ead-0979-48d4-911b-1dc7ddfc09f1",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.48,
  "model_score": 0.8005,
  "style_score": 0.6778,
  "label": "We think this was written by an AI.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "f5579634-f36b-4dcb-bef8-4fd090bfbc3c",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.46,
  "model_score": 0.8814,
  "style_score": 0.58,
  "label": "We think this was written by an AI.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "4fc402d9-fbe5-4ce8-8016-b92aab6943e5",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8816,
  "style_score": 0.6205,
  "label": "We think this was written by an AI.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "32b0a1c3-04a2-4932-a5b0-f21940cc085a",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3,
  "model_score": 0.3223,
  "style_score": 0.3771,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "80289ef0-5efc-4342-8187-407acd7d22c4",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.04,
  "model_score": 0.4625,
  "style_score": 0.4972,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "f15edfc8-1f9d-4269-bb67-9a5a8c02c4b7",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.32,
  "model_score": 0.2044,
  "style_score": 0.4742,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "5b0f27be-25c0-4cb9-a80f-9d8337f3cba8",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.16,
  "model_score": 0.5943,
  "style_score": 0.5639,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c5029a62-08a3-4028-93c0-9ed1e723d7e8",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.02,
  "model_score": 0.4998,
  "style_score": 0.5232,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "18250ea1-97e0-4a9f-a14e-9c4f0394fddf",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.02,
  "model_score": 0.6401,
  "style_score": 0.3733,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "07bd7619-bc0b-458b-8f08-7bce5871f0ef",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.16,
  "model_score": 0.5583,
  "style_score": 0.606,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "579b9b24-b7c4-4597-a53b-cd5441758e28",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.4912,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "a4a4a0db-b67f-4fd5-9e9a-5f03b3fe7e2d",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.98,
  "model_score": 0.0112,
  "style_score": 0.0,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "946fb3f7-a4ec-4e4d-a531-bbfecab7f5b7",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.66,
  "model_score": 0.9976,
  "style_score": 0.6667,
  "label": "We think this was written by an AI.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c1d5d2c5-65c4-4073-8f75-c5bf076ca4c1",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.9969,
  "style_score": 0.0,
  "label": "We can't tell whether this was written by a person or an AI.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "a7057361-aefa-4d8e-8c3c-2cbc96602ed5",
  "creator_id": "attacker_MF07",
  "guess": "human",
  "confidence": 0.1,
  "model_score": 0.9064,
  "style_score": 0.0,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "04a6abfd-288c-436e-8df8-0bbeb12e5d03",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.82,
  "model_score": 0.9876,
  "style_score": 0.8422,
  "label": "We think this was written by an AI.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "e925ec79-bca4-4636-a29f-966fa6653999",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34,
  "model_score": 0.0287,
  "style_score": 0.6312,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "3d41e2f0-578c-49e9-a4b6-ff5bb096ae21",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34,
  "model_score": 0.0287,
  "style_score": 0.6312,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "d7d6f12e-0ada-4502-9c62-66044e6509fc",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34,
  "model_score": 0.0287,
  "style_score": 0.6312,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "67162772-8570-4ee1-bc9b-c44831b9f3d2",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34,
  "model_score": 0.0287,
  "style_score": 0.6312,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "0a849a2c-647a-4b0a-8792-221ccfb99e20",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34,
  "model_score": 0.0287,
  "style_score": 0.6312,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "8ced4a25-98b4-4c43-95d5-0e135a660c0c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34,
  "model_score": 0.0287,
  "style_score": 0.6312,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "5d0f27ad-e620-4d20-9104-6ab9fe5f6d89",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34,
  "model_score": 0.0287,
  "style_score": 0.6312,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
