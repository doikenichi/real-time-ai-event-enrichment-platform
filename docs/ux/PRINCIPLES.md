# UX principles (Don Norman)

Every screen, alert, form and error message in the product follows Don Norman's human-centered design principles from *The Design of Everyday Things* (skill `human-centered-ux`). If people struggle, the design is at fault, not the user. The two qualities we design for are **discoverability** (what can I do, and how?) and **understanding** (what does this mean?).

## The principles, applied to Watchful and Build Insights
| Principle | Rule for this product | Example |
|---|---|---|
| **Affordances** | Interactive things are real controls (semantic HTML buttons and links) | "Mark as false alarm" is a `<button>`, not a clickable `<div>` |
| **Signifiers** | State and actions are labelled in words, with icons as support; never colour alone | `ServiceStatus` shows "Healthy" or "Unavailable" as text (Day 001); severity badges read "Alert", "Notable", "Info" |
| **Constraints** | Prevent invalid or unsafe actions instead of reporting them afterwards | You can't acknowledge a resolved incident; there's no zoom or identify action at all (privacy by design) |
| **Mapping** | The layout matches the real world | Cameras are grouped by zone (front, back, storage) in floor-plan order; timelines run in time order |
| **Feedback** | Every action and change gets an immediate, visible response | Optimistic acknowledgement in under 100 ms; a live-connection indicator; a "summary generating…" progress state |
| **Conceptual model** | One consistent model and vocabulary: **detection → incident → review** | The same glossary terms in the UI, the API, the docs and alerts |

## Gulfs of execution and evaluation
For each journey in [lean-inception.md](../product/lean-inception.md) (J1–J5), check:
- **Execution:** is the next action obvious, and is it the fewest steps? (J2: notification → snapshot → acknowledge takes 2 taps.)
- **Evaluation:** after acting, can the user tell what happened and what state things are in? (After "false alarm", the incident leaves the queue, with "Thanks: this improves future alerts".)

## Designing for error
- **Slips** (the right intent, a wrong click): offer **undo** for a few seconds rather than confirmation dialogs; keep destructive actions apart from frequent ones.
- **Mistakes** (a wrong mental model): show *why* the system acted ("Alert because a person was seen at night, then the back door opened").
- **Messages** say what happened, why, and what to do next, without blame. APIs return RFC 9457 problem details with an actionable `detail`.

## Alerts
Alarm fatigue is the core problem this product solves. Every alert states **what, where, when, how sure, why it matters, and what to do**. Alerts must be rare, explained and actionable, and every alert can be marked as a false alarm.

## Accessibility
WCAG 2.2 AA is part of done: role-based tests (Testing Library), axe-core in CI, keyboard operation, visible focus, contrast, and no information carried by colour alone.

## Checklist (reviews use it for every UI or alert change)
- [ ] Discoverable actions, clearly labelled (signifiers)
- [ ] Invalid actions prevented (constraints)
- [ ] Layout matches the real world and time order (mapping)
- [ ] Immediate feedback and visible state (feedback)
- [ ] Glossary terms used consistently (conceptual model)
- [ ] Undo for slips; explanations prevent mistakes; actionable messages
- [ ] Accessible (axe clean, keyboard, focus, not colour alone)
