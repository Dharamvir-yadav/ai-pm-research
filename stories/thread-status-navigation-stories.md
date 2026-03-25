# Thread Status Navigation — User Stories (Draft)

**Product**: Lenovo IT Assist | **Persona**: IT Admin

---

## Phase 1 — Frontend-only (within IT Assist)

### Story 1: [Thread Nav Status] Display Generating status on thread chips

**Maps to:** REQ-1, REQ-3, REQ-4, REQ-5

```gherkin
Feature: Thread chip Generating status indicator

  As an IT Admin
  I want to see a Generating status indicator on each thread chip in the sidebar when a response is being generated
  So that I can tell at a glance which threads are in progress without opening them

  Scenario: Generating status shown on thread chip during response generation
    Given I have a thread in the sidebar (Pinned or Recent)
    And a response is being generated in that thread (frontend streaming in progress)
    When I view the sidebar
    Then the thread chip displays a Generating status indicator
    And the indicator uses an animated visual (e.g. spinner or pulse icon)

  Scenario: Multiple threads show independent Generating status
    Given I have multiple threads in the sidebar
    And responses are being generated in more than one thread simultaneously
    When I view the sidebar
    Then each thread chip displays its own Generating status independently

  Scenario: Status is derived from frontend streaming connection state
    Given the frontend has an active streaming connection for a thread
    When the connection state indicates generation in progress
    Then the thread chip shows the Generating indicator
    And no additional backend API calls are made to determine status (in-module scenarios)

  Scenario: In-thread indicator remains unchanged
    Given I have a thread with a response being generated
    When I view the thread content area
    Then the existing "Processing your request…" indicator is still displayed
    And the thread chip status supplements it and does not replace it
```

**NFR:** NFR-1 — Phase 1 status indicator adds zero additional backend API calls.  
**NFR:** NFR-2 — Indicator is compact (icon/badge-sized); no layout shifts or thread chip height increase.  
**NFR:** NFR-3 — Status transitions (generating → done/error) reflect within 500ms of the actual state change.

---

### Story 2: [Thread Nav Status] Display Error status on thread chips

**Maps to:** REQ-2, REQ-8

```gherkin
Feature: Thread chip Error status indicator

  As an IT Admin
  I want to see an Error status indicator on a thread chip when response generation fails
  So that I can tell at a glance which threads need attention without opening them

  Scenario: Error status shown on thread chip when generation fails
    Given I have a thread in the sidebar
    And response generation failed mid-stream in that thread
    When I view the sidebar
    Then the thread chip displays an Error status indicator
    And the indicator uses a visually distinct treatment (e.g. red icon or dot)

  Scenario: Error state is informational only — no retry on chip
    Given a thread chip displays the Error status indicator
    When I view the thread chip in the sidebar
    Then the chip does not offer a retry action
    And I must open the thread to retry or take other action
```

**NFR:** NFR-3 — Status transitions (generating → error) reflect within 500ms of the actual state change.

---

### Story 3: [Thread Nav Status] Clear status when user stops generation

**Maps to:** REQ-6

```gherkin
Feature: Thread chip status clears on user stop

  As an IT Admin
  I want the thread chip status to clear when I stop a generation
  So that the sidebar accurately reflects the current state of each thread

  Scenario: Status clears when user stops generation
    Given a thread is generating a response
    And the thread chip shows the Generating indicator
    When I click the existing stop button to cancel the generation
    Then the thread chip status clears
```

---

### Story 4: [Thread Nav Status] Defer Generating indicator for fast responses

**Maps to:** REQ-7

```gherkin
Feature: No flash for fast responses

  As an IT Admin
  I want the Generating indicator to not flash for very fast responses
  So that I am not distracted by brief, unnecessary status changes

  Scenario: Generating indicator deferred for fast responses
    Given I have submitted a prompt in a thread
    When the response completes in under approximately 300ms
    Then the Generating indicator was not shown
    And no flash of the indicator occurred

  Scenario: Generating indicator shown after delay for slower responses
    Given I have submitted a prompt in a thread
    When the response takes longer than approximately 300ms to start streaming
    Then a short delay (~300ms) is applied before showing the Generating indicator
    And the indicator appears only after that delay elapses
```

**NFR:** NFR-3 — Status transitions reflect within 500ms of the actual state change.

---

## Phase 2a — Backend state persistence + cancel from chip

### Story 5: [Thread Nav Status] Backend exposes thread-level generation state

**Maps to:** REQ-9, REQ-12

```gherkin
Feature: Backend thread generation state

  As an IT Admin
  I want the backend to expose thread-level generation state
  So that status persists across panel reopen and page refresh

  Scenario: Thread list API includes generation state
    Given the backend has thread-level generation state (generating, completed, error)
    When the frontend requests the thread list
    Then the API returns generation state per thread (via thread list API or dedicated status endpoint)

  Scenario: Stale generating state is resolved after timeout
    Given a thread was in generating state
    When a reasonable timeout (TTL) elapses without completion
    Then the backend resolves the stale "generating" state
    And the state transitions to completed or error as appropriate
```

**NFR:** NFR-4 — Thread list API response time must not degrade significantly when generation_state is included.

---

### Story 6: [Thread Nav Status] Restore status on panel reopen or page refresh

**Maps to:** REQ-10

```gherkin
Feature: Status restored from backend on reopen or refresh

  As an IT Admin
  I want thread chip status to persist when I reopen the panel or refresh the page
  So that I can see which threads are still generating without losing context

  Scenario: Status displayed after panel reopen
    Given a thread was generating when I closed or navigated away from the IT Assist panel
    When I reopen the IT Assist panel
    Then the frontend fetches the thread list with generation state
    And the thread chip displays the appropriate status (Generating, Error, or none)

  Scenario: Status displayed after page refresh
    Given a thread was generating when I refreshed the page
    When the page reloads and IT Assist loads
    Then the frontend fetches the thread list with generation state
    And the thread chip displays the appropriate status
```

---

### Story 7: [Thread Nav Status] Cancel generation from thread chip in sidebar

**Maps to:** REQ-11

```gherkin
Feature: Cancel generation from thread chip

  As an IT Admin
  I want to cancel generation from the thread chip in the sidebar without opening the thread
  So that I can stop in-progress work quickly from the navigation

  Scenario: User cancels generation from thread chip
    Given a thread is generating a response
    And the thread chip shows the Generating indicator in the sidebar
    When I trigger cancel from the thread chip (e.g. stop icon or action on the chip)
    Then the generation is cancelled
    And the thread chip status clears
    And I did not need to open the thread to cancel
```

---

## Phase 2b — Completion notifications

### Story 8: [Thread Nav Status] Completion notification when response finishes in background thread

**Maps to:** REQ-13

```gherkin
Feature: Completion notification for background threads

  As an IT Admin
  I want to be notified when a response completes (or errors) in a thread I am not viewing
  So that I know when background work has finished without checking each thread

  Scenario: Notification shown when response completes in background thread
    Given I have multiple threads
    And I am viewing thread A
    And a response is generating in thread B (which I am not viewing)
    When the response in thread B completes
    Then a notification (badge or toast) is displayed within IT Assist
    And the notification indicates that a thread has completed

  Scenario: Notification shown when response errors in background thread
    Given I am viewing thread A
    And a response is generating in thread B
    When the response in thread B fails with an error
    Then a notification (badge or toast) is displayed within IT Assist
    And the notification indicates that a thread has errored
```

---

## Traceability Summary

| Requirement | Story(ies) |
|-------------|------------|
| REQ-1 | Story 1 |
| REQ-2 | Story 2 |
| REQ-3 | Story 1 |
| REQ-4 | Story 1 |
| REQ-5 | Story 1 |
| REQ-6 | Story 3 |
| REQ-7 | Story 4 |
| REQ-8 | Story 2 |
| REQ-9 | Story 5 |
| REQ-10 | Story 6 |
| REQ-11 | Story 7 |
| REQ-12 | Story 5 |
| REQ-13 | Story 8 |

| NFR | Story(ies) |
|-----|------------|
| NFR-1 | Story 1 |
| NFR-2 | Story 1 |
| NFR-3 | Story 1, Story 2, Story 4 |
| NFR-4 | Story 5 |

**Validation:** ✓ Every requirement (REQ-1 through REQ-13) is covered by at least one story. ✓ Every story maps to at least one requirement. ✓ Every NFR (NFR-1 through NFR-4) is covered. ✓ No gaps.
