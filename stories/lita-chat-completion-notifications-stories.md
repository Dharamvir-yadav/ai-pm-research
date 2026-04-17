# User stories: LITA chat completion awareness (LDO + LITA)

**Requirements (Confluence):** [LITA chat completion awareness – Requirements](https://confluence.tc.lenovo.com/spaces/CGA/pages/1400997733/LITA+chat+completion+awareness+%E2%80%93+Requirements)  
**Research:** `research/lita-chat-completion-notifications-ldo-lita.md`  
**Jira project:** `GAI` (per `.cursor/defaults.md`). **Epic Link:** [GAI-7233](https://jira.tc.lenovo.com/browse/GAI-7233) *(Jira shows this Epic as “Test EPIC [DO NOT USE]” — move stories to your real Epic in Jira if 7233 was only for testing.)*

**Published:** Eight Stories linked to Epic **GAI-7233**. Format matches `.cursor/rules/04-story-format.mdc`: `Story` summary, `story narrative` with *As a* / *I want* / *So that*, one `gherkin Acceptance Criteria` table with one row per scenario.

---

## Traceability matrix

| Requirement ID | Jira story |
|----------------|------------|
| REQ-NTF-01 | [GAI-8017](https://jira.tc.lenovo.com/browse/GAI-8017) |
| REQ-NTF-02 | [GAI-8019](https://jira.tc.lenovo.com/browse/GAI-8019) |
| REQ-NTF-03 | [GAI-8023](https://jira.tc.lenovo.com/browse/GAI-8023) |
| REQ-NTF-04 | [GAI-8025](https://jira.tc.lenovo.com/browse/GAI-8025) |
| REQ-NTF-05 | [GAI-8029](https://jira.tc.lenovo.com/browse/GAI-8029) |
| REQ-NTF-06 | [GAI-8030](https://jira.tc.lenovo.com/browse/GAI-8030) |
| REQ-NTF-07 | [GAI-8033](https://jira.tc.lenovo.com/browse/GAI-8033) |
| REQ-NTF-08 | [GAI-8038](https://jira.tc.lenovo.com/browse/GAI-8038) |

---

## Story 1 — REQ-NTF-01

```Story
[LITA NTF] Trustworthy processing and done state in threads
```

```story narrative
*As a* IT admin using LITA  
*I want* “processing” and “finished” for my questions to reflect real system state tied to my thread  
*So that* when I switch pages or come back later, I am not misled by a screen-only spinner or out-of-date status
```

## Gherkin Acceptance Criteria

```
| *Scenario* | *Given* | *When* | *Then* |
|------------|---------|--------|--------|
| *Processing reflects real work* | I am in a thread and I send a prompt | LITA shows that my request is processing | The indicator is driven by server-backed status for my thread, not only a browser-side animation |
| *I see a clear finished or attention state* | My request has been running | The system reaches completed, failed, cancelled, or needs my input | I can see that outcome consistently in the conversation or thread list when I return |
```

**NFR:** Any “processing” or completion signal shown to me SHALL match server-authoritative transitions, not be inferred only in the browser.

**Maps to:** [REQ-NTF-01](https://confluence.tc.lenovo.com/spaces/CGA/pages/1400997733/LITA+chat+completion+awareness+%E2%80%93+Requirements#REQ-NTF-01)

---

## Story 2 — REQ-NTF-02

```Story
[LITA NTF] See run status across threads without staying put
```

```story narrative
*As a* IT admin  
*I want* to see which threads are still working and which have a new result without staying inside one chat  
*So that* I can work across threads and jump back to the right place when something finishes
```

```gherkin Acceptance Criteria
| Scenario | Given | When | Then |
|----------|-------|------|------|
| Thread list shows run status | I have more than one thread and at least one answer is still in progress | I look at the LITA thread list or sidebar | I can tell which threads are still running and which already have a completed or needs-attention result for me |
| Open the right thread for the result | A thread shows that a result is ready or needs my attention | I choose that thread | I land in the correct thread and see the outcome for that run |
```

**Maps to:** [REQ-NTF-02](https://confluence.tc.lenovo.com/spaces/CGA/pages/1400997733/LITA+chat+completion+awareness+%E2%80%93+Requirements#REQ-NTF-02)

---

## Story 3 — REQ-NTF-03

```Story
[LITA NTF] LDO tells me when LITA finishes elsewhere
```

```story narrative
*As a* IT admin  
*I want* Lenovo Device Orchestration to tell me when my LITA request finishes or needs me while I use another module  
*So that* I do not have to keep the LITA screen open to notice completion
```

```gherkin Acceptance Criteria
| Scenario | Given | When | Then |
|----------|-------|------|------|
| In-product heads-up when my run ends | I am signed in and I started a LITA request that is still running | That run reaches a finished or needs-attention state | At least one LDO surface (for example notification list, LITA entry badge, or a short banner) tells me in a way that applies only to me |
| I do not see other people’s work | Another admin in my org also has LITA activity | I look at those same LDO surfaces | I do not see their threads or completions mixed with mine |
```

**NFR — Accessibility:** Any toast or banner used for this SHALL follow our accessibility targets for live regions and keyboard use (for example WCAG 2.1 AA where we claim it).

**Maps to:** [REQ-NTF-03](https://confluence.tc.lenovo.com/spaces/CGA/pages/1400997733/LITA+chat+completion+awareness+%E2%80%93+Requirements#REQ-NTF-03)

---

## Story 4 — REQ-NTF-04

```Story
[LITA NTF] Safe wording outside the chat thread
```

```story narrative
*As a* IT admin in a regulated or sensitive environment  
*I want* alerts and lists outside the thread to avoid leaking fleet or incident detail by default  
*So that* DLP and privacy expectations are met when I get pings or emails
```

```gherkin Acceptance Criteria
| Scenario | Given | When | Then |
|----------|-------|------|------|
| Default off-thread text stays generic | My tenant uses the default strict setting for OS or email alerts | I get an out-of-thread completion alert | The text is generic (for example “Response ready in LITA”) and does not include sensitive fleet wording unless my tenant explicitly allows richer previews |
| In-app list follows the same rules | I open the LDO notification list or similar | I read a row about a LITA completion | The row follows the same minimization and preview rules as my tenant configuration |
```

**Maps to:** [REQ-NTF-04](https://confluence.tc.lenovo.com/spaces/CGA/pages/1400997733/LITA+chat+completion+awareness+%E2%80%93+Requirements#REQ-NTF-04)

---

## Story 5 — REQ-NTF-05

```Story
[LITA NTF] Optional email or device alert for completion
```

```story narrative
*As a* IT admin  
*I want* to turn on email or browser or OS alerts when my LITA request completes, when my org allows it  
*So that* I can notice completion even when I am away from LDO, without breaking policy
```

```gherkin Acceptance Criteria
| Scenario | Given | When | Then |
|----------|-------|------|------|
| No outbound alert when turned off | Push or email is turned off for me or my tenant | My LITA run completes | I do not get push or email; in-product cues may still apply |
| Same meaning as in-product when turned on | Push or email is allowed and I have consented where required | My run reaches a terminal state | The outbound message matches the same completion meaning as in LDO/LITA and still respects minimization rules |
```

**Maps to:** [REQ-NTF-05](https://confluence.tc.lenovo.com/spaces/CGA/pages/1400997733/LITA+chat+completion+awareness+%E2%80%93+Requirements#REQ-NTF-05)

---

## Story 6 — REQ-NTF-06

```Story
[LITA NTF] Stop matches what I see everywhere
```

```story narrative
*As a* IT admin  
*I want* Stop or Cancel to actually stop work and clear “running” everywhere it appears  
*So that* I do not trust a stale “still working” banner or badge after I have cancelled
```

```gherkin Acceptance Criteria
| Scenario | Given | When | Then |
|----------|-------|------|------|
| Cancel is reflected on the run | I have an in-flight request and I choose Stop or Cancel | The product accepts my cancel | Within the time we promise in product copy, my run is shown as cancelled (or equivalent), not still running |
| LITA and LDO stay in sync | LDO or LITA still shows that my run is in progress | Cancel has finished on the server | Thread status and LDO indicators no longer show that run as in progress |
```

**Maps to:** [REQ-NTF-06](https://confluence.tc.lenovo.com/spaces/CGA/pages/1400997733/LITA+chat+completion+awareness+%E2%80%93+Requirements#REQ-NTF-06)

---

## Story 7 — REQ-NTF-07

##Story **[LITA NTF] Failures and blocks look different from success**

```story narrative
*As a* IT admin
*I want* timeouts, policy blocks, and partial failures to show up in the same places as success, but clearly labeled
*So that* I do not assume a happy path when something went wrong or needs my input
```

|| Scenario || Given || When || Then ||
| *Failure is visibly not success* | My run ends in a defined failure state | I look at LITA thread status and LDO heads-up | I can tell it is not a normal successful completion |
| *Needs my input stands out* | My run stops because a guardrail or policy needs me | I look at the same awareness surfaces | I see wording or styling that means “needs your attention,” not the same as a simple “done” success |

**Maps to:** [REQ-NTF-07](https://confluence.tc.lenovo.com/spaces/CGA/pages/1400997733/LITA+chat+completion+awareness+%E2%80%93+Requirements#REQ-NTF-07)

---

## Story 8 — REQ-NTF-08

```Story
[LITA NTF] No spam from tokens or duplicate pings
```

```story narrative
*As a* IT admin  
*I want* completion pings only when something meaningful changes, not on every streaming tick  
*So that* my notification list and badges stay usable, including when I have more than one tab open
```

```gherkin Acceptance Criteria
| Scenario | Given | When | Then |
|----------|-------|------|------|
| No LDO ping per token | My answer is still streaming into the thread | The model sends more tokens | LDO-level badges or notifications are not raised for each token |
| One heads-up per real completion | I have two LDO tabs open | A single run reaches one terminal transition | I do not get duplicate completion signals for that same transition beyond what the product defines as acceptable |
```

**NFR — Cost / noise:** Fan-out and rate limits SHALL keep completion signals proportional to real state changes, not to internal streaming volume.

**Maps to:** [REQ-NTF-08](https://confluence.tc.lenovo.com/spaces/CGA/pages/1400997733/LITA+chat+completion+awareness+%E2%80%93+Requirements#REQ-NTF-08)
