# Thumbs up / thumbs down feedback on chat responses

## Summary
Add lightweight thumbs up and thumbs down controls on each completed assistant chat message so IT Admins (and other chat users) can signal whether a response was helpful. Feedback is stored and used for quality and product decisions; thumbs down supports an optional inline reason (free text and/or predefined options).

## User problem / context
- **Who:** IT Admins and other users of the Gen AI chat (KB, Data insights, Actions, Agentic workflows).
- **Problem:** There is no lightweight way to signal whether a chat response was helpful. Without structured feedback, it is hard to improve models, prompts, or KB content or to prioritise quality work.
- **Context:** Feedback must be per assistant message only, low friction (one click for up/down), and non-blocking. Thumbs down can optionally capture a reason to support analysis.

## Requirements
List each requirement with a stable ID. Use these IDs in Jira stories (Maps to: REQ-TUD-01, …).

| ID     | Requirement description |
|--------|--------------------------|
| **REQ-TUD-01** | Thumbs up control on each completed assistant message; one click records positive feedback. |
| **REQ-TUD-02** | Thumbs down control on each completed assistant message; one click records negative feedback. |
| **REQ-TUD-03** | Optional reason for thumbs down (inline under message); free text and/or predefined options; dismiss = store thumbs down with no reason, submit = store reason. |
| **REQ-TUD-04** | Feedback stored with message/session id, user (or anonymous) id, vote, timestamp, optional reason; analysable by flow type and time. |
| **REQ-TUD-05** | After feedback is submitted for a message, the vote is final; UI shows submitted state and disables the other option. |
| **REQ-TUD-06** | Change of mind before submit: user can switch between up/down; only final state stored. |
| **REQ-TUD-07** | Errors/offline: best-effort send; show "Feedback couldn't be sent" and allow retry; non-blocking. |
| **REQ-TUD-08** | Thumbs and reason UI must be keyboard-accessible and screen-reader friendly. |

## Out of scope
- Star ratings or other rating schemes.
- Conversation-level feedback (only per-message).
- Feedback on user messages or during streaming.
- Mandatory reason for thumbs down.
- Automated retraining from this feedback data.

## NFRs (if any)
- **Accessibility:** Covered by REQ-TUD-08 (keyboard and screen-reader support).
- **Resilience:** Best-effort submission and retry (REQ-TUD-07) so feedback collection does not block the user.
- **Analysability:** Stored data (REQ-TUD-04) must support analysis by flow type and time for product and quality decisions.
