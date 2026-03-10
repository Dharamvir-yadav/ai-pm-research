# User Stories: Thumbs Up / Thumbs Down Feedback on Chat Response

**Source:** Requirements set (Confluence page skipped)  
**Requirements:** REQ-1, REQ-2, REQ-3, REQ-4, REQ-5, REQ-6, REQ-7, REQ-8  
**Status:** Draft for Devil's Advocate review. Do not publish to Jira until sign-off.

---

## Definitions

- **Assistant message:** One completed send unit in the chat UI (one bubble/card). For streaming, the whole completed response is one message. Feedback controls are attached to that single unit.
- **Submitted state:** Feedback is considered submitted when (a) thumbs up is clicked, or (b) thumbs down is clicked and the user either dismisses the reason step or submits the reason form.

---

## Story 1: Thumbs up control on completed assistant messages

**Maps to:** REQ-1

```gherkin
Feature: Thumbs up feedback on assistant message

  As an IT Admin (or chat user)
  I want a thumbs up control on each completed assistant message
  So that I can record positive feedback with one click

  Scenario: Thumbs up is visible and one-click records positive feedback
    Given I am viewing a conversation with at least one completed assistant message
    When I look at an assistant message
    Then I see a thumbs up control associated with that message
    And when I click the thumbs up control once
    Then my positive feedback is recorded for that message
    And I am not asked for a reason
```

---

## Story 2: Thumbs down control on completed assistant messages

**Maps to:** REQ-2

```gherkin
Feature: Thumbs down feedback on assistant message

  As an IT Admin (or chat user)
  I want a thumbs down control on each completed assistant message
  So that I can record negative feedback with one click

  Scenario: Thumbs down is visible and one-click records negative feedback
    Given I am viewing a conversation with at least one completed assistant message
    When I look at an assistant message
    Then I see a thumbs down control associated with that message
    And when I click the thumbs down control once
    Then my negative feedback is recorded for that message
```

---

## Story 3: Optional reason for thumbs down (inline; dismiss vs submit)

**Maps to:** REQ-3

```gherkin
Feature: Optional reason for thumbs down inline under message

  As an IT Admin who clicked thumbs down
  I want to optionally provide a reason inline under the message
  So that the team can understand why the response was not helpful, or dismiss without giving a reason

  Scenario: Reason UI is shown inline under the message after thumbs down
    Given I have clicked thumbs down on an assistant message
    When the negative feedback is recorded
    Then a reason capture UI is shown inline under that message (not in a modal)
    And I can provide free text and/or choose from predefined options
    And I can dismiss or submit

  Scenario: Dismiss stores thumbs down with no reason
    Given I have clicked thumbs down and the reason capture UI is visible
    When I dismiss the reason step (e.g. close, click away, or explicit "Skip")
    Then the system stores my thumbs down with no reason
    And the reason UI is closed

  Scenario: Submit stores thumbs down with reason
    Given I have clicked thumbs down and the reason capture UI is visible
    When I enter or select a reason (free text and/or predefined option)
    And I submit the reason form
    Then the system stores my thumbs down with the reason
    And the reason UI is closed
```

---

## Story 4: Feedback stored with message/session, user, vote, timestamp, optional reason

**Maps to:** REQ-4

```gherkin
Feature: Feedback persisted for analysis by flow type and time

  As the system
  I want to store each feedback event with message, session, user, vote, timestamp, and optional reason
  So that feedback is analysable by flow type and time

  Scenario: Stored payload includes required and optional fields
    Given a user has submitted feedback (thumbs up or thumbs down) for an assistant message
    When the feedback is persisted
    Then the record includes: message_id (or equivalent), session_id (or conversation_id), user_id (or anonymous id), vote (up/down), timestamp
    And if a reason was provided for thumbs down, the reason is stored with the record
    And the data is structured so it can be analysed by flow type and time
```

---

## Story 5: Vote is final after submit; UI shows submitted state and disables other option

**Maps to:** REQ-5

```gherkin
Feature: Final vote state after submission

  As an IT Admin who has submitted feedback for a message
  I want the vote to be final and the UI to reflect that
  So that I cannot accidentally change my feedback and the system state is clear

  Scenario: After feedback is submitted, vote is final and UI is locked
    Given I have submitted feedback (thumbs up or thumbs down, with or without reason) for an assistant message
    When I view that message again (same session or after refresh)
    Then the UI shows the submitted state (e.g. selected thumb, or "Feedback submitted")
    And the other option (thumbs down if I chose up, or thumbs up if I chose down) is disabled or hidden
    And I cannot change my vote for that message
```

---

## Story 6: Change of mind before submit — switch up/down; only final state stored

**Maps to:** REQ-6

```gherkin
Feature: Change vote before submission

  As an IT Admin who has not yet submitted feedback
  I want to switch between thumbs up and thumbs down
  So that only my final choice is stored

  Scenario: User can switch between thumbs up and thumbs down before submitting
    Given I am viewing an assistant message and have not yet submitted feedback
    When I click thumbs up
    Then my intent is not yet persisted (or only as draft)
    When I then click thumbs down (or vice versa)
    Then I can switch between up and down
    And no final vote is stored until I confirm (e.g. by leaving thumbs as-is or submitting reason)

  Scenario: Only final state is stored
    Given I have clicked thumbs down and the reason UI is visible
    When I change my mind and click thumbs up before submitting or dismissing
    Then the system does not store thumbs down
    And the system stores only my final choice (e.g. thumbs up) when that is submitted
```

---

## Story 7: Errors and offline — best-effort send, message, retry, non-blocking

**Maps to:** REQ-7

```gherkin
Feature: Resilient feedback submission (errors and offline)

  As an IT Admin giving feedback when the network or server fails
  I want best-effort send with a clear message and retry
  So that I am not blocked and can retry when connectivity returns

  Scenario: When submission fails, user sees message and can retry
    Given I have clicked thumbs up or thumbs down (or submitted a reason)
    When the submission fails (e.g. network error, offline, or server error)
    Then I see a clear message: "Feedback couldn't be sent"
    And I can retry the submission (e.g. "Retry" button or automatic retry when back online)
    And the feedback flow is non-blocking (I can continue using the chat)

  Scenario: Best-effort send does not block the UI
    Given I have triggered feedback submission
    When the submission is in progress or failing
    Then the UI remains responsive
    And I can continue reading or interacting with the conversation
```

---

## Story 8: Keyboard and screen-reader accessibility for thumbs and reason UI

**Maps to:** REQ-8

```gherkin
Feature: Accessible thumbs and reason UI

  As an IT Admin using keyboard or assistive technology
  I want the thumbs controls and reason UI to be keyboard-accessible and screen-reader friendly
  So that I can give feedback and provide a reason without a mouse

  Scenario: Thumbs controls are keyboard-accessible
    Given I am focused on or near an assistant message
    When I use the keyboard to navigate
    Then I can focus and activate the thumbs up and thumbs down controls
    And focus order is logical (e.g. message content, then thumbs up, then thumbs down)
    And each control has an accessible name (e.g. "Thumbs up", "Thumbs down")

  Scenario: Reason UI is keyboard-accessible and screen-reader friendly
    Given the optional reason UI is visible after thumbs down
    When I use the keyboard or screen reader
    Then I can focus and use the reason input(s) (predefined options and/or free text)
    And I can focus and activate submit and dismiss (e.g. "Skip" or close)
    And form fields and actions have appropriate labels and roles for screen readers
```

---

## Traceability summary

| Requirement | Story(ies) |
|-------------|------------|
| REQ-1 | Story 1 |
| REQ-2 | Story 2 |
| REQ-3 | Story 3 |
| REQ-4 | Story 4 |
| REQ-5 | Story 5 |
| REQ-6 | Story 6 |
| REQ-7 | Story 7 |
| REQ-8 | Story 8 |

- **Every requirement has at least one story:** Yes.
- **Every story has at least one requirement:** Yes.

---

## Out of scope (from requirements)

- Star ratings  
- Conversation-level feedback  
- Feedback on user messages  
- Mandatory reason for thumbs down  
- Automated retraining  

---

**Next step:** Run the **Devil's Advocate** agent to review these stories. After sign-off, use the **publish_jira** agent to publish to Jira.
