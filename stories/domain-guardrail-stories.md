# Domain Guardrail — User Stories

**Feature short name:** [Domain Guardrail]  
**Confluence page:** https://confluence.tc.lenovo.com/pages/viewpage.action?pageId=1369342786  
**Persona:** IT Admin

---

## Story 1: Rules-based pre-generation blocking

**Maps to:** REQ-1

| Jira field | Content |
|------------|---------|
| **Summary** | [Domain Guardrail] Block obvious out-of-domain queries via rules before LLM call |
| **ATDD - As Persona** | As an IT Admin, I want obvious out-of-domain queries to be blocked by rules before any LLM call, so that we reduce cost and latency for clearly irrelevant requests. |
| **ATDD - Acceptance Criteria** | See Gherkin below |
| **ATDD - Domain Terms** | To do |
| **Description** | Maps to: REQ-1. Rules layer runs first in the classification pipeline. |

### Gherkin

```gherkin
Feature: Rules-based pre-generation domain blocking

  As an IT Admin
  I want obvious out-of-domain queries blocked by rules before any LLM call
  So that we reduce cost and latency for clearly irrelevant requests

  Scenario: Query matches out-of-domain rule
    Given the user submits a query that matches a configured out-of-domain rule
    When the rules layer evaluates the query
    Then the query is classified as OUT_OF_DOMAIN
    And no LLM call is made
    And the user receives the out-of-domain redirect message

  Scenario: Query does not match any out-of-domain rule
    Given the user submits a query that does not match any out-of-domain rule
    When the rules layer evaluates the query
    Then the query is passed to the next classification stage (lightweight classifier)
    And no LLM call has been made yet
```

---

## Story 2: Lightweight classifier for domain classification

**Maps to:** REQ-2

| Jira field | Content |
|------------|---------|
| **Summary** | [Domain Guardrail] Classify remaining queries via lightweight classifier; high-confidence out-of-domain redirects without LLM |
| **ATDD - As Persona** | As an IT Admin, I want remaining queries to be classified by a lightweight model, so that high-confidence out-of-domain queries are redirected without invoking the main LLM. |
| **ATDD - Acceptance Criteria** | See Gherkin below |
| **ATDD - Domain Terms** | To do |
| **Description** | Maps to: REQ-2. Runs after rules layer; only queries not blocked by rules reach this stage. |

### Gherkin

```gherkin
Feature: Lightweight classifier domain classification

  As an IT Admin
  I want remaining queries classified by a lightweight model
  So that high-confidence out-of-domain queries are redirected without invoking the main LLM

  Scenario: High-confidence out-of-domain from classifier
    Given a query passed from the rules layer (no rule match)
    When the lightweight classifier evaluates the query
    And the classifier returns OUT_OF_DOMAIN with high confidence
    Then no LLM call is made
    And the user receives the out-of-domain redirect message

  Scenario: High-confidence in-domain from classifier
    Given a query passed from the rules layer
    When the lightweight classifier evaluates the query
    And the classifier returns IN_DOMAIN with high confidence
    Then the query proceeds to Stage 2 capability routing
    And no LLM classification call is made

  Scenario: Low-confidence from classifier
    Given a query passed from the rules layer
    When the lightweight classifier evaluates the query
    And the classifier returns low confidence
    Then the query is passed to the LLM fallback for classification
```

---

## Story 3: LLM fallback for low-confidence classification

**Maps to:** REQ-3

| Jira field | Content |
|------------|---------|
| **Summary** | [Domain Guardrail] LLM fallback for low-confidence queries; structured classification before main LLM |
| **ATDD - As Persona** | As an IT Admin, I want low-confidence queries to be classified via a structured LLM call before the main generation, so that we only use the main LLM when the query is in-domain. |
| **ATDD - Acceptance Criteria** | See Gherkin below |
| **ATDD - Domain Terms** | To do |
| **Description** | Maps to: REQ-3. Invoked only for queries that pass rules and have low classifier confidence. |

### Gherkin

```gherkin
Feature: LLM fallback for low-confidence domain classification

  As an IT Admin
  I want low-confidence queries classified via a structured LLM call before main generation
  So that we only use the main LLM when the query is in-domain

  Scenario: LLM classifies as out-of-domain
    Given a query with low classifier confidence passed to the LLM fallback
    When the structured LLM classification call runs
    And the LLM returns OUT_OF_DOMAIN
    Then no main LLM generation call is made
    And the user receives the out-of-domain redirect message

  Scenario: LLM classifies as in-domain
    Given a query with low classifier confidence passed to the LLM fallback
    When the structured LLM classification call runs
    And the LLM returns IN_DOMAIN
    Then the query proceeds to Stage 2 capability routing
    And the main LLM is invoked only if needed for generation
```

---

## Story 4: Two-stage classification pipeline

**Maps to:** REQ-4

| Jira field | Content |
|------------|---------|
| **Summary** | [Domain Guardrail] Two-stage classification — domain check then capability routing |
| **ATDD - As Persona** | As an IT Admin, I want queries to go through a two-stage classification, so that we first check domain fit and then route to the right capability (KB, Data insights, Actions, Agentic). |
| **ATDD - Acceptance Criteria** | See Gherkin below |
| **ATDD - Domain Terms** | To do |
| **Description** | Maps to: REQ-4. Stage 1: IN_DOMAIN/OUT_OF_DOMAIN. Stage 2: KB, DATA_INSIGHTS, ACTIONS, AGENTIC, UNSUPPORTED. |

### Gherkin

```gherkin
Feature: Two-stage classification pipeline

  As an IT Admin
  I want queries to go through a two-stage classification
  So that we first check domain fit and then route to the right capability

  Scenario: Stage 1 returns OUT_OF_DOMAIN
    Given a user query
    When Stage 1 (domain check) returns OUT_OF_DOMAIN
    Then Stage 2 (capability routing) is not executed
    And the user receives the out-of-domain redirect message

  Scenario: Stage 1 returns IN_DOMAIN — Stage 2 routes to supported capability
    Given a user query
    When Stage 1 returns IN_DOMAIN
    And Stage 2 (capability routing) returns KB, DATA_INSIGHTS, ACTIONS, or AGENTIC
    Then the query is routed to the appropriate capability
    And the main LLM or agent handles the request

  Scenario: Stage 1 returns IN_DOMAIN — Stage 2 returns UNSUPPORTED
    Given a user query
    When Stage 1 returns IN_DOMAIN
    And Stage 2 returns UNSUPPORTED
    Then the user receives the in-domain out-of-capability redirect message
    And supported capabilities are listed
    And the user is invited to retry within scope
```

---

## Story 5: Out-of-domain redirect message

**Maps to:** REQ-5

| Jira field | Content |
|------------|---------|
| **Summary** | [Domain Guardrail] Out-of-domain redirect — clear message, no generation, no hint of future support |
| **ATDD - As Persona** | As an IT Admin, I want a clear message when my query is out-of-domain, so that I understand the scope without false expectations. |
| **ATDD - Acceptance Criteria** | See Gherkin below |
| **ATDD - Domain Terms** | To do |
| **Description** | Maps to: REQ-5. No generation attempt; no hint of future support. |

### Gherkin

```gherkin
Feature: Out-of-domain redirect message

  As an IT Admin
  I want a clear message when my query is out-of-domain
  So that I understand the scope without false expectations

  Scenario: User receives out-of-domain message
    Given the user submitted a query classified as OUT_OF_DOMAIN
    When the system responds
    Then the user sees a clear message that the query is outside the supported domain
    And no generation attempt is made
    And the message does not hint at or promise future support for the topic
```

---

## Story 6: In-domain out-of-capability redirect message

**Maps to:** REQ-6

| Jira field | Content |
|------------|---------|
| **Summary** | [Domain Guardrail] In-domain out-of-capability redirect — softer message, list capabilities, invite retry |
| **ATDD - As Persona** | As an IT Admin, I want a helpful message when my query is in-domain but not supported by any capability, so that I can retry with a supported use case. |
| **ATDD - Acceptance Criteria** | See Gherkin below |
| **ATDD - Domain Terms** | To do |
| **Description** | Maps to: REQ-6. Softer tone than out-of-domain; lists supported capabilities. |

### Gherkin

```gherkin
Feature: In-domain out-of-capability redirect message

  As an IT Admin
  I want a helpful message when my query is in-domain but not supported by any capability
  So that I can retry with a supported use case

  Scenario: User receives in-domain out-of-capability message
    Given the user submitted a query classified as IN_DOMAIN
    And Stage 2 capability routing returned UNSUPPORTED
    When the system responds
    Then the user sees a softer message than the out-of-domain case
    And the message lists the supported capabilities (KB, Data insights, Actions, Agentic workflows)
    And the user is invited to retry within scope
```

---

## Story 7: Classification observability

**Maps to:** REQ-7

| Jira field | Content |
|------------|---------|
| **Summary** | [Domain Guardrail] Log classification result, confidence, and path for tuning and auditing |
| **ATDD - As Persona** | As an IT Admin (or platform operator), I want classification results, confidence scores, and path taken to be logged, so that we can tune the system and audit decisions. |
| **ATDD - Acceptance Criteria** | See Gherkin below |
| **ATDD - Domain Terms** | To do |
| **Description** | Maps to: REQ-7. Path = rules / classifier / LLM. |

### Gherkin

```gherkin
Feature: Classification observability

  As an IT Admin (or platform operator)
  I want classification results, confidence scores, and path taken to be logged
  So that we can tune the system and audit decisions

  Scenario: Log when rules layer blocks query
    Given a query blocked by the rules layer
    When the classification completes
    Then the log includes the classification result (OUT_OF_DOMAIN)
    And the log includes the path taken (rules)
    And confidence is recorded as applicable (e.g. N/A or high for rules)

  Scenario: Log when classifier classifies query
    Given a query classified by the lightweight classifier
    When the classification completes
    Then the log includes the classification result
    And the log includes the confidence score
    And the log includes the path taken (classifier)

  Scenario: Log when LLM fallback classifies query
    Given a query classified by the LLM fallback
    When the classification completes
    Then the log includes the classification result
    And the log includes the confidence score
    And the log includes the path taken (LLM)
```

---

## Story 8: System prompt domain reinforcement

**Maps to:** REQ-8

| Jira field | Content |
|------------|---------|
| **Summary** | [Domain Guardrail] Enforce domain rules in system prompt as secondary layer |
| **ATDD - As Persona** | As an IT Admin, I want domain rules reinforced in the system prompt, so that even if a query slips through pre-generation checks, the LLM respects domain boundaries. |
| **ATDD - Acceptance Criteria** | See Gherkin below |
| **ATDD - Domain Terms** | To do |
| **Description** | Maps to: REQ-8. Secondary layer; primary blocking is pre-generation. |

### Gherkin

```gherkin
Feature: System prompt domain reinforcement

  As an IT Admin
  I want domain rules reinforced in the system prompt
  So that even if a query slips through pre-generation checks, the LLM respects domain boundaries

  Scenario: System prompt includes domain rules
    Given the main LLM or agentic workflow is invoked
    When the system prompt is constructed
    Then the system prompt includes domain rules (fleet management, IT assets)
    And the rules instruct the LLM to stay within scope
    And the rules instruct the LLM to decline out-of-domain requests
```

---

## Traceability Summary

| Requirement | Description | Story(ies) |
|-------------|-------------|------------|
| REQ-1 | Pre-generation domain classification (rules layer) | Story 1 |
| REQ-2 | Pre-generation domain classification (lightweight classifier) | Story 2 |
| REQ-3 | Pre-generation domain classification (LLM fallback) | Story 3 |
| REQ-4 | Two-stage classification | Story 4 |
| REQ-5 | Out-of-domain redirect | Story 5 |
| REQ-6 | In-domain out-of-capability redirect | Story 6 |
| REQ-7 | Observability | Story 7 |
| REQ-8 | System prompt reinforcement | Story 8 |

**Validation:**
- Every requirement (REQ-1 through REQ-8) has exactly one story.
- Every story maps to exactly one requirement.
- No gaps.

---

## Handover to Devil's Advocate

These drafted user stories are ready for review. Run the **Devil's Advocate** agent to challenge assumptions, find gaps, and stress-test the stories. After Devil's Advocate sign-off and your go-ahead, use the **publish_jira** agent to publish these stories to Jira.
