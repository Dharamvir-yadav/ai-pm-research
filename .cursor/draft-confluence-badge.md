# Badge on Chat Icon (Response-Ready Notification) – Requirements

## Summary
A badge on the chat entry point (dropdown trigger or nav item) signals when a background response is ready. IT Admins can navigate away after submitting long-running queries and return when notified, improving productivity.

## User problem / context
IT Admins using the fleet management Gen AI chatbot sometimes submit long-running queries (e.g. data insights, agentic workflows). Currently the user must stay on the chat page and wait. There is no signal when the response is ready, causing frustration and lost productivity.

## Requirements
List each requirement with a stable ID. Use these IDs in Jira stories (Maps to: REQ-x).

| ID | Requirement description |
|----|--------------------------|
| REQ-1 | The chat entry point (dropdown trigger or nav item) displays a badge when there is at least one unviewed completed response. |
| REQ-2 | The badge shows a numeric count (1–9) or a capped indicator (e.g. "9+" or dot) when count ≥ 10. |
| REQ-3 | The badge has two visual states: ready (primary/blue) when all unviewed responses succeeded, and error/attention (red/warning) when any unviewed response failed. |
| REQ-4 | The badge appears when a background response completes and disappears when all completed responses have been viewed. |
| REQ-5 | The badge remains visible when the user opens the chat until each response is viewed (scrolled into view for a defined duration). |
| REQ-6 | A response is "viewed" when it has been scrolled into the viewport for a configurable duration while the chat is open. |
| REQ-7 | Unread/viewed state is stored server-side; the client fetches and syncs with the server. |
| REQ-8 | In-progress responses do not contribute to the badge count; only completed (success or error) responses count. |
| REQ-9 | Completed responses persist across browser close and reconnect; the badge reflects unviewed count on next load. |
| REQ-10 | Completed responses have a configurable TTL (e.g. 24–48 hours) after which they no longer count as unviewed for the badge. |
| REQ-11 | Badge updates are announced to screen readers (e.g. via aria-live="polite" and appropriate aria-label). |
| REQ-12 | Badge meets WCAG 2.1 AA contrast and does not rely on colour alone to indicate error state. |
| REQ-13 | Badge respects prefers-reduced-motion: reduce by avoiding or minimising animations. |
| REQ-14 | Badge logic is event-driven automation only; no AI is used for badge behaviour. |

## Out of scope
- Threading
- Toast/browser notifications
- Pending panels
- Content preview in badge

## NFRs (if any)
- **Performance:** Badge count should update within 2 seconds of response completion.
- **Accessibility:** WCAG 2.1 AA. Screen reader announcements via aria-live.
- **Security:** Badge shows only a count (no content); no PII exposed. Optional tenant policy for dot-only mode.
- **Automation vs AI:** Badge/notification mechanism is pure automation (event/polling). AI is used only for response generation.
