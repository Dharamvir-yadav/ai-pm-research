# Response Feedback Enhancement — User Stories

**Confluence page:** [TEST: Created by Cursor — Response Feedback Enhancement – Requirements](https://confluence.tc.lenovo.com//pages/viewpage.action?pageId=1377146423)

---

## Story 1 — Structured negative feedback: reason panel and dismissal

**Maps to:** REQ-RF-01, REQ-RF-02

```gherkin
Feature: Structured negative feedback — reason panel after thumbs-down

  As an IT Admin
  I want to optionally tell IT Assist what went wrong after I thumbs-down a reply
  So that product teams can improve answers without forcing me through a long form

  Scenario: Panel shows five reason chips plus escape hatch
    Given I have received an assistant reply in a thread
    When I tap thumbs-down on that reply
    Then an inline "What went wrong?" panel is displayed
    And I see exactly these mutually exclusive reason chips: "Wrong or inaccurate", "Doesn't match my question", "Missing steps or details", "Too long or hard to follow", "Unsafe or I wouldn't do this"
    And I see a "Something else" escape hatch
    And at most one reason chip can be selected at a time

  Scenario: Thumbs-down without chip is valid feedback
    Given I have tapped thumbs-down on a reply
    When I do not select any chip and I dismiss or skip the panel
    Then negative feedback is still recorded as valid
    And I am not blocked from continuing the conversation

  Scenario: Panel is dismissible
    Given the "What went wrong?" panel is open
    When I press Escape, click outside the panel, or choose "Skip"
    Then the panel closes
    And my earlier thumbs-down remains valid per product rules

  Scenario: Chip panel renders quickly after tap
    Given I am viewing an assistant reply
    When I tap thumbs-down
    Then the reason panel begins rendering within 200 milliseconds (NFR-1)

  Scenario: Keyboard and screen reader access for panel
    Given the "What went wrong?" panel is open
    When I navigate with keyboard only
    Then all chips and controls are reachable in logical order
    And chips and actions have appropriate ARIA labels
    And the experience meets WCAG 2.1 AA for this flow (NFR-2)
```

---

## Story 2 — Optional improvement text after reason

**Maps to:** REQ-RF-03, REQ-RF-07

```gherkin
Feature: Optional free-text improvement after negative reason

  As an IT Admin
  I want to optionally add a short note after choosing a reason (or "Something else")
  So that I can clarify what to improve without mandatory typing

  Scenario: Text field appears after reason selection
    Given the "What went wrong?" panel is open
    When I select any reason chip or "Something else"
    Then I am shown an optional single-line field labelled along the lines of "Optional: what should we improve?"
    And I am not required to enter text to proceed

  Scenario: Submit without free text
    Given I have selected a reason or "Something else"
    And I have left the optional field empty
    When I submit feedback
    Then submission succeeds without requiring free text

  Scenario: Optional field respects tenant disablement
    Given my tenant has the optional comment field disabled in org settings
    When I complete the negative feedback flow after selecting a reason
    Then the optional text field is not shown
    And I can still submit structured feedback (REQ-RF-07A)

  Scenario: Keyboard and ARIA for optional field
    Given the optional improvement field is visible
    When I use keyboard and a screen reader
    Then the field has an accessible name and instructions
    And the control meets WCAG 2.1 AA (NFR-2)
```

---

## Story 3 — Submit acknowledgement and unsafe escalation copy

**Maps to:** REQ-RF-04

```gherkin
Feature: Feedback submit acknowledgement

  As an IT Admin
  I want immediate confirmation after I send negative feedback
  So that I know my input was received and I get appropriate guidance when safety is involved

  Scenario: Standard acknowledgement after submit
    Given I have submitted negative feedback (with or without optional text per rules)
    When the client accepts the submission as successful or queued
    Then I see a brief acknowledgement such as "Thanks — this helps us improve IT Assist"

  Scenario: Differentiated copy for Unsafe reason
    Given I selected the "Unsafe or I wouldn't do this" chip
    When I submit feedback
    Then the acknowledgement references internal escalation channels as defined in copy spec
    And the messaging is distinct from the standard acknowledgement

  Scenario: Submit feels instant
    Given I submit negative feedback from the panel
    When the action completes or is queued for retry
    Then the user-perceived submit completes within 300 milliseconds or shows queued state without blocking the UI unreasonably (NFR-1)

  Scenario: No silent loss on network failure
    Given I submit negative feedback
    When the network request fails transiently
    Then feedback is queued locally and retried (NFR-3)
    And I am informed appropriately if the UI cannot confirm delivery after retries per UX spec
```

---

## Story 4 — Server-side feedback event capture

**Maps to:** REQ-RF-05

```gherkin
Feature: Server-side metadata for each feedback event

  As a platform operator
  I want each feedback event stored with full correlation metadata
  So that analytics and investigations can tie feedback to messages, threads, and product context

  Scenario: Required fields stored on submit
    Given an IT Admin submits negative feedback for a message
    When the server ingests the event
    Then the record includes message ID, thread ID, response type (KB, insights, actions, or agents), selected chip(s) if any, timestamp, tenant/org ID, and app version
    And optional free text is stored when provided and allowed by policy

  Scenario: Thumbs-down only still creates auditable event
    Given an IT Admin thumbs-downed without selecting a chip and dismissed or skipped
    When the server records the event
    Then chip list reflects no structured reason or an agreed empty representation
    And other required metadata is still present

  Scenario: Retry does not duplicate events incorrectly
    Given the client retries a queued submission after network failure
    When the server receives duplicate or idempotent requests per API design
    Then feedback is not silently lost (NFR-3)
    And duplicate analytics inflation is prevented per idempotency rules
```

---

## Story 5 — PII redaction on free-text ingest

**Maps to:** REQ-RF-06

```gherkin
Feature: PII redaction on optional feedback text

  As a security-conscious organisation
  I want sensitive patterns stripped from free-text feedback before storage and reporting
  So that dashboards and exports minimise accidental PII exposure

  Scenario: Redaction at ingest before persistence
    Given optional free text is submitted with feedback
    When the platform ingests the text
    Then basic redaction is applied for emails, IP addresses, and common credential patterns before storage
    And redacted form is what appears in analytics drill-down and exports

  Scenario: Redaction applied before dashboard display
    Given stored feedback includes free text that was redacted at ingest
    When an authorised user views the feedback in the internal dashboard
    Then displayed text matches the redacted stored form

  Scenario: Retention aligns with tenant policy
    Given tenant data policy defines retention for free-text feedback
    When retention period elapses (default 90 days unless contract overrides)
    Then data handling follows configurable tenant retention (NFR-4)
```

---

## Story 6 — Tenant/org configuration for feedback UX

**Maps to:** REQ-RF-07

```gherkin
Feature: Tenant org-level feedback controls

  As a tenant administrator
  I want to control optional comment visibility and context attachment defaults
  So that our org policy is reflected in IT Assist feedback behaviour

  Scenario: Toggle optional comment field
    Given I manage org-level settings for IT Assist feedback
    When I disable the optional comment field
    Then users in my tenant do not see the free-text field in the negative feedback flow
    When I enable it
    Then eligible users see the field per Story 2 rules

  Scenario: Default for last user message and assistant reply attachment
    Given I configure the default for "Include last user message and assistant reply" attachment
    When the default is off
    Then new feedback submissions follow off unless user overrides per product rules
    When the default is on
    Then new submissions include that attachment per product rules
    And the setting is evaluated per tenant

  Scenario: Settings apply only within authorised tenant scope
    Given two different tenants exist
    When tenant A changes feedback configuration
    Then tenant B behaviour is unchanged
```

---

## Story 7 — Internal analytics dashboard (v0)

**Maps to:** REQ-RF-08, REQ-RF-06, NFR-5

```gherkin
Feature: Internal analytics dashboard for response feedback (v0)

  As an internal product or operations user
  I want to see aggregated negative feedback trends and drill down safely
  So that we can prioritise improvements and investigate issues

  Scenario: Feedback volume over time
    Given I am authorised for the feedback analytics dashboard
    When I open the v0 dashboard
    Then I can view feedback volume over time

  Scenario: Chip distribution and optional-comment rate
    Given feedback exists for the selected filters
    When I view the dashboard
    Then I see distribution of selected chips
    And I see optional-comment rate

  Scenario: Filters
    Given I use the dashboard filters
    When I filter by response type, feature area, app version, and tenant
    Then charts and tables reflect only matching feedback

  Scenario: Drill-down with redacted view
    Given I drill down to a conversation or thread
    When I view associated feedback detail
    Then free text and fields are shown in redacted form consistent with ingest rules (REQ-RF-06)

  Scenario: Dashboard accessibility
    Given I use keyboard and assistive technology on the dashboard
    Then primary controls and data regions meet WCAG 2.1 AA (NFR-2)

  Scenario: RBAC and break-glass for sensitive views
    Given I am not authorised for raw or security-flagged content
    When I attempt to access restricted views
    Then access is denied per RBAC (NFR-5)
    Given break-glass access is used for security-flagged items
    When full content is viewed under break-glass
    Then an audit log entry is recorded (NFR-5)
```

---

## Story 8 — Thumbs-up unchanged (V1 regression guard)

**Maps to:** REQ-RF-09

```gherkin
Feature: Thumbs-up feedback unchanged in V1

  As an IT Admin
  I want positive feedback to stay a single quick action
  So that I am not burdened when the answer helped

  Scenario: Single-tap thumbs-up with no expansion
    Given I view an assistant reply
    When I tap thumbs-up
    Then positive feedback is recorded as today
    And no expanded "what worked?" chip panel appears in V1
    And no new mandatory steps are introduced for thumbs-up

  Scenario: Thumbs-up does not open negative feedback panel
    Given I tap thumbs-up on a reply
    Then the structured negative feedback panel for thumbs-down is not shown
```

---

## Story 9 — Taxonomy validation with IT Admins

**Maps to:** REQ-RF-10

```gherkin
Feature: Validate negative-feedback taxonomy before final labels

  As a product owner
  I want real IT Admin input on reason labels using recent bad answers
  So that chip wording matches how admins think before we ship final copy

  Scenario: Structured validation sessions
    Given we have 5–10 IT Admins available for research
    And we have recent negative-response examples
    When we run validation sessions against the proposed taxonomy
    Then we capture fit, confusion, and missing categories

  Scenario: Labels adjusted from findings
    Given validation findings indicate label or taxonomy issues
    When we finalise requirements for implementation
    Then chip labels and grouping are updated to reflect findings before commit to final implementation
    And documentation and Story 1 acceptance criteria are updated to match agreed labels
```

---

## Traceability Matrix

| Requirement | Story(ies) | Covered? |
|-------------|------------|----------|
| REQ-RF-01 | Story 1 | Yes |
| REQ-RF-02 | Story 1 | Yes |
| REQ-RF-03 | Story 2 | Yes |
| REQ-RF-04 | Story 3 | Yes |
| REQ-RF-05 | Story 4 | Yes |
| REQ-RF-06 | Story 5, Story 7 | Yes |
| REQ-RF-07 | Story 2, Story 6 | Yes |
| REQ-RF-08 | Story 7 | Yes |
| REQ-RF-09 | Story 8 | Yes |
| REQ-RF-10 | Story 9 | Yes |

**NFR coverage:** NFR-1 → Stories 1, 3 | NFR-2 → Stories 1, 2, 7 | NFR-3 → Stories 3, 4 | NFR-4 → Story 5 | NFR-5 → Story 7

**No gaps — every requirement has at least one story, every story maps to at least one requirement.**
