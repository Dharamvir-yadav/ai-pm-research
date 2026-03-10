# Devil's Advocate: Feedback on Chat Response – User Stories

**Source:** `stories/feedback-on-chat-response-stories.md`  
**Purpose:** Challenge assumptions, find gaps, argue against; stay constructive.

---

## Assumptions challenged

| Assumption | Why it might fail |
|------------|-------------------|
| **“Each assistant message” is a single bubble** | If the UI shows multi-message turns or streaming chunks, “one message” may be ambiguous. Users could rate the wrong unit or get confused about what they’re rating. |
| **Optional reason keeps friction low** | If most thumbs down have no reason, the signal may be too weak to act on. Teams may later push for mandatory reason and rework. |
| **Inline UI is always better than modal** | On very small screens or long threads, inline reason UI can push content down and feel cluttered; a small popover might be better. The stories don’t cover narrow viewports. |
| **Rate limiting / idempotency is enough for abuse** | A determined user could still thumbs down many different messages; rate limiting per message doesn’t stop that. No story covers “user can only give N pieces of feedback per session.” |
| **“IT Admin” is the only persona** | Other roles (e.g. read-only viewers, support) might use the same chat; accessibility and clarity of “who can give feedback” aren’t explicit. |

---

## Gaps

- **Thumbs up path:** No scenario for “user clicks thumbs up” (e.g. no double-submit, no reason asked). Minor but could leave thumbs-up behavior underspecified.
- **Change of mind:** No scenario for “user clicks thumbs down then wants to change to thumbs up” (or reverse). Product may need to decide: allow change, or lock after first vote.
- **Dismissing reason UI:** Story 2 says “dismiss/ignore” but doesn’t specify whether dismissing still sends “reason: none” or only the thumbs down. Affects analytics and storage.
- **Multi-device / refresh:** No scenario for “user gives feedback, then refreshes or switches device.” Idempotency (Story 6) helps, but “already submitted” state in the UI isn’t fully specified.
- **Error handling:** No scenario for “submit fails” (network, 4xx/5xx). User doesn’t know if feedback was saved; no retry or clear error message.
- **NFR – performance:** No explicit story for “feedback submission doesn’t block the UI” or “submission is async / non-blocking.”

---

## Counter-arguments

1. **Scope may be too narrow.** Limiting to “thumbs down + optional reason” might miss “report safety” or “wrong answer type” (e.g. hallucination vs outdated). Adding one more reason or a “Report” path later could mean reworking the reason list and analytics.
2. **Optional reason could undercut value.** If the goal is to improve answers, a high share of “thumbs down, no reason” may not be actionable. Making reason mandatory for thumbs down (or at least for “Other”) could improve signal at the cost of some friction.
3. **Storage and PII.** Storing `conversation_id` and feedback ties feedback to conversations. Depending on retention and who can access it, this could raise privacy/compliance questions. No story or NFR calls out data retention or access control.

---

## Recommendations

- **Clarify “message”:** Add a short definition (e.g. “one assistant message = one send unit in the UI”) in the Confluence page or a story so “each assistant message” is unambiguous.
- **Decide change-of-mind:** Add a scenario or out-of-scope note: “User cannot change vote after submitting” or “User can change vote until reason is submitted.”
- **Dismiss behavior:** In Story 2 or 4, specify: on dismiss, store `reason: null` (or equivalent) so analytics can separate “thumbs down only” from “thumbs down + reason.”
- **Error scenario:** Add one scenario (Story 2 or 4): “When submission fails, user sees a clear message and can retry or dismiss.”
- **Optional:** Consider one NFR scenario for “feedback submission is non-blocking” (e.g. spinner or optimistic UI, then confirm).

---

*Product owner decides whether to update the requirement page or stories based on this pass. Workflow can proceed to **publish_jira** after you’re satisfied.*
