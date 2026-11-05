"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "A wrong accusation can harm a real writer, so I want a low false-positive rate even if that means some AI writing lands in the unsure band.",
            "Repeating the same ten pieces checks that small score variations do not keep flipping human work into an accusation.",
            "The unsure label gives the system a way to express doubt without making an accusation.",
            "Requiring all three outcomes to be reachable checks that the thresholds and scores are not effectively collapsing into one label.",
            "A writer needs a dependable way to challenge a decision.",
            "Checking both the response and the append-only log makes the outcome visible and traceable.",
            "Malformed requests should get a clear client error rather than a server crash, and a fixed size limit prevents an unexpectedly large submission from consuming unbounded time or memory.",
            "The status and response field make each case straightforward to check.",
            "The system should show measurable separation on examples whose origins are known, while the 0.20 margin avoids treating a tiny average difference as useful.",
            "This is a calibration check, not proof that any individual score establishes authorship.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 2,
        # Inputs spread across your score range, so you can check all three
        # labels are actually reachable.
        "texts": [
            "I left my keys beside the chipped blue mug, then spent ten minutes looking for them. The rain had stopped, but the window still clicked in the wind.",
            "The bus was late again, and nobody at the stop seemed surprised. I checked the time, put my phone away, and watched a dog pull its owner toward the bakery.",
            "I have a confirmit survey where i have BG fields S_state_fips, S_state , respemail variables. My survey page gets email and State (dropdown field) from the respondent and i want to validate the combination on respondentdata",
            "The old notebook has a grocery list on one page and a half-finished idea on the next. I keep it because both are useful in different ways.",
            "In today's rapidly evolving digital landscape, it is crucial to leverage innovative, cutting-edge solutions to unlock new opportunities, foster meaningful connections, and drive impactful outcomes. By harnessing the power of technology, we can navigate complex challenges and build a brighter future.",
            "This comprehensive overview explores the essential components of effective communication. By embracing clarity, consistency, and collaboration, organizations can empower teams, strengthen relationships, and achieve sustainable success in an increasingly dynamic environment.",
        ],
    },
    {
        "name": "appeal path seed submission (appeal by hand)",
        "criterion": 3,
        # Submit this first, then appeal the returned content_id manually.
        "texts": [
            "I wrote this short note myself and want the decision reviewed. The point is to verify that a real submission can be appealed and recorded.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 4,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": 42, "creator_id": "eval_bad_non_string"},
            {"text": "x" * 100001, "creator_id": "eval_bad_huge"},
        ],
    },
    {
        "name": "human and AI score separation",
        "criterion": 5,
        # First five are human-origin; last five are AI-generated.
        "texts": [
            "I missed the first bus, so I walked to the next stop. It was colder than I expected, and I wished I had brought gloves.",
            "The cabinet door still sticks unless you lift it a little. Dad said he would fix it last weekend, but we both forgot.",
            "I tried the new recipe on Tuesday and added too much lemon. It was still edible, though my roommate laughed when I made a face.",
            "There is a tiny crack in the corner of my phone screen. I keep meaning to get it repaired, then remember only when the light catches it.",
            "We moved the table closer to the window because the room felt dark. Now the plants seem happier, and there is less space to walk past.",
            "In today's rapidly evolving digital landscape, organizations must embrace innovative solutions to unlock their full potential. By leveraging advanced technologies and fostering collaboration, teams can drive meaningful outcomes and build a sustainable future.",
            "Effective communication is essential for success in any environment. By prioritizing clarity, consistency, and collaboration, individuals can strengthen relationships, overcome challenges, and achieve shared goals.",
            "This comprehensive guide explores the key principles of personal growth. Through dedication, resilience, and a commitment to continuous learning, anyone can develop the skills needed to thrive in an ever-changing world.",
            "Technology continues to transform the way we live and work. By embracing emerging tools and adapting to new opportunities, communities can create a more connected, efficient, and inclusive future.",
            "Achieving long-term success requires a thoughtful approach. By setting clear objectives, building strong habits, and remaining open to feedback, individuals can make steady progress toward their aspirations.",
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
