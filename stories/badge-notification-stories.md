# User Stories: Badge on Chat Icon (Response-Ready Notification)

**Source:** Confluence page "Badge on Chat Icon (Response-Ready Notification)" (pageId=1369343899)  
**Requirements:** REQ-1 through REQ-14  
**Feature:** Badge on Chat Icon (Response-Ready Notification)

---

## Definitions

- **Chat entry point:** The dropdown trigger or nav item that opens the chatbot.
- **Unviewed completed response:** A response that has finished (success or error) and has not yet been scrolled into the viewport for the configured duration while the chat is open.
- **Viewed:** A response is "viewed" when it has been scrolled into the viewport for a configurable duration (default: 1 second) while the chat is open.

---

## Story 1: Badge display on chat entry point when unviewed responses exist

**Maps to:** REQ-1, REQ-2

```gherkin
Feature: Badge visible on chat entry point

  As an IT Admin using the fleet management application
  I want the chat entry point to display a badge when there is at least one unviewed completed response
  So that I know when new responses are ready for me to view

  Scenario: Badge appears when unviewed completed response exists
    Given there is at least one unviewed completed response
    When I view the chat entry point (dropdown trigger or nav item)
    Then I see a badge on the chat entry point

  Scenario: Badge shows numeric count for 1 to 9 unviewed responses
    Given there are N unviewed completed responses where N is between 1 and 9
    When I view the chat entry point
    Then the badge displays the number N

  Scenario: Badge shows capped indicator when count is 10 or more
    Given there are 10 or more unviewed completed responses
    When I view the chat entry point
    Then the badge displays a capped indicator (e.g. "9+" or dot)
    And the exact count is not displayed
```

---

## Story 2: Badge visual states (ready vs error/attention)

**Maps to:** REQ-3

```gherkin
Feature: Badge visual states indicate response status

  As an IT Admin
  I want the badge to indicate whether all unviewed responses succeeded or any failed
  So that I can prioritise when there are errors to address

  Scenario: Badge shows ready state when all unviewed responses succeeded
    Given there is at least one unviewed completed response
    And all unviewed responses completed successfully
    When I view the chat entry point
    Then the badge displays in ready state (primary/blue)

  Scenario: Badge shows error state when any unviewed response failed
    Given there is at least one unviewed completed response
    And at least one unviewed response failed (error)
    When I view the chat entry point
    Then the badge displays in error/attention state (red/warning)
```

---

## Story 3: Badge lifecycle and viewed definition

**Maps to:** REQ-4, REQ-5, REQ-6

```gherkin
Feature: Badge appears and disappears based on response completion and viewing

  As an IT Admin
  I want the badge to appear when a background response completes and disappear when I have viewed all responses
  So that I am notified of new content without being overwhelmed by stale reminders

  Scenario: Badge appears when a background response completes
    Given I have no unviewed completed responses
    When a background response completes (success or error)
    Then the badge appears on the chat entry point

  Scenario: Badge disappears when all completed responses have been viewed
    Given there were unviewed completed responses
    When I have viewed all completed responses (scrolled into viewport for configured duration)
    Then the badge disappears from the chat entry point

  Scenario: Badge remains visible when chat is open until viewed
    Given there is at least one unviewed completed response
    When I open the chat
    Then the badge remains visible until each response is viewed

  Scenario: Response is viewed when scrolled into viewport for configured duration
    Given the chat is open and I have unviewed completed responses
    When I scroll a response into the viewport and it remains visible for the configured duration (default: 1 second)
    Then that response is marked as viewed
    And the badge count updates accordingly

  Scenario: Badge count updates within 2 seconds of response completion (NFR)
    Given I am viewing the chat entry point
    When a background response completes
    Then the badge count updates within 2 seconds
```

---

## Story 4: Server-side storage and sync of viewed state

**Maps to:** REQ-7, REQ-9

```gherkin
Feature: Viewed state persisted server-side and synced across sessions

  As the system
  I want unread/viewed state stored server-side with client sync
  So that badge state is consistent across sessions and devices

  Scenario: Viewed state is stored server-side
    Given a user has viewed a completed response (scrolled into viewport for configured duration)
    When the response is marked as viewed
    Then the viewed state is persisted on the server

  Scenario: Client fetches and syncs with server on load
    Given there are unviewed completed responses stored on the server
    When the user loads the application or reconnects
    Then the client fetches the unviewed count from the server
    And the badge reflects the correct count

  Scenario: Badge reflects unviewed count after browser close and reconnect
    Given there are unviewed completed responses
    When the user closes the browser and reopens the application
    Then the badge displays the correct unviewed count on next load

  Scenario: Badge stays consistent across concurrent open tabs
    Given the user has the application open in two browser tabs
    And there is at least one unviewed completed response
    When the user views the response in one tab (marked as viewed server-side)
    Then the badge updates in the other open tab to reflect the new unviewed count
```

---

## Story 5: Badge count rules (only completed responses)

**Maps to:** REQ-8

```gherkin
Feature: Badge counts only completed responses

  As the system
  I want only completed (success or error) responses to contribute to the badge count
  So that I do not show a badge for responses still in progress

  Scenario: In-progress responses do not contribute to badge count
    Given there are one or more responses in progress
    And no completed responses are unviewed
    When I view the chat entry point
    Then the badge does not appear or shows zero

  Scenario: Only completed responses count toward badge
    Given there are 2 completed unviewed responses and 1 in-progress response
    When I view the chat entry point
    Then the badge shows count 2
    And the in-progress response is not included in the count
```

---

## Story 6: Configurable TTL for unviewed responses

**Maps to:** REQ-10

```gherkin
Feature: Unviewed responses expire after configurable TTL

  As the system
  I want completed responses to have a configurable TTL after which they no longer count as unviewed
  So that old responses do not indefinitely inflate the badge

  Scenario: Unviewed responses expire after TTL
    Given unviewed completed responses exist
    And the configured TTL (e.g. 24–48 hours) has elapsed since completion
    When the badge count is calculated
    Then those expired responses no longer count as unviewed
    And the badge reflects only responses within the TTL window

  Scenario: TTL is configurable
    Given the system needs to support different retention policies
    When the TTL is configured (e.g. 24 or 48 hours)
    Then the badge uses that value to determine which responses count as unviewed

  Scenario: At TTL expiry the response remains in chat history but stops counting for the badge
    Given an unviewed completed response has passed the configured TTL
    When the badge count is calculated
    Then that response no longer counts as unviewed for the badge
    But the response is still visible in the chat history for the user to read
    And it is not automatically deleted from chat
```

---

## Story 7: Accessibility (screen reader, contrast, reduced motion)

**Maps to:** REQ-11, REQ-12, REQ-13

```gherkin
Feature: Accessible badge notification

  As an IT Admin using assistive technology or with visual or motion preferences
  I want the badge to be accessible and usable
  So that I can be notified of new responses regardless of how I interact with the UI

  Scenario: Badge updates are announced to screen readers
    Given the badge count or state changes
    When the update occurs
    Then the change is announced via aria-live="polite" and appropriate aria-label
    And the announcement conveys the count or state change

  Scenario: Badge meets WCAG 2.1 AA contrast
    Given the badge is displayed
    When I view the badge
    Then it meets WCAG 2.1 AA contrast requirements
    And the error state is not conveyed by colour alone
    And an additional indicator is present alongside colour (e.g. a "!" icon or distinct border on the badge)

  Scenario: Badge respects prefers-reduced-motion
    Given the user has prefers-reduced-motion: reduce set
    When the badge is displayed or updated
    Then animations are avoided or minimised
    And the badge remains functional without relying on motion
```

---

## NFRs (applied across stories)

| NFR | Description | Relevant stories |
|-----|-------------|-----------------|
| Performance | Badge count updates within 2 seconds of response completion | Story 1, Story 3, Story 4 |
| Security | Badge shows count only (no content); no PII exposed | Story 1, Story 4 |
| Automation vs AI | Badge/notification is pure automation; AI used only for response generation | All stories |

---

## Technical note: Badge logic is event-driven automation only (REQ-14)

> Badge behaviour is fully deterministic and event-driven — no AI is involved. Badge count and state are calculated from task completion events, viewed events, and TTL expiry. AI is used only for generating the response content, not for any badge or notification logic.
>
> Implementation guidance: use server-sent events, WebSocket, or polling to propagate completion events to the client. The `document.visibilityState` / Page Visibility API can be used to decide between in-app and browser notification (if added later).

---

## Traceability summary

| Requirement | Story(ies) |
|-------------|------------|
| REQ-1 | Story 1 |
| REQ-2 | Story 1 |
| REQ-3 | Story 2 |
| REQ-4 | Story 3 |
| REQ-5 | Story 3 |
| REQ-6 | Story 3 |
| REQ-7 | Story 4 |
| REQ-8 | Story 5 |
| REQ-9 | Story 4 |
| REQ-10 | Story 6 |
| REQ-11 | Story 7 |
| REQ-12 | Story 7 |
| REQ-13 | Story 7 |
| REQ-14 | Technical note (see below) |

- **Every requirement has at least one story or technical note:** Yes.
- **Every story has at least one requirement:** Yes.

---

## Jira field mapping (for publish_jira)

| Story element | Jira field |
|---------------|------------|
| Summary | **Summary** — prefix with `[Badge Notification]` |
| Story narrative (As a … I want … So that …) | **ATDD - As Persona** |
| Acceptance criteria (Gherkin) | **ATDD - Acceptance Criteria** |
| Domain terms | **ATDD - Domain Terms** — use **"To do"** |
| Maps to REQ-x | **Description** |

---

**Status:** Updated post Devil's Advocate review (R1–R5 applied). Ready for **publish_jira**.
