# User Stories: Feedback on Chat Response (Final)

**Source:** Confluence requirement page "Feedback on Chat Response – Requirements"  
**Requirements:** REQ-FCF-01, REQ-FCF-02, REQ-FCF-03, REQ-FCF-04  
**Updated:** After Devil's Advocate pass; incorporates clarification of "message", change-of-mind rule, dismiss behavior, error handling, and non-blocking submission NFR.

---

## Definitions

- **Assistant message:** One send unit in the UI (one bubble/card that the user can point at). For streaming, the whole completed response is one message. Feedback controls are attached to that single unit.

---

## Story 1: Display thumbs up and thumbs down on assistant messages

**Maps to:** REQ-FCF-01

```gherkin
Feature: Thumbs up/down controls on assistant messages

  As an IT Admin (or other chat user) using the chat
  I want to see thumbs up and thumbs down controls on each assistant message
  So that I can indicate whether the response was helpful

  Scenario: Thumbs up and thumbs down are visible on each assistant message
    Given I am viewing a conversation with at least one assistant message
    When I look at an assistant message
    Then I see a thumbs up control
    And I see a thumbs down control
    And the controls are associated with that message only

  Scenario: Thumbs up is recorded without asking for a reason
    Given I am viewing an assistant message with thumbs up/down controls
    When I click the thumbs up control
    Then my positive feedback is recorded for that message
    And I am not asked for a reason

  Scenario: Controls are not shown on user messages
    Given I am viewing a conversation with user and assistant messages
    When I look at a message I sent (user message)
    Then I do not see thumbs up or thumbs down controls on that message
```

---

## Story 2: Thumbs down records feedback on first click and offers optional reason

**Maps to:** REQ-FCF-02

```gherkin
Feature: Thumbs down records feedback and offers optional reason

  As an IT Admin
  I want my thumbs down to be recorded immediately on first click
  So that my negative feedback is captured even if I do not provide a reason

  Scenario: Thumbs down is recorded on first click
    Given I am viewing an assistant message with thumbs up/down controls
    When I click the thumbs down control
    Then my negative feedback is recorded for that message
    And I see an optional second step to capture a reason inline under the message

  Scenario: Optional reason step is shown inline under the message
    Given I have just clicked thumbs down on an assistant message
    When the feedback is recorded
    Then a reason capture UI is shown inline under that message
    And I can choose to provide a reason or dismiss the reason step

  Scenario: Dismissing reason step stores thumbs down with no reason
    Given I have clicked thumbs down and the reason capture UI is visible
    When I dismiss the reason step (e.g. close or click away) without submitting a reason
    Then the system stores my thumbs down with reason null (or equivalent)
    And I see that my thumbs down was recorded (e.g. control remains in thumbs-down state)

  Scenario: Vote is final after submission
    Given I have submitted thumbs up or thumbs down for an assistant message
    When I view that message again (same session or after refresh)
    Then I cannot change my vote to the other option (vote is locked for that message)
    And the UI shows my submitted state (e.g. selected thumb, or "already submitted")

  Scenario: When feedback submission fails user can retry or dismiss
    Given I have clicked thumbs up or thumbs down
    When the submission fails (e.g. network error or server error)
    Then I see a clear error message (e.g. "Feedback could not be sent")
    And I can retry the submission or dismiss the message
```

---

## Story 3: Reason dropdown and optional free-text comment inline

**Maps to:** REQ-FCF-03

```gherkin
Feature: Reason selection and optional comment for thumbs down

  As an IT Admin who gave thumbs down
  I want to optionally select a reason from a predefined list and add a comment
  So that the team can understand why the response was not helpful

  Scenario: Predefined reason dropdown is shown inline
    Given I have clicked thumbs down and the optional reason step is visible
    When I view the reason capture UI
    Then I see a dropdown with options: Incorrect, Incomplete, Not relevant, Unclear, Other
    And the UI is inline under the assistant message

  Scenario: Optional free-text comment can be provided
    Given I am in the reason capture UI under the message
    When I have selected a reason (or "Other")
    Then I can optionally enter a free-text comment
    And I can submit reason and comment or submit with reason only

  Scenario: Submitting reason and comment
    Given I have selected a reason and optionally entered a comment
    When I submit the reason form
    Then the reason and comment (if provided) are saved and associated with my thumbs down feedback
```

---

## Story 4: Store feedback payload (message_id, conversation_id, feedback_type, timestamp, reason, comment)

**Maps to:** REQ-FCF-04

```gherkin
Feature: Persist feedback with required and optional fields

  As the system
  I want to store each feedback event with message and conversation context
  So that feedback can be analyzed and traced to specific messages and conversations

  Scenario: Thumbs down is stored with required fields
    Given a user has clicked thumbs down on an assistant message
    When the feedback is recorded
    Then the system stores: message_id, conversation_id, feedback_type (e.g. thumbs_down), timestamp
    And the record is persisted so it can be retrieved later

  Scenario: Reason and comment are stored when provided; reason null when dismissed
    Given a user has given thumbs down and optionally provided a reason and/or comment
    When the user submits the reason form
    Then if reason was provided, it is stored with the feedback record
    And if comment was provided, it is stored with the feedback record
    And the record remains linked to the same message_id and conversation_id
  When the user dismisses the reason form without submitting
  Then the system stores the thumbs down with reason null (or equivalent)
  So that analytics can separate "thumbs down only" from "thumbs down with reason"

  Scenario: Thumbs up is stored with required fields only
    Given a user has clicked thumbs up on an assistant message
    When the feedback is recorded
    Then the system stores: message_id, conversation_id, feedback_type (e.g. thumbs_up), timestamp
    And no reason or comment is stored
```

---

## Story 5: Accessibility, inline UX, and non-blocking submission

**Maps to:** REQ-FCF-01, REQ-FCF-02, REQ-FCF-03 (inline UX and accessibility NFRs)

```gherkin
Feature: Accessible and inline feedback controls

  As an IT Admin, including one using assistive technology
  I want the feedback controls to be keyboard accessible and clearly associated with the message
  So that I can give feedback regardless of how I interact with the UI

  Scenario: Feedback controls are keyboard accessible
    Given I am focused on or near an assistant message
    When I use the keyboard to reach the thumbs up/down controls
    Then I can focus and activate both controls without a mouse
    And focus order is logical (e.g. message content then thumbs up then thumbs down)

  Scenario: Reason UI is inline and does not obscure the message
    Given the optional reason step is shown after thumbs down
    When I view the reason dropdown and comment field
    Then they appear inline under the message (e.g. below the message, not in a modal overlay that hides the message)
    And the reason UI is keyboard accessible and has appropriate labels for screen readers

  Scenario: Feedback submission does not block the UI
    Given I have clicked thumbs up or thumbs down (or submitted a reason)
    When the submission is in progress
    Then the UI remains responsive (e.g. optimistic update or brief spinner)
    And I can continue reading or interacting with the conversation
    And I see a clear confirmation when submission succeeds (or an error if it fails)
```

---

## Story 6: Rate limiting and already-submitted state

**Maps to:** REQ-FCF-04 (NFR: rate limiting)

```gherkin
Feature: Rate limiting and idempotent feedback submission

  As the system
  I want to apply rate limiting to feedback submissions and show already-submitted state
  So that abuse or accidental repeated submissions do not overload storage or APIs

  Scenario: Repeated thumbs down on same message is idempotent or rate limited
    Given a user has already submitted thumbs down for a message
    When the user attempts to submit thumbs down again for the same message (or reason/comment again)
    Then the system either treats it as idempotent (no duplicate record) or applies rate limiting
    And the UI or API responds in a predictable way (e.g. no error spam, or clear "already submitted" state)

  Scenario: Already submitted state is visible after refresh or revisit
    Given a user has submitted thumbs up or thumbs down for an assistant message
    When the user refreshes the page or returns to the conversation later
    Then the UI shows that feedback was already submitted for that message (e.g. selected thumb, read-only)
    And the user cannot submit a second vote for the same message
```

---

## Traceability summary

| Requirement | Story(ies) |
|-------------|------------|
| REQ-FCF-01 | Story 1, Story 5 |
| REQ-FCF-02 | Story 2, Story 5 |
| REQ-FCF-03 | Story 3, Story 5 |
| REQ-FCF-04 | Story 4, Story 6 |

- **Every requirement has at least one story:** Yes.
- **Every story has at least one requirement:** Yes.

---

## Out of scope (from Devil's Advocate)

- **Change of mind:** User cannot change vote after submitting (thumbs down → thumbs up or vice versa); vote is locked for that message. Documented in Story 2.
- **Data retention / access control:** Not in scope for this set of stories; may be addressed in a separate NFR or policy.

---

**Status:** Final. Ready for **publish_jira** (Epic link and "Maps to:" each requirement ID, e.g. REQ-FCF-01, in each story).
