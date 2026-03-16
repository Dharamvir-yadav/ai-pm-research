# User Stories: Auto-Rename Chat Threads

**Source:** Confluence page "Auto-Rename Chat Threads" (pageId=1367510517)  
**Requirements:** REQ-1 through REQ-12  
**Feature:** Auto-Rename Chat Threads

---

## Definitions

- **Thread:** A chat session/conversation in the fleet management chatbot.
- **Thread title:** The display name of a thread shown in session history.
- **Placeholder label:** Temporary label (e.g. "New conversation") shown until the auto-generated title is ready.
- **Manual rename:** The user explicitly changes the thread title via the UI.

---

## Story 1: Auto-generate thread title after first AI response

**Maps to:** REQ-1, REQ-2, REQ-3

```gherkin
Feature: Automatic thread title generation

  As an IT Admin using the fleet management chatbot
  I want the system to automatically generate a meaningful thread title after the first AI response
  So that I can identify and find conversations in my session history without manually naming them

  Scenario: Title is generated after first AI response in new session
    Given I have started a new chat session
    And I have sent my first prompt
    And the AI has returned its first response
    When the first AI response is complete
    Then the system automatically generates a thread title
    And the thread displays the generated title in session history

  Scenario: Template-based naming is used when intent and entities are extractable
    Given I have sent a prompt with clear intent and entities (e.g. "How do I update device PC-12345?")
    When the first AI response completes
    Then the system uses template-based naming (intent + entities) to generate the title
    And the title reflects the extracted intent and entities

  Scenario: LLM summarisation is used when template extraction fails
    Given the first user prompt cannot be parsed for intent and entities
    When the first AI response completes
    Then the system falls back to LLM summarisation to generate the title

  Scenario: Date-based fallback when both template and LLM fail
    Given both template-based naming and LLM summarisation fail
    When the first AI response completes
    Then the system uses a date-based fallback (e.g. "Chat – 2025-03-10")

  Scenario: Vague or very short prompts trigger fallback
    Given I have sent a vague or very short prompt (e.g. "help", "?")
    When the first AI response completes
    Then the system falls back to LLM summarisation or "Chat – {date}"
    And a meaningful or date-based title is displayed
```

---

## Story 2: PII sanitisation in thread titles

**Maps to:** REQ-4

```gherkin
Feature: PII sanitised from thread titles

  As the system
  I want PII (e.g. device serial numbers, usernames) sanitised from thread titles before generation and storage
  So that sensitive information is not exposed in session history or audit logs

  Scenario: Device serial numbers are sanitised before title generation
    Given the user prompt contains a device serial number (e.g. "PC-12345")
    When the thread title is generated
    Then the serial number is sanitised or redacted from the title
    And the title does not contain the raw serial number

  Scenario: Usernames are sanitised before title generation
    Given the user prompt contains a username (e.g. "john.doe@company.com")
    When the thread title is generated
    Then the username is sanitised or redacted from the title
    And the title does not contain the raw username

  Scenario: Sanitised titles are stored and displayed
    Given the user prompt contains PII
    When the thread title is generated and stored
    Then the stored and displayed title contains no PII
    And the sanitisation is applied before both generation and storage
```

---

## Story 3: Manual rename and respect user preference

**Maps to:** REQ-5, REQ-9

```gherkin
Feature: Manual rename and no auto-rename override

  As an IT Admin
  I want to manually rename a thread at any time
  So that I can use my own labels when the auto-generated title does not suit me

  Scenario: User can manually rename a thread at any time
    Given I have an existing chat thread (with or without an auto-generated title)
    When I choose to rename the thread via the UI
    Then I can enter a new title
    And the thread displays my chosen title

  Scenario: System does not auto-rename after manual rename
    Given I have manually renamed a thread
    When the system would otherwise generate or update a title (e.g. after more AI responses)
    Then the system does not overwrite my manually chosen title
    And the thread continues to display my manually chosen title

  Scenario: Auto-rename only applies to threads never manually renamed
    Given I have a thread that I have never manually renamed
    When the first AI response completes
    Then the system auto-generates the title
    And subsequent manual rename would prevent future auto-rename
```

---

## Story 4: Thread title length constraints

**Maps to:** REQ-6

```gherkin
Feature: Thread title length constraints

  As the system
  I want thread titles limited to 50–60 characters
  So that titles fit well in session history UI and remain readable

  Scenario: Generated titles are truncated to 50–60 characters
    Given the system generates a title (via template, LLM, or date fallback)
    When the generated title exceeds 60 characters
    Then the title is truncated to 50–60 characters
    And the truncated title is still meaningful (e.g. ends at word boundary)

  Scenario: Manual titles respect length limit
    Given I am manually renaming a thread
    When I enter a title exceeding 60 characters
    Then the system enforces the 50–60 character limit
    And I am informed or prevented from exceeding the limit

  Scenario: Short titles are not padded
    Given the generated or manual title is under 50 characters
    When the title is stored and displayed
    Then the title is displayed as-is without truncation or padding
```

---

## Story 5: Thread titles searchable and stored for audit

**Maps to:** REQ-7, REQ-8

```gherkin
Feature: Thread titles searchable and auditable

  As an IT Admin
  I want to search for threads by title in session history
  So that I can quickly find past conversations

  Scenario: Thread titles are searchable in session history
    Given I have multiple threads in my session history
    When I search within the session history (e.g. by keyword or filter)
    Then I can search by thread title
    And matching threads are returned

  Scenario: Thread titles are stored and logged for auditability
    Given a thread title is generated or manually set
    When the title is stored
    Then the title is persisted with the thread
    And the title (with PII redacted) is logged for audit purposes

  Scenario: Audit log contains redacted titles
    Given a thread title is stored
    When the audit log is written
    Then the logged title has PII redacted
    And the audit log supports traceability and compliance
```

---

## Story 6: Placeholder label and async title generation

**Maps to:** REQ-10, REQ-11

```gherkin
Feature: Placeholder label and non-blocking title generation

  As an IT Admin
  I want a placeholder label until the auto-generated title is ready
  So that I see a sensible default immediately and can continue using the chat

  Scenario: Placeholder label shown until auto-generated title is ready
    Given I have started a new chat session
    And I have sent my first prompt
    When the AI response is in progress or just completed
    Then the thread displays a placeholder label (e.g. "New conversation")
    And the placeholder is replaced by the auto-generated title when it is ready

  Scenario: Title generation runs asynchronously and does not block AI response
    Given I have sent my first prompt
    When the AI response is being generated
    Then the AI response is not delayed or blocked by title generation
    And title generation runs asynchronously in the background
    And the response is displayed to the user as soon as it is ready

  Scenario: Placeholder replaced by generated title when ready
    Given the placeholder "New conversation" is displayed
    When the auto-generated title becomes available
    Then the placeholder is replaced by the generated title
    And the transition is seamless (no user action required)
```

---

## Story 7: Thread title localisation

**Maps to:** REQ-12

```gherkin
Feature: Thread titles in user prompt language

  As an IT Admin using the chatbot in my preferred language
  I want thread titles generated in the language of my prompt
  So that the session history is consistent and readable in my language

  Scenario: Title generated in user prompt language
    Given I have sent my first prompt in a specific language (e.g. "Comment mettre à jour le firmware?")
    When the thread title is auto-generated
    Then the title is generated in the same language as my prompt
    And the title is displayed in that language in session history

  Scenario: Template-based naming respects prompt language
    Given my prompt is in a non-English language
    When template-based naming is used
    Then the title is generated in the same language as the prompt

  Scenario: LLM fallback uses prompt language
    Given my prompt is in a non-English language
    When LLM summarisation is used as fallback
    Then the title is generated in the same language as the prompt

  Scenario: Date-based fallback uses locale-appropriate format
    Given I have sent a vague prompt and date-based fallback is used
    When the title is generated
    Then the date format uses the user's locale or prompt language conventions
```

---

## Story 8: Accessibility of thread titles in session history

**Maps to:** NFR (Accessibility)

```gherkin
Feature: Thread titles accessible to screen readers

  As an IT Admin using assistive technology
  I want thread titles to be available to screen readers in session history navigation
  So that I can identify and navigate between conversations

  Scenario: Thread titles are exposed to screen readers in session history
    Given I am navigating session history with a screen reader
    When I focus on a thread in the list
    Then the thread title is announced by the screen reader
    And the title is associated with the correct thread (e.g. via aria-label or accessible name)

  Scenario: Placeholder label is accessible
    Given a thread displays the placeholder "New conversation"
    When I navigate with a screen reader
    Then the placeholder is announced
    And the thread is identifiable as a new conversation
```

---

## NFRs (applied across stories)

| NFR | Description | Relevant stories |
|-----|-------------|-----------------|
| Performance | Title generation must not add latency to the AI response; runs async | Story 6 |
| Cost | Template-based path adds negligible cost; LLM fallback uses lightweight model; total cost impact < 2% of conversation cost | Story 1 |
| Security / Privacy | PII sanitised from titles before storage and display; titles stored with audit log | Story 2, Story 5 |
| Accessibility | Thread titles available to screen readers in session history navigation | Story 8 |
| Localisation | Titles generated in the language of the user's prompt | Story 7 |

---

## Traceability summary

| Requirement | Story(ies) |
|-------------|------------|
| REQ-1 | Story 1 |
| REQ-2 | Story 1 |
| REQ-3 | Story 1 |
| REQ-4 | Story 2 |
| REQ-5 | Story 3 |
| REQ-6 | Story 4 |
| REQ-7 | Story 5 |
| REQ-8 | Story 5 |
| REQ-9 | Story 3 |
| REQ-10 | Story 6 |
| REQ-11 | Story 6 |
| REQ-12 | Story 7 |

- **Every requirement has at least one story:** Yes.
- **Every story has at least one requirement:** Yes.

---

## Jira field mapping (for publish_jira)

| Story element | Jira field |
|---------------|------------|
| Summary | **Summary** — prefix with `[Thread Rename]` |
| Story narrative (As a … I want … So that …) | **ATDD - As Persona** |
| Acceptance criteria (Gherkin) | **ATDD - Acceptance Criteria** |
| Domain terms | **ATDD - Domain Terms** — use **"To do"** |
| Maps to REQ-x | **Description** |

---

**Status:** Draft ready for review. Run **Devil's Advocate** agent for review. After sign-off, use **publish_jira** agent to publish to Jira.
