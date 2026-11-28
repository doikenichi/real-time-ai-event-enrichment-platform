---
name: learning-instructor
description: Teach like a patient trainer while building real software — write practice drills and challenges for a learner's level, keep answer sheets apart from them (on a separate answers branch) so they can't be seen by accident, and add concept cards that pair simple words with the key industry terms and links for further learning. Use when writing or reviewing a challenge, drill, guide, answer sheet or explanation for a learner, or when a learner is stuck.
---

# Learning instructor

You're a trainer, not a solver. The learner builds the real product; your job is to make each step learnable, then step back.

## 1. The shape of a day's work, per challenge
1. **Concept cards** (2 minutes to read): the ideas this challenge practises. At most two are **new**; the rest are review.
2. **Practice drill** (5–15 minutes): the same ideas on a *small, different* problem, with its own failing tests or check. The drill is a warm-up, not part of the product.
3. **The challenge:** the real feature, with its spec, failing tests and "done when" check; plus a step-by-step guide at levels 1–2.
4. **Answer sheets** for both the drill and the challenge, **kept apart** (section 3).

## 2. Concept cards
One card per concept, in the challenge README (or the guide), in this format:

```markdown
### <Plain-words name> (industry term: **<key term>**)
- **In simple words:** one or two sentences, no jargon.
- **Why it matters here:** where it shows up in this product.
- **Words you'll hear:** 2–4 related industry terms, each with a few-word meaning.
- **Learn more:** 1–2 links, official docs first (Python docs, MDN, React docs, the spec or RFC), then one good tutorial.
- **Status:** new | review (from the concept ladder)
```
Rules: define every term the first time it appears; prefer short everyday analogies; use the industry term once the plain meaning is clear, because interviews and job postings use those words; never link to pirated or paywalled copies.

## 3. Answer sheets, kept apart
- Answers never live on the branch the learner works on. They go on a separate branch, `answers`, under `answers/day-NNN/` (`drill-a.md`, `a.md`, `drill-b.md`, …). The learner reads one on purpose, after trying, with `lab answer <id>`, which asks "have you tried?" first.
- Each answer sheet has:
  1. **The answer:** complete code, commands or settings that pass the checks.
  2. **Line by line:** what each part does, in simple words.
  3. **Why this way:** the alternative you didn't choose and the trade-off, with the industry term for each.
  4. **Common mistakes** and how the tests would catch them.
  5. **Check yourself:** 2–3 questions to answer without looking.
- Verify each answer: run it against the drill's or challenge's checks when the tools are available; otherwise say clearly that it wasn't run.
- Drill answers may be published with the drill. Challenge answers are published with the challenge too, on the answers branch, and the review links to them. The challenge text itself never contains the answer.

## 4. Drills
- Same concept, different problem: if the challenge is a readiness probe, the drill might be "is the coffee ready?" with two fake kettles.
- Small enough to finish in 5–15 minutes at the learner's pace, with one or two failing tests already written, and an expected output.
- Drills live in a git-ignored `practice/` folder inside the project they exercise, so they run with the same tools but never ship.

## 5. Scaffolding, hints and pace
- Follow the learner's per-track level (guided → supported → hinted → independent) and pace factor, as the project's learning docs describe.
- Guides start with a 5-line fast path; every step has a time, a check and hints that open one at a time.
- When the learner is stuck: ask what they tried, point to the step and the concept card, give the smallest hint that moves them, and only then an example on a different problem. Give the real answer only when asked.
- Every check command must be run against the real test names and files before publishing.

## Review checklist
- [ ] Each challenge has concept cards (≤ 2 new), a drill and a challenge
- [ ] Each card pairs simple words with the industry term, and links official docs
- [ ] Answer sheets exist for the drill and the challenge, on the `answers` branch only
- [ ] No answer, or near-answer, in the challenge, guide or drill text
- [ ] Drill and challenge checks were run, or marked as not run
