# User Stories: Embedded Panel Chatbot — Phase 1

**Source:** Confluence page "Embedded Panel Chatbot — Phase 1 Requirements" (pageId=1372618985)
**Requirements:** REQ-PANEL-01 through REQ-PANEL-17, NFR-1 through NFR-6
**Feature:** Embedded Panel Chatbot

---

## Definitions

- **Panel:** A right-side chatbot panel that slides in from the right edge of the viewport, pushing page content to the left.
- **Top-nav button:** A persistent button in the platform's top navigation bar (near the bell/notification icon) used to open/close the panel.
- **Context label:** A per-message label on each user message showing which platform page the prompt was sent from (e.g. "From: Device Management > Devices").
- **Home screen:** The panel view shown when there is no active thread — displays page-specific pre-canned prompts.
- **Full-page LITA:** The existing full-screen Lenovo IT Assist chatbot page, accessible via the platform dropdown navigation.

---

## Story 1: Panel entry point in top navigation

**Maps to:** REQ-PANEL-01, REQ-PANEL-16, REQ-PANEL-17

```gherkin
Feature: IT Assist panel button in top navigation bar

  As an IT Admin working on any page in Lenovo Device Orchestration
  I want a visible, persistent button in the top navigation bar to open the AI chatbot
  So that I can access AI assistance without navigating away from my current page

  Scenario: IT Assist button is visible on every platform page
    Given I am logged into Lenovo Device Orchestration
    When I navigate to any page (Dashboard, Device Management, Device Insights, Support Tickets, Configurations & Settings, Reports, App Management)
    Then I see the IT Assist button in the top navigation bar near the notification bell icon
    And the button displays the IT Assist / IQ branding icon
    And hovering over the button shows a tooltip "Open Lenovo IT Assist"

  Scenario: Button is hidden on the full-page LITA
    Given I am on the full-page Lenovo IT Assist page
    When the page loads
    Then the top-nav panel button is hidden or disabled
    And the chatbot is already in full view

  Scenario: First-use onboarding cue
    Given I am a user who has never opened the panel before
    When I land on any platform page for the first time after rollout
    Then the system displays a one-time onboarding cue on the IT Assist button (e.g. tooltip, callout, or pulse animation)
    And the cue informs me that AI assistance is available from any page
    And the cue is dismissible by clicking dismiss or by opening the panel

  Scenario: Onboarding cue does not reappear after dismissal
    Given I have dismissed the onboarding cue or opened the panel at least once
    When I navigate to any platform page
    Then the onboarding cue is not shown again
```

---

## Story 2: Open and close the panel

**Maps to:** REQ-PANEL-02, REQ-PANEL-03, REQ-PANEL-14

```gherkin
Feature: Open and close the right-side chatbot panel

  As an IT Admin
  I want to open the chatbot panel with one click and close it when I'm done
  So that I can quickly ask questions without losing my working context

  Scenario: Open the panel by clicking the top-nav button
    Given I am on any platform page
    And the panel is closed
    When I click the IT Assist button in the top navigation bar
    Then the panel slides in from the right side of the viewport
    And the page content shifts left to accommodate the panel
    And the panel displays the chatbot interface

  Scenario: Close the panel by clicking the top-nav button again
    Given the panel is open
    When I click the IT Assist button in the top navigation bar
    Then the panel slides out and closes
    And the page content shifts back to full width

  Scenario: Close the panel by clicking the close icon
    Given the panel is open
    When I click the close (X) icon in the panel header
    Then the panel slides out and closes
    And the page content shifts back to full width

  Scenario: Panel stays open when navigating to a different page
    Given the panel is open
    When I navigate to a different page in the platform (e.g. from Dashboard to Device Management)
    Then the panel remains open and visible on the new page
    And my active conversation persists in the panel

  Scenario: Panel is lazy-loaded on first open
    Given I am on any platform page and have not opened the panel in this session
    When the page loads
    Then the chat engine and thread data are not loaded
    And only the panel button shell is rendered
    When I click the IT Assist button for the first time
    Then the chat engine, thread data, and prompts are loaded
    And subsequent opens in the same session do not re-trigger the full load
```

---

## Story 3: Thread persistence and per-message context labels

**Maps to:** REQ-PANEL-04

```gherkin
Feature: Thread persistence with per-message page context labels

  As an IT Admin
  I want the panel to show my most recent conversation when I open it, with labels showing which page each message was sent from
  So that I can resume my conversation and understand its context across pages

  Scenario: Panel shows the most recent active thread on open
    Given I have an active thread with messages
    And the panel is closed
    When I open the panel
    Then the panel displays my most recent active thread
    And I can see previous messages and continue the conversation

  Scenario: Each user message shows a context label
    Given I have sent messages from different platform pages
    When I view the thread in the panel
    Then each user message displays a context label indicating the page it was sent from
    And the label format is "From: [Page Name]" (e.g. "From: Device Management > Devices")

  Scenario: Context label reflects the page at the time the message was sent
    Given I am on the Dashboard and send a message
    And I then navigate to Device Management and send another message
    When I view the thread
    Then the first message shows "From: Dashboard"
    And the second message shows "From: Device Management > Devices"

  Scenario: Thread persists across panel close and reopen
    Given I have an active thread with messages
    When I close the panel and later reopen it (on the same or different page)
    Then the same thread is displayed with all previous messages intact
```

---

## Story 4: New thread button ("+" button)

**Maps to:** REQ-PANEL-05

```gherkin
Feature: Start a new thread from panel header

  As an IT Admin
  I want to start a new conversation with one click
  So that I can begin a new topic without the previous context

  Scenario: "+" button creates a new thread
    Given I have an active thread in the panel
    When I click the "+" button in the panel header
    Then the current thread closes
    And a new thread is created (maintaining existing behaviour from full-screen LITA)
    And the panel shows the new empty thread ready for input

  Scenario: Previous thread is preserved in history
    Given I have started a new thread via the "+" button
    When I navigate to full-page LITA
    Then the previous thread appears in the thread history
    And I can switch back to it if needed

  Scenario: New thread behaviour matches existing full-screen LITA
    Given I click the "+" button in the panel
    When the new thread creation starts
    Then the behaviour is identical to the existing new thread creation in full-screen LITA
```

---

## ~~Story 5: Thread list in panel~~ — Moved to Phase 2

*(REQ-PANEL-07, REQ-PANEL-08 moved to Phase 2. Accessing historic threads from the right-side panel will be covered in Phase 2.)*

---

## Story 6: Navigate to full-page LITA from panel

**Maps to:** REQ-PANEL-06, REQ-PANEL-15

```gherkin
Feature: Navigate to full-page LITA from the panel

  As an IT Admin
  I want to open the full-page chatbot view from the panel
  So that I can use thread management features or work in a larger view when needed

  Scenario: Open full-page LITA from panel header link
    Given the panel is open with an active thread
    When I click the "open full view" icon/link in the panel header
    Then I am navigated to the full-page Lenovo IT Assist page
    And the full-page view shows the same active thread I was viewing in the panel

  Scenario: Full-page LITA remains accessible via dropdown navigation
    Given I am on any platform page
    When I open the platform navigation dropdown
    Then "Lenovo IT Assist" is listed as a navigation option
    And clicking it navigates me to the full-page LITA
```

---

## ~~Story 7: Page-specific pre-canned prompts~~ — Removed (covered in Phase 2)

*(REQ-PANEL-09, REQ-PANEL-10, REQ-PANEL-11 removed from Phase 1. Page-specific prompts and smart suggestions are covered in Phase 2 via "Ask IQ" context-aware features.)*

---

## Story 8: Full capability parity in panel

**Maps to:** REQ-PANEL-12, REQ-PANEL-13

```gherkin
Feature: Full chatbot capabilities in the panel

  As an IT Admin
  I want the panel chatbot to support all the same capabilities as the full-page chatbot
  So that I don't have to switch to the full-page view for any type of question or action

  Scenario: KB Q&A works in the panel
    Given the panel is open
    When I ask a knowledge base question (e.g. "How do I onboard a new Windows device?")
    Then I receive a KB response with text, images, and/or data tables
    And all content renders correctly within the panel width

  Scenario: Data insights work in the panel
    Given the panel is open
    When I ask a data insights question (e.g. "Show me device groups distribution")
    Then I receive a response with text and charts/visualisations
    And charts adapt to the panel width (e.g. adjusted aspect ratio)

  Scenario: Actions work in the panel
    Given the panel is open
    When I initiate an action (e.g. "Run a system scan on device XYZ")
    Then the action is executed and status is shown in the panel

  Scenario: Reasoning toggle works in the panel
    Given the panel shows a response with reasoning
    When I click "Show reasoning" or "Hide reasoning"
    Then the reasoning section expands or collapses within the panel

  Scenario: Smart suggestions appear after responses
    Given the panel shows a completed response
    Then follow-up prompt suggestions (recommendations) are displayed below the response

  Scenario: Response feedback works in the panel
    Given the panel shows a completed response
    When I click thumbs up or thumbs down
    Then my feedback is recorded

  Scenario: Rich content renders within panel width
    Given a response contains a wide data table
    When I view it in the panel
    Then the table is horizontally scrollable within the panel
    And no content is clipped or hidden without indication

  Scenario: In-progress state with stop/cancel
    Given I have sent a prompt and the response is being generated
    When I view the panel
    Then I see the "Processing your request…" indicator
    And a stop/cancel button is available to abort the request
```

---

## Story 9: Panel performance and responsive behaviour

**Maps to:** NFR-1, NFR-2, NFR-3, NFR-5

```gherkin
Feature: Panel performance and responsive behaviour

  As an IT Admin
  I want the panel to open quickly and not slow down my page
  So that AI assistance is fast and does not interfere with my work

  Scenario: Panel animation completes within 300ms
    Given I click the IT Assist button to open or close the panel
    When the panel animates in or out
    Then the animation completes within 300ms

  Scenario: Lazy loading completes within 2 seconds
    Given I open the panel for the first time in a session
    When the chat engine and thread data are loaded
    Then the panel is fully interactive within 2 seconds (P95)

  Scenario: Panel does not increase page load time
    Given I am on any platform page with the panel closed
    When the page loads
    Then the page load time is not increased by the panel's presence
    And only the button shell is rendered initially

  Scenario: Overlay mode on narrow viewports
    Given my viewport width is below 1024px
    When I open the panel
    Then the panel opens as an overlay instead of push
    And the page content is not shifted
```

---

## ~~Story 10: Panel accessibility~~ — Removed

*(NFR-4 removed from Phase 1 scope.)*

---

## NFRs (applied across stories)

| NFR | Description | Relevant stories |
|-----|-------------|-----------------|
| NFR-1 | Panel open/close animation ≤300ms | Story 9 |
| NFR-2 | Lazy loading ≤2s on first open (P95) | Story 9 |
| NFR-3 | No increase to page load time | Story 9 |
| NFR-5 | Overlay mode on viewports <1024px | Story 9 |

---

## Traceability summary

| Requirement | Story(ies) |
|-------------|------------|
| REQ-PANEL-01 | Story 1 |
| REQ-PANEL-02 | Story 2 |
| REQ-PANEL-03 | Story 2 |
| REQ-PANEL-04 | Story 3 |
| REQ-PANEL-05 | Story 4 |
| REQ-PANEL-06 | Story 6 |
| REQ-PANEL-07 | Moved to Phase 2 |
| REQ-PANEL-08 | Moved to Phase 2 |
| REQ-PANEL-09 | Removed (covered in Phase 2) |
| REQ-PANEL-10 | Removed (covered in Phase 2) |
| REQ-PANEL-11 | Removed (covered in Phase 2) |
| REQ-PANEL-12 | Story 8 (agentic workflows removed) |
| REQ-PANEL-13 | Story 8 |
| REQ-PANEL-14 | Story 2 |
| REQ-PANEL-15 | Story 6 |
| REQ-PANEL-16 | Story 1 |
| REQ-PANEL-17 | Story 1 |

---

## Jira field mapping (for publish_jira)

| Story element | Jira field |
|---------------|------------|
| Summary | **Summary** — prefix with `[Embedded Panel]` |
| Story narrative (As a … I want … So that …) | **ATDD - As Persona** |
| Acceptance criteria (Gherkin) | **ATDD - Acceptance Criteria** |
| Domain terms | **ATDD - Domain Terms** — use **"To do"** |
| Maps to requirement ID | **Description** |

---

**Status:** Draft ready for review. Run **Devil's Advocate** for review. After sign-off, use **publish_jira** to publish to Jira.
