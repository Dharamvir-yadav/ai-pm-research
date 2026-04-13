# Thread Status Indicator — User Stories (Draft)

**Product**: Lenovo IT Assist | **Persona**: IT Admin  
**Maps to**: REQ-TSI-01 through REQ-TSI-10 | **NFRs**: NFR-1, NFR-2, NFR-3

---

## Story 1: [Thread Status] Display Generating status on thread chips

**Maps to:** REQ-TSI-01, REQ-TSI-03, REQ-TSI-04, REQ-TSI-06, REQ-TSI-09

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
    And the indicator is compact and does not add visual clutter to the sidebar

  Scenario: Multiple threads show independent Generating status
    Given I have multiple threads in the sidebar
    And responses are being generated in more than one thread simultaneously
    When I view the sidebar
    Then each thread chip displays its own Generating status independently

  Scenario: Status is driven by frontend streaming state
    Given the frontend has an active streaming connection for a thread
    When the connection state indicates generation in progress
    Then the thread chip shows the Generating indicator
    And no additional backend API calls are made to determine status

  Scenario: In-thread indicator remains unchanged
    Given I have a thread with a response being generated
    When I view the thread content area
    Then the existing "Processing your request…" indicator is still displayed
    And the thread chip status supplements it and does not replace it
```

**NFR scenarios:**
- **NFR-1 (Performance)**: Status indicator derives state from existing frontend streaming connection; no additional API calls or backend load.
- **NFR-2 (Visual footprint)**: Indicator is compact (icon/badge-sized); no layout shifts or increase in thread chip height.
- **NFR-3 (Responsiveness)**: Status transitions (generating → done) reflect within 500ms of the actual state change on the frontend.

---

## Story 2: [Thread Status] Display Error status on thread chips

**Maps to:** REQ-TSI-02, REQ-TSI-05

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

  Scenario: Error state is distinguishable from Generating state
    Given one thread is generating a response
    And another thread has a failed generation
    When I view the sidebar
    Then I can distinguish the Error state from the Generating state at a glance
```

**NFR scenarios:**
- **NFR-3 (Responsiveness)**: Status transition (generating → error) reflects within 500ms of the actual state change on the frontend.

---

## Story 3: [Thread Status] Clear status when user stops generation

**Maps to:** REQ-TSI-07

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
    And the chip reflects the resulting state (completed-partial or error) as appropriate
```

---

## Story 4: [Thread Status] Defer Generating indicator for fast responses

**Maps to:** REQ-TSI-08

```gherkin
Feature: No flash for fast responses

  As an IT Admin
  I want the Generating indicator to not flash for very fast responses
  So that I am not distracted by brief, unnecessary status changes

  Scenario: Generating indicator not shown for fast responses
    Given I have submitted a prompt in a thread
    When the response completes in under approximately 300ms
    Then the Generating indicator was not shown
    And no flash of the indicator occurred

  Scenario: Generating indicator shown after short delay for slower responses
    Given I have submitted a prompt in a thread
    When the response takes longer than approximately 300ms to start streaming
    Then a short delay is applied before showing the Generating indicator
    And the indicator appears only after that delay elapses
```

---

## Story 5: [Thread Status] Error state informational only on chip

**Maps to:** REQ-TSI-10

```gherkin
Feature: Error chip is informational only

  As an IT Admin
  I want the Error indicator on the thread chip to inform me that something went wrong
  So that I know to open the thread to investigate, without expecting retry from the chip

  Scenario: Error state has no retry action on chip
    Given a thread chip displays the Error status indicator
    When I view the thread chip in the sidebar
    Then the chip does not offer a retry action
    And I must open the thread to retry or take other action
    And the error state on the chip is informational only
```

---

## Traceability Summary

| Requirement | Story(ies) |
|-------------|------------|
| REQ-TSI-01 | Story 1 |
| REQ-TSI-02 | Story 2 |
| REQ-TSI-03 | Story 1 |
| REQ-TSI-04 | Story 1 |
| REQ-TSI-05 | Story 2 |
| REQ-TSI-06 | Story 1 |
| REQ-TSI-07 | Story 3 |
| REQ-TSI-08 | Story 4 |
| REQ-TSI-09 | Story 1 |
| REQ-TSI-10 | Story 5 |

| NFR | Story(ies) |
|-----|------------|
| NFR-1 | Story 1 |
| NFR-2 | Story 1 |
| NFR-3 | Story 1, Story 2 |

**Validation:** ✓ Every requirement (REQ-TSI-01 through REQ-TSI-10) is covered by at least one story. ✓ Every story maps to at least one requirement. ✓ No gaps.
