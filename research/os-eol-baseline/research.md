# Research: OS Version EOL Baselining & At-Risk Device Identification

## Research topic

Agentic feature to keep fleet OS versions baselined to a version that is not reaching end-of-life (EOL) within 6 months. Surface devices running Windows subversions (e.g. Windows 10 22H2, Windows 11 23H2) approaching EOL so IT admins can act proactively. Account for real-world upgrade blockers — stale drivers, hardware incompatibility, application conflicts.

**Scope:** Windows only (macOS out of scope). Lenovo Device Orchestration is already integrated with Microsoft Intune — the feature should leverage Intune as the primary data source for device inventory and driver/upgrade readiness.

**Phasing:**
- **Phase 1:** Ingest EOL lifecycle KB + support user queries about which devices are approaching OS EOL. Pure intelligence layer.
- **Phase 2:** Add device upgrade readiness — driver compatibility, hardware blockers, actionable upgrade/remediation workflows.

---

## 1. The Problem — Seen Through the IT Admin's Eyes

An IT admin managing a fleet of hundreds or thousands of Lenovo devices faces a quiet, compounding risk: **devices silently drifting into unsupported OS versions**. Once a Windows subversion (e.g. 22H2) or a macOS release (e.g. Ventura) passes its end-of-servicing date, the device stops receiving security patches. The admin may not notice until a compliance audit flags it — or worse, a breach exploits an unpatched vulnerability.

**What makes this hard today:**

- **Fragmented lifecycle data.** Microsoft publishes EOL dates per edition (Home, Pro, Enterprise, Education, LTSC) and per subversion. Apple doesn't publish official EOL schedules at all. Admins must manually track dates across multiple Microsoft Learn pages, Apple security update pages, and third-party trackers.
- **Subversion granularity.** It's not enough to know "Windows 11 is supported." Windows 11 22H2 Enterprise ends servicing October 14, 2025, while 24H2 Enterprise runs to October 12, 2027. A fleet on 22H2 looks current but is months from losing security updates.
- **Upgrade is not a click.** Stale drivers, incompatible third-party software (e.g. SentinelOne, Intel SST audio drivers), hardware limitations (TPM 2.0, CPU generation), and OEM firmware gaps can block or break upgrades. 82% of enterprise Windows endpoints had not migrated to Windows 11 as of mid-2024 (ControlUp study), with 11% requiring full hardware replacement.
- **No single pane of glass.** ServiceNow ITAM requires custom reporting to get asset-level EOL views. Intune enforces minimum versions but doesn't proactively surface "at-risk within N months" lists. Tanium and Ivanti have compliance baselines but don't combine lifecycle intelligence with readiness assessment in one workflow.

**The admin's expression:** "I need to know which devices are going to become unsupported *before* it happens, and whether I can actually upgrade them — not just that they're non-compliant after the fact."

---

## 2. Windows OS Version Lifecycle — Current State

### Major version EOL

| OS | End of support | Notes |
|----|---------------|-------|
| Windows 10 (all editions) | **Oct 14, 2025** | End of security updates. ESU programme available at cost. |
| Windows 10 Enterprise LTSC 2021 | Jan 12, 2027 | Extended support. |
| Windows 11 Enterprise LTSC 2024 | Oct 9, 2029 | Longest current support window. |

### Windows 11 subversion EOL (Enterprise & Education)

| Subversion | GA date | End of servicing |
|-----------|---------|-----------------|
| 21H2 | Oct 4, 2021 | Oct 8, 2024 (passed) |
| 22H2 | Sep 20, 2022 | **Oct 14, 2025** |
| 23H2 | Oct 31, 2023 | **Nov 10, 2026** |
| 24H2 | Oct 1, 2024 | Oct 12, 2027 |
| 25H2 | Sep 30, 2025 | Oct 10, 2028 |
| 26H1 | Feb 10, 2026 | Mar 13, 2029 |

**Home & Pro editions have shorter servicing windows** (typically 24 months vs 36 months for Enterprise/Education). The baseline policy must account for edition-specific dates.

### macOS lifecycle

| Version | Release | Approx. EOL |
|---------|---------|-------------|
| macOS 13 Ventura | Oct 2022 | Sep 2025 (ended) |
| macOS 14 Sonoma | Sep 2023 | Sep 2026 |
| macOS 15 Sequoia | Sep 2024 | ~Jan 2028 |
| macOS 26 Tahoe | Sep 2025 | ~2028 |

Apple does not publish official EOL dates; they are inferred from the pattern of ~3 years of support per release. This uncertainty is a design consideration — the system should flag "estimated" vs "confirmed" EOL dates.

---

## 3. Lifecycle Data Sources (Programmatic)

| Source | Type | Coverage | Notes |
|--------|------|----------|-------|
| **Microsoft Graph API** (Windows updates) | Official API | Windows versions, editions, known issues | Launched Apr 2024 (beta). Provides servicing periods, EOL dates by edition. Requires `Device.Read.All` / `WindowsUpdates.ReadWrite.All`. |
| **endoflife.date API** | Open-source, community-maintained | 300+ products incl. Windows, macOS, Linux distros | Free, well-structured JSON API. Good fallback / cross-reference. Not vendor-official. |
| **Microsoft Lifecycle Policy page + export** | Official, manual/scrape | All Microsoft products | learn.microsoft.com/en-us/lifecycle — supports CSV export. |
| **Apple security updates page** | Unofficial pattern inference | macOS releases | No API. Dates inferred from when Apple stops issuing security patches. |

**Recommendation:** Primary source for Windows = Microsoft Graph API. Cross-reference with endoflife.date for macOS, Linux, and as a fallback. Flag any date sourced from community data as "estimated."

---

## 4. Competition & Market Scan

| Product | What they do | How | Relevance |
|---------|-------------|-----|-----------|
| **Microsoft Intune** | Enforces min/max OS version compliance. Blocks access via Conditional Access if non-compliant. | Compliance policies + enrollment restrictions. Grace period for remediation. Intune Compatibility Reports assess driver/app risk before feature updates. | Reactive enforcement (blocks *after* non-compliance). Does not proactively surface "at-risk in N months" devices. No integrated EOL countdown. Strong driver compatibility assessment via readiness reports. |
| **ServiceNow ITAM** | EOL/EOS tracking via `sam_sw_product_lifecycle` and `cmdb_hardware_model_lifecycle` tables. | Requires custom reports to join asset data with lifecycle data. Out-of-box reporting is model-level, not asset-level. | Data exists but **reporting is weak out-of-box**; admins manually query. No proactive alerting. No upgrade-readiness assessment. |
| **Tanium** | Real-time endpoint visibility. Can query any endpoint attribute including OS version. Compliance baselines. | Tanium's natural-language questions can surface device counts by OS version. Compliance modules flag deviations. | Strong data collection but **no built-in EOL lifecycle intelligence**. Admin must know EOL dates and build queries manually. |
| **Ivanti Neurons / Endpoint Security** | Mandatory Baseline feature. Defines minimum content requirements per group. Auto-remediation. | Policy-based enforcement with inheritance across groups. Checks OS version, patch level, AV, encryption. | Closest to "baseline" concept. But **baseline is static** — admin must update it when EOL dates change. No lifecycle-aware automation. |
| **Freshservice (Freshworks)** | Asset lifecycle management. Discovery and inventory. Alert rules. | Freddy AI provides recommendations. Asset normalization. Lifecycle stages tracked. | Limited evidence of subversion-level EOL tracking. General lifecycle management, not OS-version-specific. |
| **Fleet (FleetDM)** | Open-source. OS update enforcement via policies (osquery). Automated script execution on policy failure. | Infrastructure-as-code policies. GitOps workflow for baseline management. Supports macOS, Windows, Linux. | Good automation model (policy → detect → remediate). But **no EOL lifecycle intelligence built in** — policies are version-specific and manually defined. |
| **ManageEngine** | Endpoint Central provides OS deployment and patch management. Software lifecycle tracking. | Agent-based discovery + patch deployment. Reports on OS distribution. | General patch management. Limited evidence of proactive EOL-based alerting at subversion level. |

**Key gap across all competitors:** No product combines (1) lifecycle-aware EOL intelligence at the subversion level, (2) proactive "at-risk" surfacing with configurable time horizons, and (3) upgrade-readiness assessment (driver/hardware/app compatibility) in a single workflow. Most are either reactive (flag after non-compliance) or require manual lifecycle tracking.

---

## 5. Upgrade Blockers — The Real-World Complexity

### 5a. Stale / incompatible drivers

This is the highest-risk upgrade blocker in practice.

- **Intel Smart Sound Technology (SST) audio drivers** caused BSODs on 11th-gen Intel devices during Windows 11 24H2 upgrades. Required specific driver version updates (10.29.00.5714+). Microsoft applied safeguard holds to block affected devices.
- **WD NVMe drivers** caused boot failures during 24H2 upgrades.
- **OEM-specific display/audio/fingerprint drivers** frequently lag behind new OS versions. Lenovo devices ship with Lenovo-customized drivers that may not be immediately updated for new Windows feature releases.
- The new Windows "checkpoint" servicing model (introduced 24H2) broke assumptions in third-party middleware that hooked into low-level servicing paths.

**Implication for the feature:** A "devices at risk" list that doesn't account for driver readiness will generate false positives ("upgrade this device") that fail on execution. The system should either (a) integrate with readiness assessment data (Intune compatibility reports, Windows Setup `CompatData*.xml` scan logs) or (b) clearly flag "EOL risk identified — upgrade readiness not assessed" so the admin knows the limitation.

### 5b. Hardware incompatibility

- Windows 11 requires TPM 2.0, Secure Boot, specific CPU generations. ~11% of enterprise Windows 10 devices cannot run Windows 11 at all (ControlUp).
- These devices need full replacement, not OS upgrade. The feature should distinguish between "upgradeable" and "hardware-blocked" devices.

### 5c. Application compatibility

- Line-of-business (LOB) applications may not be certified for newer OS versions.
- Third-party security software (SentinelOne, CrowdStrike) can block upgrades if their agent version is incompatible.
- Enterprise middleware (VPN clients, DLP agents, print drivers) frequently cause upgrade regressions.

### 5d. LTSC vs. General Availability

- LTSC editions have different (much longer) lifecycle timelines.
- A fleet may have a mix of GA and LTSC devices. The baseline policy must handle both.

### 5e. macOS-specific challenges

- Apple does not pre-announce EOL. The "end of support" is inferred when security patches stop arriving.
- Major macOS upgrades can drop hardware support for older Mac models entirely.
- Less granular subversioning than Windows (no equivalent of H1/H2 feature updates).

---

## 6. What the Agentic Feature Could Look Like

### Core concept

An **OS EOL Baseline Agent** that continuously monitors fleet OS versions against lifecycle data and surfaces actionable intelligence — not just compliance violations.

### Proposed capabilities (for research discussion — not final requirements)

**A. EOL Lifecycle Intelligence**
- Ingest and maintain a lifecycle database for Windows (by edition and subversion), macOS, and optionally Linux distributions.
- Primary source: Microsoft Graph API + endoflife.date API.
- Support configurable risk horizon (default: 6 months). "Show me devices whose OS version reaches EOL within 6 months."
- Distinguish confirmed EOL dates (Microsoft official) from estimated dates (macOS, community data).

**B. At-Risk Device Identification**
- Query fleet device inventory for current OS version and edition.
- Cross-reference against lifecycle database.
- Produce an "at-risk" device list segmented by:
  - **Red — Past EOL:** Already unsupported. Immediate action.
  - **Amber — EOL within horizon:** Approaching EOL within configured window (e.g. 6 months).
  - **Green — Compliant:** OS version has > horizon months of support remaining.
- Include device metadata: device name, model, serial, assigned user, OS version, edition, EOL date, days remaining.

**C. Baseline Policy Definition**
- Allow IT admin to define a "baseline OS version" per OS family (e.g. "Windows 11 23H2 Enterprise" or "macOS 14 Sonoma").
- The baseline must itself not be approaching EOL within the configured horizon. System validates this.
- Devices below the baseline are flagged for upgrade.

**D. Upgrade Readiness Signal (Phase 2 / enhancement)**
- For Windows devices, integrate with Intune compatibility reports or Windows Setup compatibility scan data to add a readiness dimension:
  - "At risk AND upgrade-ready" → safe to push upgrade.
  - "At risk BUT driver/hardware blocker identified" → needs manual investigation.
  - "At risk AND hardware-incompatible with target OS" → replacement candidate.
- For Lenovo devices specifically, cross-reference with Lenovo driver/BIOS update catalogue (Lenovo XClarity / UXSP data).

**E. Agentic Workflow Integration**
- **Natural language queries in IT Assist:** "Which devices are running an OS version that reaches EOL within 3 months?" / "What's our fleet's EOL risk posture?" / "Show me all Windows 10 devices that can't upgrade to Windows 11."
- **Proactive alerts / smart suggestions:** When the chatbot detects a device or fleet segment approaching EOL, surface a recommendation: "48 devices are running Windows 11 22H2 Enterprise, which reaches end of servicing on Oct 14, 2025 — 4 months away."
- **Action trigger:** From the at-risk list, the admin could initiate an upgrade workflow (system update action) for eligible devices directly from IT Assist.

---

## 7. Enterprise Considerations

### Security
- Devices on unsupported OS versions are a direct security risk — no security patches after EOL.
- This feature is fundamentally a **security posture** tool. Framing it as "compliance" undersells the risk.
- No new data exposure risk — the feature reads existing fleet inventory data and public lifecycle data.

### Privacy
- No PII beyond what's already in the device inventory (device name, assigned user).
- No new data collection required.

### Cost
- **Lifecycle data ingestion:** Microsoft Graph API is included with existing Intune/M365 licensing. endoflife.date is free.
- **Query cost:** Fleet inventory queries are standard device-management operations — negligible incremental cost.
- **LLM cost (for agentic queries):** Natural-language queries about EOL status would use the existing IT Assist LLM pipeline. The lifecycle cross-reference itself is deterministic (date comparison), not AI — the AI layer is for natural-language interface and recommendation generation only. This is a case where **simple automation handles the core logic; AI enhances the interface**.

### Latency
- Lifecycle data can be cached and refreshed daily or weekly (EOL dates change infrequently).
- At-risk device list generation is a database join (device inventory × lifecycle data) — sub-second for typical fleet sizes.
- No user-perceived latency concern.

---

## 8. Intune Integration — Technical Feasibility Deep Dive

### 8a. Can we pull device-level OS version data from Intune? — YES

The Microsoft Graph API exposes the `managedDevice` resource at:
```
GET https://graph.microsoft.com/v1.0/deviceManagement/managedDevices
```

Each device includes:
- `osVersion` — the OS build number (e.g. `10.0.22631.4602`)
- `operatingSystem` — platform name (e.g. `Windows`)
- `model`, `manufacturer`, `serialNumber`, `deviceName`, `userPrincipalName`

**Key nuance:** `osVersion` returns a **build number**, not the friendly subversion name (22H2, 23H2). The agent needs a **build-to-subversion mapping table** to translate. For example:
- `10.0.22621.*` → Windows 11 22H2
- `10.0.22631.*` → Windows 11 23H2
- `10.0.26100.*` → Windows 11 24H2

Microsoft publishes this mapping at [Windows 11 release information](https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information). The mapping is stable and changes only when new feature updates release (~annually). This can be maintained as a static lookup or pulled from the Microsoft Graph lifecycle API (beta).

**Permission required:** `DeviceManagementManagedDevices.Read.All`
**Licensing:** Included in Intune Plan 1 (part of M365 E3/E5/Business Premium). No extra cost.

**Verdict:** Since Lenovo Device Orchestration already integrates with Intune, this is the right data source. No new integration needed — just a new query pattern on existing APIs.

### 8b. The driver compatibility / blocking APIs — what exactly exists?

There are **three distinct APIs/reports**, each with a different purpose. This is where the nuance matters:

#### API 1: Intune Compatibility Reports (PROACTIVE — before upgrade)

This is **not reactive**. It uses Microsoft's app compatibility database and Windows diagnostic data to assess risks **before you attempt an upgrade**.

- **What it tells you:** For a target OS version (e.g. Windows 11 24H2), per device: how many drivers have known compatibility risks, how many apps have risks, system requirement issues, and an overall readiness status (Low/Medium/High risk / Replace device).
- **Driver-specific data:** Identifies specific drivers that will: not migrate, block the upgrade, or need reinstallation. Includes vendor name, driver version, and guidance (e.g. "check with IHV for compatible driver").
- **How it works:** Relies on **Windows diagnostic data** (telemetry) from enrolled devices, cross-referenced against Microsoft's known compatibility database. Devices must have diagnostic data collection enabled (`Share usage data = Required`).
- **Programmatic access:** Reports can be exported via:
  ```
  POST https://graph.microsoft.com/beta/deviceManagement/reports/exportJobs
  ```
  However, the specific report name/parameters for compatibility data via API are not fully documented in the public beta. The Intune admin center UI is the primary surface today.
- **Licensing:** Intune Plan 1.

#### API 2: Windows Autopatch Driver Catalog (the "applicable drivers" API)

This is the API that answers "what's the latest driver available for this device's hardware?"

- **Endpoint:** `GET /beta/admin/windows/updates/deploymentAudiences/{id}/applicableContent?$expand=catalogEntry,matchedDevices`
- **What it tells you:** For each device enrolled in driver management, a list of driver updates that are **newer than currently installed** and applicable to that device's hardware. Each entry includes: manufacturer, driver class, version, release date, and which specific devices it applies to (`matchedDevices`).
- **Critical detail — opt-in required:** Devices must be explicitly **enrolled in Windows Autopatch driver management** first. Once enrolled, Windows Autopatch becomes the authority for driver updates — devices won't get drivers from Windows Update automatically until you approve them.
- **What "applicable" means:** Windows Update scans the device's hardware profile and returns drivers that are better than installed. This includes OEM-published drivers (Lenovo, Intel, Realtek, etc.) **only if the OEM publishes them to Windows Update**. Drivers distributed only via Lenovo Vantage, Lenovo SCCM packages, or direct downloads will **not** appear in this catalog.
- **Licensing:** Intune Plan 1 + Windows Autopatch entitlement (included in M365 E3/E5/Business Premium).

#### API 3: Safeguard Holds (REACTIVE — Microsoft blocks devices after discovering issues)

- **What it is:** When Microsoft discovers that a specific driver/hardware/software combination causes upgrade failures (BSODs, boot failures, data loss), they apply a **safeguard hold** that blocks affected devices from receiving the feature update.
- **Visibility:** Safeguard holds appear in Windows Update for Business reports and in the Intune compatibility report as an "Other" issue type. They're identified by 8-digit hold IDs.
- **API access:** The Windows Updates API in Graph exposes deployment status, but specific safeguard hold queries per device are primarily visible through WUfB reports, not a direct "list all safeguarded devices" API call.
- **Nature:** Reactive in origin (Microsoft discovers the issue from telemetry across millions of devices), but **proactively protective** for your fleet (it prevents your devices from hitting the same issue).

### 8c. Is the workflow you described feasible? — PARTIALLY, with important caveats

Your proposed workflow:
> "Agent runs daily → sees OS upgrades failed due to driver → pulls driver info → compares with latest → upgrades driver → then upgrades OS → then moves to latest driver version"

**What works:**

1. **"See which OS upgrades failed"** — YES. Intune's Feature Update Failure Report (available via Intune admin center and exportable) shows per-device update state, including failures with alert types. The agent could poll this daily.

2. **"Compare with latest driver info"** — YES, via the Autopatch driver catalog API (API 2 above). For devices enrolled in driver management, you can see exactly which newer drivers are available per device.

3. **"Upgrade driver, then upgrade OS, then upgrade driver again"** — YES, this is the correct sequence and the API supports it:
   - Approve the pre-OS-upgrade driver via `POST /updatePolicies/{id}/complianceChanges` (content approval)
   - After driver deploys, the OS upgrade should unblock
   - After OS upgrade completes, re-query the driver catalog — new applicable drivers for the new OS will appear
   - Approve the post-OS-upgrade drivers

**What has gaps:**

4. **"Based on hardware, which is the latest supported driver"** — PARTIALLY. The Autopatch catalog shows drivers published to **Windows Update** that are newer than installed. But:
   - It does NOT show the absolute latest driver version available from the hardware vendor's website or OEM tools.
   - Lenovo-specific drivers distributed only through Lenovo Vantage, Lenovo Commercial Vantage, or Lenovo System Update (not published to Windows Update) will be invisible to this API.
   - For Lenovo devices specifically, there may be a gap between "latest driver on Windows Update" and "latest driver from Lenovo's own catalog."

5. **"If machine is already on latest driver, stay on stale OS or change hardware"** — MOSTLY. If the Autopatch catalog shows no newer applicable drivers AND the compatibility report flags the current driver as blocking the upgrade, then yes — the conclusion is "driver is at latest available version but still incompatible with target OS." The options are: (a) wait for OEM to publish a compatible driver, (b) accept the risk and stay on current OS, or (c) replace hardware. The agent can surface this logic. **However**, the "latest from Windows Update" may not be the absolute latest — the OEM might have a newer version on their website that hasn't been published to Windows Update yet.

6. **"Agent runs daily and detects failures"** — The data latency matters. Windows diagnostic data uploads ~once per day and takes up to 52 hours for end-to-end processing into Intune reports. So the agent's "daily check" would see data that's 1-2 days old, which is acceptable for this use case but worth noting.

### 8d. Licensing and cost summary

| Capability | API | License required | Extra cost? |
|------------|-----|-----------------|-------------|
| List devices + OS version | Graph `managedDevice` | Intune Plan 1 | No (included in M365 E3/E5) |
| Windows lifecycle / EOL dates | Graph Windows Updates API (beta) | M365 E3/E5 | No |
| Compatibility reports (pre-upgrade readiness) | Intune Reports | Intune Plan 1 | No |
| Driver catalog (applicable drivers per device) | Graph Windows Autopatch | Intune Plan 1 + Autopatch entitlement | No (included in M365 E3/E5) |
| Driver deployment (approve + push drivers) | Graph Windows Autopatch | Same as above | No |
| Feature update deployment | Graph Windows Autopatch | Same as above | No |

**All APIs are included in standard M365 E3/E5 licensing.** No per-API-call cost. No separate subscription required. The only prerequisite is that devices are enrolled in Intune and (for driver management) enrolled in Windows Autopatch driver management.

### 8e. Gaps in your understanding — what I'd flag

1. **The compatibility report is PROACTIVE, not just reactive.** You framed the driver blocking data as "upgrade fails once and now the info is there." That's only true for safeguard holds (API 3). The Intune Compatibility Report (API 1) can tell you **before you attempt** an upgrade which drivers will block it. This is the higher-value data source for Phase 2 — you don't have to fail first.

2. **Build number ≠ friendly version name.** Intune gives you `10.0.22631.4602`, not "23H2". The agent needs a mapping layer. This is straightforward but must be designed — it's not automatic.

3. **Windows Autopatch driver catalog only covers drivers on Windows Update.** If Lenovo publishes drivers only through Lenovo System Update or Lenovo Vantage (not Windows Update), they won't appear. For a Lenovo-specific product, this is a meaningful gap. You may need to cross-reference with Lenovo's own driver catalog API or treat this as a known limitation.

4. **Device enrollment in driver management is opt-in and gives Windows Autopatch authority.** Once enrolled, devices **stop** receiving drivers from Windows Update automatically — all driver updates must be explicitly approved. This is a policy decision for the fleet, not just a technical toggle. The IT admin needs to understand this trade-off.

5. **The compatibility report relies on Windows diagnostic data (telemetry).** Devices with telemetry disabled or set to minimal won't appear in readiness reports. In privacy-sensitive environments, this could limit coverage.

6. **"Latest driver supported by hardware and present OS" is not a single API call.** The Autopatch catalog tells you what's newer and applicable. It doesn't give you a canonical "latest version for this hardware model." To truly know the absolute latest, you'd need the OEM's own catalog (Lenovo's driver repository for ThinkPad T14 Gen 4, for instance). This is a product decision: is "latest on Windows Update" good enough, or do you need "latest from Lenovo"?

7. **The driver → OS → driver upgrade sequence is correct but multi-step.** Each step (driver approval → deployment → OS upgrade → re-scan → new driver approval → deployment) takes time. Driver deployments can take days to roll out. OS upgrades can take hours per device. The full cycle for a blocked device could be a week+. The agent workflow needs to account for this timeline and provide status tracking across the sequence.

---

## 9. Tools & APIs Inventory for Engineering Evaluation

This section catalogues every tool and API relevant to solving the OS EOL baselining and driver readiness problem. Engineering should evaluate each for access, feasibility, and integration effort.

### TOOL 1: Microsoft Graph — managedDevice (Device Inventory)

**What it solves:** Phase 1 — "Which devices are on which OS version?"

| Attribute | Detail |
|-----------|--------|
| **Endpoint** | `GET https://graph.microsoft.com/v1.0/deviceManagement/managedDevices` |
| **API status** | GA (v1.0) — production-ready |
| **Key fields returned** | `osVersion` (build number, e.g. `10.0.22631.4602`), `operatingSystem`, `model`, `manufacturer`, `serialNumber`, `deviceName`, `userPrincipalName` |
| **Filter support** | OData `$filter` on `osVersion`, `operatingSystem`, etc. |
| **Permission** | `DeviceManagementManagedDevices.Read.All` |
| **License** | Intune Plan 1 (included in M365 E3/E5/Business Premium) |
| **Extra cost** | None |
| **Caveat** | Returns build numbers, NOT friendly names (22H2, 23H2). Needs a build-to-subversion mapping table. |

**Build-to-subversion mapping source:** [Windows 11 release information](https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information). Changes ~once/year. Can be hard-coded or pulled from Graph lifecycle API.

---

### TOOL 2: Microsoft Graph — Windows Product Lifecycle API (EOL Dates)

**What it solves:** Phase 1 — "When does each OS subversion reach end of servicing?"

| Attribute | Detail |
|-----------|--------|
| **Endpoint** | `GET https://graph.microsoft.com/beta/admin/windows/updates/products` (and sub-resources for editions, servicing periods) |
| **API status** | Beta — functional but schema may change |
| **What it provides** | Per-product: editions, servicing periods with start/end dates, known issues |
| **Permission** | `WindowsUpdates.ReadWrite.All` |
| **License** | M365 E3/E5 |
| **Extra cost** | None |
| **Caveat** | Beta endpoint. For production stability, can cross-reference with endoflife.date API or hard-code from Microsoft Lifecycle page. |

**Fallback source:** [endoflife.date API](https://endoflife.date/docs/api) — free, open-source, community-maintained. Endpoint: `GET https://endoflife.date/api/windows.json`. Returns release dates, EOL dates, latest versions per cycle. Not vendor-official but well-maintained.

---

### TOOL 3: Intune Compatibility Reports (Pre-Upgrade Readiness)

**What it solves:** Phase 2 — "Before I upgrade, which devices will fail due to driver/app/hardware issues?"

| Attribute | Detail |
|-----------|--------|
| **Where** | Intune admin center → Reports → Device management → Windows updates → Reports tab |
| **Reports** | (a) *Windows feature update device readiness report* — per-device risk. (b) *Windows feature update compatibility risks report* — org-wide top risks. |
| **What it tells you per device** | Readiness status (Low/Medium/High risk / Replace device), count of driver issues, app issues, system requirement issues. Drill-down shows specific driver name, vendor, version, issue type, and guidance. |
| **Driver issue types** | "Driver won't migrate" / "Driver blocks upgrade" / "New driver installed during upgrade" — with guidance per issue. |
| **How data is generated** | From **Windows diagnostic data** (telemetry) cross-referenced with Microsoft's compatibility database. Devices scan and upload data ~daily; end-to-end latency up to ~52 hours. |
| **Proactive or reactive?** | **PROACTIVE.** This data exists BEFORE you attempt an upgrade. It's predictive based on Microsoft's known-issue database across millions of devices. |
| **Prerequisites to enable** | 1. In Intune admin center: Tenant administration → Connectors and tokens → Windows data → set "Enable features that require Windows diagnostic data in processor configuration" to **On**. 2. Attest to having Windows E3/E5 or equivalent licenses. 3. Devices must be Azure AD joined or Hybrid Azure AD joined, enrolled in Intune MDM. 4. Devices must have diagnostic data collection set to **"Required"** (not Optional or Off). |
| **Programmatic access** | Reports can be exported via `POST https://graph.microsoft.com/beta/deviceManagement/reports/exportJobs`. Specific report type parameters for compatibility reports are not fully documented in public beta — **engineering should test this in a sandbox**. The Intune admin center UI is the primary surface today. |
| **License** | Intune Plan 1 + Windows E3/E5 attestation |
| **Extra cost** | None beyond existing licensing |
| **Key limitation** | Depends on devices having telemetry enabled at "Required" level. Devices with telemetry off = invisible. |

---

### TOOL 4: Windows Autopatch — Driver Update Catalog (Applicable Drivers per Device)

**What it solves:** Phase 2 — "What newer drivers are available for each device's hardware?"

**What Autopatch actually is (plain English):** Windows Autopatch is a cloud service built into Intune that manages the rollout of Windows updates (feature updates, quality updates, drivers, firmware). For drivers specifically, it acts as a **gatekeeper**: when a device scans Windows Update, Autopatch collects the scan results (which drivers are available and newer than installed), catalogues them, and lets the admin browse/approve/schedule them. Think of it as a "driver update shopping cart" populated automatically by Windows Update scan results, per device.

**How it relates to Lenovo Device Orchestration:** Autopatch runs inside the Intune service that Device Orchestration is already integrated with. It does not require a separate product. However, the driver data it surfaces only covers what's on **Windows Update** — not Lenovo's own driver repository (see Tool 5).

| Attribute | Detail |
|-----------|--------|
| **Step 1 — Enroll devices** | `POST https://graph.microsoft.com/beta/admin/windows/updates/updatableAssets/enrollAssets` with `"updateCategory": "driver"` and device IDs |
| **Step 2 — Create audience** | `POST /beta/admin/windows/updates/deploymentAudiences` → add devices as members |
| **Step 3 — Browse applicable drivers** | `GET /beta/admin/windows/updates/deploymentAudiences/{id}/applicableContent?$expand=catalogEntry,matchedDevices` |
| **What it returns** | Per driver: `displayName`, `manufacturer`, `driverClass`, `version`, `releaseDateTime`, `setupInformationFile`, and which devices it matches (`matchedDevices` with device IDs) |
| **Step 4 — Approve & deploy** | `POST /beta/admin/windows/updates/updatePolicies/{id}/complianceChanges` with the catalog entry ID and a scheduled start date |
| **Approval modes** | **Automatic** (deploy after configurable deferral days) or **Manual** (admin explicitly approves each driver) |
| **API status** | Beta — but publicly available and actively used since Feb 2023 |
| **Permission** | `WindowsUpdates.ReadWrite.All` + `Device.Read.All` |
| **License** | Intune Plan 1 + Autopatch entitlement (included in M365 E3/E5/Business Premium) |
| **Extra cost** | None |
| **Critical behavior change** | **Once a device is enrolled in driver management, Windows Autopatch takes over as the authority for driver updates.** The device STOPS receiving automatic driver updates from Windows Update. All driver updates must go through the approval workflow (manual or auto). This is intentional — it gives the admin control — but it means the fleet's driver update behaviour changes. IT admins must be aware of this trade-off. |
| **What "applicable" covers** | Only drivers published to **Windows Update** by OEMs (Intel, Realtek, NVIDIA, Lenovo, etc.). If a driver is only available through Lenovo's own distribution (Vantage, System Update, Thin Installer), it will NOT appear in this catalog. |

---

### TOOL 5: Lenovo Driver Catalog (Lenovo's Own Driver Repository)

**What it solves:** The **Lenovo-specific gap** — drivers that Lenovo distributes outside of Windows Update.

**Why this matters:** Lenovo publishes many device-specific drivers (display, fingerprint sensor, power management, Thunderbolt firmware, BIOS, Lenovo Vantage components) through its own repository at `download.lenovo.com`. These may not be published to Windows Update, so they won't appear in the Autopatch driver catalog (Tool 4). For a Lenovo product, this is a significant blind spot.

| Attribute | Detail |
|-----------|--------|
| **Catalog URL** | `https://download.lenovo.com/catalog/{ModelCode}_Win10.xml` (per model, per OS) |
| **Master catalog** | `https://download.lenovo.com/cdrt/td/catalogv2.xml` (all models, used by SCCM/Update Retriever) |
| **Catalog V3** | `https://download.lenovo.com/luc/v2/LenovoUpdatesCatalog2v2.cab` |
| **Format** | XML — model-specific package lists with version, severity, applicability rules, download URLs |
| **What each package entry contains** | Package ID, title, version, severity (critical/recommended/optional), reboot type, applicable models, applicable OS versions, download URL, applicability tests (hardware detection rules) |
| **Programmatic access** | **Option A — PowerShell (LSUClient):** Open-source module. `Get-LSUpdate -Model 20K70000GE` returns all available packages for a specific Lenovo model, including applicability and install status checks. Repository defaults to `https://download.lenovo.com/catalog`. **Option B — Lenovo Client Scripting Module:** Official Lenovo PowerShell module. `Get-LnvUpdatesRepo` generates a local repo for specified machine types and OS versions. `Find-LnvUpdate` searches for specific updates. **Option C — Direct XML parsing:** Fetch the model-specific catalog XML, parse package entries, compare versions with installed. |
| **Can it tell "latest driver for this hardware"?** | **Yes** — for Lenovo-published drivers. The catalog lists all available packages per model. By comparing `version` in the catalog with what's installed on the device, you can determine if the device is on the latest Lenovo-published version. |
| **Lenovo-internal access** | Since Lenovo Device Orchestration is a Lenovo product, engineering likely has internal access to the catalog infrastructure. The public XML endpoints are available but a more structured internal API may exist — **engineering should confirm**. |
| **License / cost** | The public catalog is free. No API key required. |
| **Key gap** | The catalog tells you what's available. It does NOT tell you which drivers are compatible with which OS version for upgrade purposes (i.e. "will this driver block a Windows 11 24H2 upgrade?"). That compatibility intelligence comes from Microsoft (Tool 3). |

---

### TOOL 6: Microsoft Graph — Feature Update Deployment + Failure Reports

**What it solves:** Phase 2 — "Track OS upgrade status and detect failures."

| Attribute | Detail |
|-----------|--------|
| **Deploy feature updates** | Via Intune feature update policies or Graph API: `POST /beta/admin/windows/updates/deployments` |
| **Monitor status** | Intune Reports → Feature update policies → per-device update state (Pending, In progress, Succeeded, Failed, Cancelled) |
| **Failure data** | Feature update failures report shows alert type, alert message, last event time per device. Includes error codes and categories. |
| **Programmatic access** | Export via `POST /beta/deviceManagement/reports/exportJobs` |
| **License** | Intune Plan 1 |

---

### TOOL 7: Safeguard Holds (Microsoft-side Protection)

**What it solves:** Awareness — "Which devices is Microsoft actively blocking from upgrading?"

| Attribute | Detail |
|-----------|--------|
| **What it is** | When Microsoft identifies a driver/hardware/software combo that causes upgrade failure, they apply a "safeguard hold" that prevents affected devices from receiving the update. |
| **Visibility** | Appears in Windows Update for Business reports, in the Intune compatibility report under "Other" category, identified by 8-digit hold IDs. |
| **API access** | Not directly queryable as "list all safeguarded devices." Visible through WUfB reports and Intune compatibility reports. |
| **Admin action** | None required — it's automatic protection. The hold is lifted when Microsoft/OEM resolves the issue. Admin can opt out (not recommended). |

---

### TOOL 8: Windows Update for Business (WUfB) Reports — Azure Log Analytics

**What it solves:** Both phases — EOS device counts (Phase 1) + driver update status/failures (Phase 2), all queryable via KQL.

| Attribute | Detail |
|-----------|--------|
| **What it is** | A cloud reporting service that collects Windows update data (feature, quality, driver) from Intune-managed devices and stores it in Azure Log Analytics. Pre-built Azure Workbook for visualization. |
| **Where** | Azure Portal → Monitor → Workbooks → "Windows Update for Business reports" |
| **Data storage** | Azure Log Analytics workspace (KQL-queryable) |
| **Key tables** | `UCClient` (device info), `UCClientUpdateStatus` (per-device per-update status), `UCUpdateAlert` (errors/warnings), `UCClientReadinessStatus` (Win 11 readiness), `UCServiceUpdateStatus` (service-side status) |
| **Driver-specific fields** | `UpdateManufacturer` (OEM name — Intel, Lenovo, Synaptics, etc.), `UpdateDisplayName` (driver name + version), `UpdateCategory` = "Driver", `CatalogId` (Autopatch catalog ID), `ClientState` / `ClientSubstate` (install progress) |
| **EOL/EOS awareness** | Feature Updates tab already has built-in tiles: "End of service feature update" (devices past EOS), "Nearing EOS" (devices within 18 months of EOS). Not configurable to 6-month horizon — custom KQL query needed. |
| **Driver update tracking** | Tracks which driver updates were offered/installing/installed/failed per device, with manufacturer and display name. |
| **Failure data** | `UCUpdateAlert` table contains error codes, descriptions, recommendations when updates fail. |
| **Programmatic access** | Azure Monitor Log Analytics API — REST endpoint for running KQL queries. Also: Power BI integration, Azure Data Explorer. |
| **Prerequisites** | Azure subscription + Log Analytics workspace + device enrollment into WUfB Reports (via Intune policy or script). Same diagnostic data requirement (Required level). |
| **License** | Included in Windows 10/11 E3/E5, M365 E3/E5. Log Analytics ingestion for WUfB data is **free** (no Azure charges for this specific data). |
| **Extra cost** | None for WUfB data. Standard Azure charges apply only if you add custom data. |
| **Advantage over Intune UI** | Data is in Log Analytics = fully queryable, joinable, exportable. Intune admin center reports are UI-only with limited export. |
| **Limitation** | Tracks driver updates that flow through Windows Update/Autopatch only. No Lenovo-specific drivers outside WU. "Nearing EOS" threshold is fixed at 18 months in the workbook (custom query needed for 6 months). No predictive compatibility assessment — only tracks what happened, not what will happen. |

**Source:** [WUfB Reports overview](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-overview) | [WUfB Reports workbook](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-workbook) | [UCClientUpdateStatus schema](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-schema-ucclientupdatestatus) | [Prerequisites](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-prerequisites)

---

### Summary: How the Tools Fit Together

```
PHASE 1 (EOL Intelligence)
├── OPTION A (simpler): TOOL 8 — WUfB Reports
│   └── Feature Updates tab already has "End of service" + "Nearing EOS" device counts
│   └── Custom KQL query to change threshold from 18 months → 6 months
│   └── Data in Log Analytics = programmatically queryable
│
├── OPTION B (more control): TOOL 1 + TOOL 2
│   ├── TOOL 1: Graph managedDevice → Get device list with OS build numbers
│   ├── Build-to-subversion mapping table → Convert 10.0.22631.* → "23H2"
│   ├── TOOL 2: Graph Lifecycle API (or endoflife.date) → Get EOL dates per subversion + edition
│   └── Cross-reference → At-risk device list (Red/Amber/Green)
│
├── Recommended: Use BOTH — WUfB Reports for dashboard/alerting, Tool 1+2 for IT Assist queries

PHASE 2 (Upgrade Readiness + Remediation)
├── TOOL 3: Intune Compatibility Reports → BEFORE upgrade: which devices have driver/app/hw blockers?
├── TOOL 4: Autopatch Driver Catalog → What newer drivers are available on Windows Update?
├── TOOL 5: Lenovo Driver Catalog → What newer drivers are available from Lenovo's own repo?
├── TOOL 8: WUfB Reports → Track driver update status, failures, OEM info across fleet
├── Decision logic:
│   ├── Device has driver blocker + newer driver available (Tool 4 or 5) → Upgrade driver first, then OS
│   ├── Device has driver blocker + already on latest driver → Stay on current OS or replace hardware
│   ├── Device has hardware blocker (no TPM 2.0, etc.) → Replace hardware
│   └── Device is clear → Safe to push OS upgrade
├── TOOL 6: Feature Update Deployment + Failure Reports → Track upgrade progress, detect failures
└── TOOL 7: Safeguard Holds → Awareness of Microsoft-side blocks
```

### Engineering Evaluation Checklist

| # | Question for Engineering | Tool(s) | Priority |
|---|-------------------------|---------|----------|
| 1 | Can we query `GET /deviceManagement/managedDevices` and filter by `osVersion`? Test with a sample tenant. What's the exact format of `osVersion` values returned? | Tool 1 | Phase 1 — must have |
| 2 | Is the Graph Windows lifecycle API (beta) stable enough for production? Or should we hard-code EOL dates / use endoflife.date as primary? | Tool 2 | Phase 1 — must have |
| 3 | Is Windows diagnostic data already enabled on managed devices in the fleet? If not, what's the rollout effort? | Tool 3 prereq | Phase 2 — must have |
| 4 | Can we programmatically export compatibility reports via the Graph `exportJobs` endpoint? What report type string is needed? Test in sandbox. | Tool 3 | Phase 2 — must have |
| 5 | Are devices currently enrolled in Autopatch driver management? If not, is the fleet willing to accept the behavior change (Autopatch becomes driver authority)? | Tool 4 | Phase 2 — key decision |
| 6 | Does Lenovo Device Orchestration already consume the Lenovo driver catalog XML? Is there an internal API that provides structured access (beyond public XML)? | Tool 5 | Phase 2 — Lenovo advantage |
| 7 | For the driver → OS → driver upgrade sequence: can we orchestrate this via Graph API calls, or does it need to flow through existing Intune deployment rings? | Tools 4 + 6 | Phase 2 — architecture |
| 8 | What's the telemetry coverage? % of devices with diagnostic data at "Required" level? | Tool 3 prereq | Phase 2 — coverage risk |

---

## 10. Open Questions (Revised, Windows-only scope)

1. **Lenovo driver catalog gap:** The Autopatch driver catalog only covers drivers published to Windows Update. Lenovo distributes many device-specific drivers (display, fingerprint, power management) only through Lenovo System Update / Vantage. Does Lenovo Device Orchestration have access to Lenovo's own driver repository API? If so, this could close the gap. If not, should Phase 2 acknowledge "latest on Windows Update" as a known limitation?
2. **Autopatch enrollment policy:** Enrolling devices in Windows Autopatch driver management transfers driver update authority from Windows Update to Autopatch (manual/auto approval required). Is this acceptable for the fleet, or would IT admins push back on the control change?
3. **LTSC handling:** Should LTSC devices (5–10 year support lifecycle) be included in the same baseline policy as GA devices, or require a separate baseline?
4. **Telemetry dependency:** Compatibility reports require Windows diagnostic data set to "Required." Are there fleet segments where telemetry is restricted (e.g. government, regulated industries) that would limit Phase 2 coverage?
5. **Upgrade action depth (Phase 2):** Should the agent trigger the driver → OS → driver upgrade sequence directly, or present the plan and let the admin execute through their existing Intune deployment rings / SCCM task sequences?
6. **Hardware replacement:** For devices that can't upgrade due to hardware incompatibility (no TPM 2.0, unsupported CPU), should the feature surface a replacement recommendation, or is that out of scope?
7. **Non-Intune devices:** Are there devices in the fleet not managed by Intune? If so, Phase 1 EOL queries would miss them. What's the fallback?

---

## 11. Sources

1. Microsoft Lifecycle — Ending Support 2025/2026: [learn.microsoft.com/en-us/lifecycle/end-of-support](https://learn.microsoft.com/en-us/lifecycle/end-of-support/end-of-support-2025)
2. Windows 11 Enterprise & Education lifecycle: [learn.microsoft.com/en-us/lifecycle/products/windows-11-enterprise-and-education](https://learn.microsoft.com/en-us/lifecycle/products/windows-11-enterprise-and-education)
3. Microsoft Graph API — Windows lifecycle + known issues: [techcommunity.microsoft.com — Windows Known Issues and Product Lifecycle in Graph API](https://techcommunity.microsoft.com/blog/windows-itpro-blog/windows-known-issues-and-product-lifecycle-in-graph-api/4105047)
4. endoflife.date API: [endoflife.date/docs/api](https://endoflife.date/docs/api)
5. Intune OS version management: [learn.microsoft.com/en-us/mem/intune/fundamentals/manage-os-versions](https://learn.microsoft.com/en-us/mem/intune/fundamentals/manage-os-versions)
6. Intune compatibility reports: [learn.microsoft.com/en-us/intune/device-updates/windows/compatibility-reports](https://learn.microsoft.com/en-us/intune/device-updates/windows/compatibility-reports)
7. ControlUp Windows 11 adoption study: [prnewswire.com — ControlUp Study](https://www.prnewswire.com/news-releases/controlup-study-reveals-over-82-of-enterprise-windows-endpoint-devices-are-not-yet-running-windows-11-302215428.html)
8. Windows 11 24H2 driver compatibility issues: [windowsforum.com — 24H2 rollout challenges](https://windowsforum.com/threads/windows-11-24h2-update-rollout-fixes-challenges-and-enterprise-insights.364750/)
9. Gitnux update statistics / failure cost data: [gitnux.org/update-statistics](https://gitnux.org/update-statistics/)
10. Ivanti Mandatory Baseline: [help.ivanti.com — mandatory-baseline-view](https://help.ivanti.com/ht/help/en_US/IES/2022/UG_PR/mandatory-baseline-view.htm)
11. FleetDM OS update enforcement: [fleetdm.com/guides/enforce-os-updates](https://fleetdm.com/guides/enforce-os-updates)
12. Apple lifecycle management: [apple.com/business/docs/resources/Apple_Lifecycle_Management.pdf](https://www.apple.com/business/docs/resources/Apple_Lifecycle_Management.pdf)
13. Microsoft Graph — managedDevice resource: [learn.microsoft.com/en-us/graph/api/resources/intune-devices-manageddevice](https://learn.microsoft.com/en-us/graph/api/resources/intune-devices-manageddevice?view=graph-rest-1.0)
14. Microsoft Graph — Deploy driver update via Autopatch: [learn.microsoft.com/en-us/graph/windowsupdates-manage-driver-update](https://learn.microsoft.com/en-us/graph/windowsupdates-manage-driver-update)
15. Microsoft Graph — driverUpdateCatalogEntry: [learn.microsoft.com/en-us/graph/api/resources/windowsupdates-driverupdatecatalogentry](https://learn.microsoft.com/en-us/graph/api/resources/windowsupdates-driverupdatecatalogentry?view=graph-rest-beta)
16. Intune driver update policy FAQ: [learn.microsoft.com/en-us/intune/device-updates/windows/driver-updates-faq](https://learn.microsoft.com/en-us/intune/device-updates/windows/driver-updates-faq)
17. Windows Autopatch driver management: [learn.microsoft.com/en-us/windows/deployment/update/deployment-service-drivers](https://learn.microsoft.com/en-us/windows/deployment/update/deployment-service-drivers)
18. Intune licensing: [learn.microsoft.com/en-us/intune/intune-service/fundamentals/licenses](https://learn.microsoft.com/en-us/intune/intune-service/fundamentals/licenses)
19. Safeguard holds: [learn.microsoft.com/en-us/windows/deployment/update/safeguard-holds](https://learn.microsoft.com/en-us/windows/deployment/update/safeguard-holds)
20. Lenovo CDRT documentation: [docs.lenovocdrt.com](https://docs.lenovocdrt.com/)
21. Lenovo driver catalog XML (per model): `https://download.lenovo.com/catalog/{ModelCode}_Win10.xml`
22. Lenovo master catalog V2 (SCCM): `https://download.lenovo.com/cdrt/td/catalogv2.xml`
23. LSUClient (open-source PowerShell module): [jantari.github.io/LSUClient-docs](https://jantari.github.io/LSUClient-docs/docs/cmdlets/get-lsupdate/)
24. Lenovo Client Scripting Module: [docs.lenovocdrt.com/guides/lcsm](https://docs.lenovocdrt.com/guides/lcsm/lcsm_top/)
25. Intune enabling Windows diagnostic data: [learn.microsoft.com/en-us/intune/protect/data-enable-windows-data](https://learn.microsoft.com/en-us/intune/intune-service/protect/data-enable-windows-data)
26. Windows Autopatch overview: [learn.microsoft.com/en-us/windows/deployment/windows-autopatch/overview](https://learn.microsoft.com/en-us/windows/deployment/windows-autopatch/overview/windows-autopatch-overview)
27. WUfB Reports overview: [learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-overview](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-overview)
28. WUfB Reports workbook: [learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-workbook](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-workbook)
29. UCClientUpdateStatus schema (driver fields): [learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-schema-ucclientupdatestatus](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-schema-ucclientupdatestatus)
30. WUfB Reports prerequisites: [learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-prerequisites](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-prerequisites)
31. WUfB Reports enable: [learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-enable](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-enable)
