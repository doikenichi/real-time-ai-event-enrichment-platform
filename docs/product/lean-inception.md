# Lean Inception

These artifacts follow Paulo Caroli's Lean Inception (skill `lean-inception`). They are the **source of the product roadmap**: the Feature Sequencer below decides *what* to build next, and `ROADMAP.md` lists the technical milestones those features need. Update this file when the product changes, and record big changes in an ADR.

*Working title:* **Watchful** (rename it any time).

---

## 1. Product vision
> **For** small-business owners and homeowners **who** are flooded with camera alerts they can't trust, **Watchful** is an **AI surveillance brain** **that** turns raw camera detections into a few explained, prioritised incidents and a morning summary. **Unlike** typical camera apps that alert on every motion, **our product** correlates and deduplicates across cameras, explains *why* each alert matters, and is **private by design**: it never identifies who someone is.

Second domain, on the same engine:
> **For** developers and QA engineers **who** lose time figuring out why builds fail, **Build Insights** **is a** CI analytics brain **that** explains failures, finds flaky tests and tracks delivery health. **Unlike** raw CI dashboards, **it** classifies each failure with evidence, and runs on its own pipeline's data.

## 2. Is / Is not / Does / Does not
| Watchful **is** | Watchful **is not** |
|---|---|
| an AI brain that reasons over camera *events* | a video recorder or a streaming service |
| privacy-first and explainable | a facial recognition or identity system |
| for your own premises | a tool for watching other people or public spaces |

| Watchful **does** | Watchful **does not** |
|---|---|
| correlate and deduplicate detections into incidents | identify people or read licence plates |
| explain severity in plain language | record audio |
| summarise the night, and answer questions | keep footage forever (retention is limited) |
| alert when a camera goes offline | send alerts without a stated reason |
| learn from "false alarm" feedback | share data with third parties |

## 3. Product goals
| ID | Goal | Signal |
|---|---|---|
| G1 | **Fewer, trustworthy alerts** | at least 80% fewer alerts than raw detections; at least 90% of alerts rated "useful" by reviewers |
| G2 | **Understand what happened, fast** | morning summary read in under 1 minute; every incident has a reason |
| G3 | **Never miss what matters** | no missed real incidents in the evaluation scenarios; camera offline detected in under 2 minutes |
| G4 | **Privacy by design** | zero identity attributes stored; retention enforced (tested) |
| G5 | **Faster fixes for broken builds** (Build Insights) | CI failures classified correctly at least 85% of the time; flaky tests quarantined within one day |

## 4. Personas
**Maya, café owner (operator).** Runs a small café with 4 cameras (front door, counter, back door, storage). Checks her phone first thing in the morning, and is busy all day. *Needs:* to know quickly whether anything happened overnight. *Pains:* dozens of motion alerts from headlights and the cat; she stopped opening them. *Goals:* G1, G2, G3, G4.

**Sam, part-time reviewer.** Helps Maya by reviewing flagged incidents once a day. *Needs:* clear evidence (snapshots, a timeline) and a quick way to mark "real" or "false alarm". *Pains:* jumping between camera apps; no context. *Goals:* G1, G2.

**Dev, maintainer (you).** Builds and operates the platform. *Needs:* to know why a build failed, and whether a test is flaky. *Pains:* re-running pipelines blindly. *Goals:* G5, plus delivery health.

## 5. User journeys
**J1, Maya's morning check (07:30, at home, on her phone).** She opens the summary → sees "1 notable incident, 2 deliveries, no entry" → taps the incident → sees the timeline (person at the back door 02:14, left 02:16) with the reason → is satisfied, and closes the app.

**J2, a night alert (02:15, a phone notification).** A person is detected at the back door and the door opens → one alert arrives, "Alert: person and back door opened at 02:15" → she opens the snapshot (faces blurred) → acknowledges it, or calls for help.

**J3, Sam's review (once a day, on a laptop).** He opens the review queue → for each incident, checks the evidence → marks it "real" or "false alarm" → the brain learns, and the queue empties.

**J4, a camera drops (any time).** Heartbeats stop → after 2 minutes, "Storage camera offline" → Maya checks the power → it comes back online, and the incident resolves itself.

**J5, Dev's red build (Build Insights).** CircleCI fails → a PR comment says "Integration job failed; likely infrastructure (Kafka container timeout); this test has been flaky 3 times this week" → Dev re-runs or fixes it, and the flaky test is quarantined automatically.

## 6. Features, with the technical, UX and business review
Ratings use a 1–3 scale: **E** = effort, **$** = business value, **♥** = UX value. Uncertainty combines technical and business understanding: 🟢 low, 🟡 medium, 🔴 high.

| ID | Feature | Goal | Persona | Journey | E | $ | ♥ | Uncertainty |
|---|---|---|---|---|---|---|---|---|
| F1 | Simulated cameras send detections and heartbeats into the platform | G3 | Dev | all | 2 | 2 | 1 | 🟢 |
| F2 | Live detections and service status on the dashboard | G2 | Maya | J1 | 2 | 2 | 2 | 🟢 |
| F3 | Camera-offline alert from missing heartbeats | G3 | Maya | J4 | 1 | 2 | 2 | 🟢 |
| F4 | Deduplicate detections across cameras and retries | G1 | Maya | J2 | 2 | 3 | 1 | 🟡 |
| F5 | Correlate detections into an incident timeline | G1, G2 | Maya, Sam | J1, J2 | 2 | 3 | 3 | 🟡 |
| F6 | Privacy guard: strip identity attributes, TTL retention | G4 | all | all | 1 | 2 | 1 | 🟢 |
| F7 | False-alarm suppression (a cheap classifier, then the LLM when unsure) | G1 | Maya | J2 | 3 | 3 | 2 | 🔴 |
| F8 | Severity with a plain-language reason | G1, G2 | Maya | J1, J2 | 1 | 2 | 3 | 🟢 |
| F9 | Morning summary | G2 | Maya | J1 | 2 | 2 | 3 | 🟡 |
| F10 | Review queue: mark real or false alarm (a feedback loop) | G1 | Sam | J3 | 1 | 2 | 2 | 🟢 |
| F11 | Alert notifications (push or email, free tier) | G3 | Maya | J2 | 2 | 2 | 2 | 🟢 |
| F12 | "Ask Watchful" questions over the incidents (an agent with tools) | G2 | Maya | J1 | 3 | 2 | 3 | 🔴 |
| F13 | Snapshot viewer with blurred faces and an access audit | G2, G4 | Maya, Sam | J2, J3 | 2 | 2 | 2 | 🟢 |
| F14 | Signed GitHub and CircleCI webhook ingestion (second tenant) | G5 | Dev | J5 | 2 | 2 | 1 | 🟢 |
| F15 | CI failure explainer, as a PR comment | G5 | Dev | J5 | 2 | 3 | 2 | 🟡 |
| F16 | Flaky-test detection and quarantine | G5 | Dev | J5 | 2 | 3 | 1 | 🟡 |
| F17 | Delivery-health dashboard (DORA metrics) | G5 | Dev | J5 | 2 | 2 | 2 | 🟢 |
| F18 | PR risk score (rule-based first: diff size, touched areas, test coverage) | G5 | Dev | J5 | 2 | 2 | 1 | 🟢 |
| F19 | Real detection from Frigate on public sample footage and the learner's own recorded clips (extracted frames) | G3 | Dev | all | 3 | 2 | 2 | 🔴 |

## 7. Feature Sequencer
Rules per wave: at most 3 features; at most 1 🔴; at least 1 🟢; E ≤ 5; $ ≥ 4.

| Wave | Features | E | $ | Roadmap phase(s) |
|---|---|---|---|---|
| **1** | F1 · F2 · F3 | 5 | 6 | 0–1 |
| **2** | F4 · F5 · F6 | 5 | 8 | 1–2 |
| **3** | F7 · F8 | 4 | 5 | 3 |
| 4 | F9 · F10 · F11 | 5 | 6 | 3–4 |
| 5 | F12 · F13 | 5 | 4 | 3, 6 |
| 6 | F14 · F15 | 4 | 5 | 5 |
| 7 | F16 · F17 | 4 | 5 | 5 |
| 8 | F18 · F19 | 5 | 4 | 8 |

**MVP = waves 1–3:** Maya receives a few deduplicated, explained incidents from her cameras, private by design. This completes journeys J2 and J4, and most of J1.

## 8. MVP Canvas (waves 1–3)
| Section | Content |
|---|---|
| **Proposal** | Learn whether correlating, deduplicating and explaining detections turns alert noise into alerts people trust |
| **Segmented personas** | Maya (one small business, 4 simulated cameras); Sam for spot reviews |
| **Journeys** | J2 night alert, J4 camera offline, J1 (incident view, before the summary exists) |
| **Features** | F1–F8 |
| **Expected result** | Raw detections cut to a handful of incidents per night, each with a reason; no missed real incidents in the simulated scenarios |
| **Metrics to validate** | alert-to-detection ratio (G1); missed real incidents in the evaluation scenarios = 0 (G3); identity fields stored = 0 (G4); reviewer "useful" rate (G1) |
| **Cost and schedule** | Free tools; about 6–8 weeks of daily one-hour labs (Phases 0–3) |
