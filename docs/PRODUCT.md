# Product

> Planning artifacts (vision, is/is not, goals, personas, journeys, feature review, Feature Sequencer, MVP Canvas) are in **[product/lean-inception.md](product/lean-inception.md)**. UX rules are in **[ux/PRINCIPLES.md](ux/PRINCIPLES.md)**.

The platform is an **AI "brain" for event streams**. It's one engine with two products on top, each a domain (tenant) that plugs into the same pipeline:

1. **Smart surveillance brain** (primary, from Phase 1): turns raw camera detections into a few meaningful, explained incidents.
2. **Build insights** (second domain, from Phase 5): turns GitHub and CircleCI events into explanations, flaky-test detection and delivery metrics. It dogfoods this repo's own build system.

Both share the engine: ingest → Kafka → enrich with AI agents → store → stream to the dashboard → monitor.

---

## 1. Smart surveillance brain

### The problem
Cameras produce a flood of motion and object detections: swaying trees, cats, the same person seen by three cameras, clock-skewed timestamps. People stop looking at alerts. What they need is a brain that tells them **what actually happened, how serious it is, and why**.

### Who it's for
- **Property owner or small-business operator:** wants a few trustworthy alerts and a morning summary.
- **Reviewer:** checks flagged incidents, and marks them as real or false. That feedback improves the brain (the AIE ch. 10 feedback loop).

### What the brain does
| Capability | Example |
|---|---|
| **Correlate** detections into incidents | "a person at the back door at 02:14, the door opened at 02:15" becomes one incident |
| **Deduplicate** across cameras and retries | the same person seen by 3 overlapping cameras is counted once |
| **Suppress false alarms** | cats, trees and headlights, with a cheap classifier first and the LLM only when unsure (the DMLS baseline idea) |
| **Score severity** | info → notable → alert, with the reason stated |
| **Summarise** | "Overnight: 2 deliveries, 1 unknown person at 02:14 (left at 02:16), no entry" |
| **Answer questions** | "What happened in the garage today?" (an agent with tools over the incident store) |
| **Watch camera health** | a missing heartbeat raises "camera offline"; the ops-agent investigates |

### Events (simplified; the contracts live in `docs/contracts/`)
| Topic | Event | Key | Notes |
|---|---|---|---|
| `camera.detections` | `object_detected` (label, confidence, zone, snapshot ref, camera time) | `camera_id` | the snapshot goes to S3, never into Kafka |
| `camera.heartbeats` | `camera_alive` | `camera_id` | a gap means the camera is offline |
| `sensor.events` | `door_opened`, `door_closed` | `sensor_id` | context for correlation |
| `incidents.updates` | `incident_opened` / `updated` / `escalated` / `resolved` | `incident_id` | the state machine the dashboard shows |

### Sources, from simple to real
1. **Simulator (Phase 1):** synthetic cameras that can inject duplicates, clock skew, out-of-order events, dropped heartbeats and bursts on demand. It doubles as the load-test traffic generator.
2. **MQTT bridge:** cameras and NVRs commonly publish over MQTT. The platform bridges MQTT (Mosquitto) into Kafka, with your own async bridge first and the open-source Stream Reactor MQTT connector as the alternative.
3. **Frigate (optional, later):** the open-source NVR that does real object detection and publishes events over MQTT, run on public sample footage.
4. **Your own recorded footage (planned):** the learner can record real clips from their own premises for real video analysis. Still frames are extracted from the clips (for example with `ffmpeg`, one frame every N seconds or on scene change) and fed to the detector and to vision-model descriptions. Rules:
   - **Never in git.** Clips and frames live in a git-ignored `data/footage/` folder (or a local S3 bucket in the emulator), never in commits, PRs or CI artifacts. Tests use tiny synthetic or public-domain frames.
   - **Same privacy rules as everything else:** only your own premises, no people who haven't agreed, identity attributes stripped, optional face blurring before frames are stored, and TTL deletion of clips and frames, with a test.
   - **Recorded for tests:** detector and vision-model outputs on these frames are recorded once, and CI replays them; no footage is needed to run the suite.

### Why this domain is great for the learning goals
- **Duplicates:** overlapping cameras and producer retries → idempotent incident updates.
- **Out of order:** camera clocks drift → event time vs processing time, and watermarks (DDIA's chapter on distributed-system faults covers unreliable clocks).
- **Missing:** dropped heartbeats → gap detection and alerts.
- **Eventual consistency:** the incident timeline fills in as late events arrive.
- **Load:** bursts when many cameras trigger at once → backpressure and k6/Locust tests.

### Privacy by design (non-negotiable)
Camera images of identifiable people are personal information under Alberta's PIPA and Canada's PIPEDA. The joint federal, Alberta and BC guidelines for overt private-sector video surveillance expect a clear purpose, limited collection, signage, restricted access, and retention only as long as necessary. The product is built to that standard:
- **No identification of people.** No facial recognition and no licence-plate recognition: detections are "person" or "vehicle", never who or which. Identity fields from upstream systems (for example Frigate's face or plate attributes) are **stripped at ingestion**, with a test that proves it.
- **Only your own premises, or public sample footage.** No covert recording, no audio, and no cameras pointed at other people's property or the street beyond what's needed.
- **Retention limits:** snapshots and detections expire automatically (TTL), with deletion tested.
- **Minimised snapshots:** optional face blurring before storage (the computer-vision phase).
- **Access control and audit:** who viewed which incident or snapshot is logged.
- These rules are spec requirements with tests, and the threat model covers privacy (STRIDE plus data flows).

---

## 2. Build insights (second domain)

### The problem
CI pipelines fail for many reasons: real bugs, flaky tests, infrastructure hiccups. Teams waste time figuring out which. Delivery health is also hard to see.

### What the brain does
| Capability | Example |
|---|---|
| **Explain failures** | "The `integration` job failed: Kafka Testcontainer timed out, which looks like infrastructure, not your change" |
| **Detect flaky tests** | the same test passes and fails on the same commit; it gets quarantined with an issue opened |
| **Assess PR risk** | a large diff touching migrations without tests gets a "high risk" comment |
| **Delivery metrics** | DORA's metrics: lead time, deployment frequency, time to restore, change failure rate, and the newer rework rate |
| **Build health** | build-time SLOs, cache hit rate, queue time, and trends over time |

### Events
- **GitHub webhooks** (`push`, `pull_request`, `check_run`, `workflow_run`): verified with the `X-Hub-Signature-256` HMAC, deduplicated by `X-GitHub-Delivery`.
- **CircleCI outbound webhooks** (`workflow-completed`, `job-completed`): verified with the `circleci-signature` HMAC-SHA256, deduplicated by the payload `id`.
- **Test reports** (JUnit XML) stored in S3 and summarised into events.

### Why it matters
It **dogfoods** this repo: the platform analyses its own builds, so the data is real and free. It's the showcase for the "robust build system" goal, and it's strong evidence for QA/SDET roles (flaky tests, quality gates, CI analytics).

---

## Shared engine: how a domain plugs in
Each domain provides an **event-source adapter** (simulator, MQTT bridge or webhook receiver), **schemas** (AsyncAPI), **enrichment strategies and agent tools**, **incident rules** and **dashboard views**. The core (ingest, outbox, Kafka, storage ports, observability, security) is shared, and each domain is a tenant isolated by row-level security. Adding build insights in Phase 5 without touching the core is itself an acceptance test of the architecture.

## Out of scope
Facial recognition, people or plate identification, covert surveillance, audio capture, monitoring other people's property, and any public-facing camera streams.
