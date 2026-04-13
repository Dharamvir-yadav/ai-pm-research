# Step-by-Step: Accessing OS EOL & Driver Readiness Data from Intune

This document walks through how to access each piece of data, what you get back, and how it maps to the OS EOL baselining use case.

---

## Verification Sources

Before we start — here are the primary Microsoft documentation pages to verify every claim:

| Claim | Source |
|-------|--------|
| Windows 11 Enterprise defaults to "Required" diagnostic data | [admx.help — AllowTelemetry policy](https://admx.help/?Category=Windows_11_2022&Policy=Microsoft.Policies.DataCollection::AllowTelemetry) — quote: *"If you disable or do not configure this policy setting, the device will send required diagnostic data"* |
| Diagnostic data levels (Required/Optional/Off) | [Changes to Windows diagnostic data collection](https://learn.microsoft.com/en-us/windows/privacy/changes-to-windows-diagnostic-data-collection) |
| How to configure diagnostic data in your org | [Configure Windows diagnostic data in your organization](https://learn.microsoft.com/en-us/windows/privacy/configure-windows-diagnostic-data-in-your-organization) |
| Intune tenant-level toggle (defaults to Off) | [Enable use of Windows diagnostic data by Intune](https://learn.microsoft.com/en-us/intune/intune-service/protect/data-enable-windows-data) |
| Compatibility reports — what they show, prerequisites | [Use Compatibility Reports for Windows Updates in Intune](https://learn.microsoft.com/en-us/intune/device-updates/windows/compatibility-reports) |
| managedDevice resource (device list + OS version) | [managedDevice resource type — Microsoft Graph v1.0](https://learn.microsoft.com/en-us/graph/api/resources/intune-devices-manageddevice?view=graph-rest-1.0) |
| List managedDevices API | [List managedDevices — Microsoft Graph v1.0](https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-list?view=graph-rest-1.0) |
| Windows product lifecycle API | [Windows known issues and product lifecycle in Graph API](https://techcommunity.microsoft.com/blog/windows-itpro-blog/windows-known-issues-and-product-lifecycle-in-graph-api/4105047) |
| Driver update catalog + deployment via Autopatch | [Deploy a driver update using Windows Autopatch](https://learn.microsoft.com/en-us/graph/windowsupdates-manage-driver-update) |
| Autopatch driver management overview | [Programmatic controls for drivers and firmware](https://learn.microsoft.com/en-us/windows/deployment/update/deployment-service-drivers) |
| Intune driver update policies (manual/auto approval) | [Manage Windows Driver Updates — Intune](https://learn.microsoft.com/en-us/intune/intune-service/protect/windows-driver-updates-overview) |
| Safeguard holds | [Safeguard holds for Windows](https://learn.microsoft.com/en-us/windows/deployment/update/safeguard-holds) |
| Intune licensing for all of the above | [Licenses available for Microsoft Intune](https://learn.microsoft.com/en-us/intune/intune-service/fundamentals/licenses) |

---

## STEP 1: Get device inventory with OS version (Phase 1)

### What you're doing
Pulling the list of all Intune-managed devices with their current OS build number, model, and assigned user.

### How to access

**Option A — Graph Explorer (for testing / manual):**
1. Go to [Graph Explorer](https://developer.microsoft.com/graph/graph-explorer)
2. Sign in with an account that has `DeviceManagementManagedDevices.Read.All` permission
3. Run this query:
```
GET https://graph.microsoft.com/v1.0/deviceManagement/managedDevices?$select=deviceName,osVersion,operatingSystem,model,manufacturer,serialNumber,userPrincipalName
```

**Option B — Programmatic (for production):**
```
GET https://graph.microsoft.com/v1.0/deviceManagement/managedDevices
  ?$filter=operatingSystem eq 'Windows'
  &$select=deviceName,osVersion,operatingSystem,model,manufacturer,serialNumber,userPrincipalName
```
Permission: `DeviceManagementManagedDevices.Read.All`
Auth: OAuth2 bearer token via app registration in Azure AD.

### What data you get back

```json
{
  "value": [
    {
      "deviceName": "LAPTOP-ABC123",
      "osVersion": "10.0.22631.4602",
      "operatingSystem": "Windows",
      "model": "ThinkPad T14 Gen 4",
      "manufacturer": "LENOVO",
      "serialNumber": "PF4ABC12",
      "userPrincipalName": "john.doe@company.com"
    },
    {
      "deviceName": "DESKTOP-XYZ789",
      "osVersion": "10.0.19045.4170",
      "operatingSystem": "Windows",
      "model": "ThinkCentre M90q Gen 3",
      "manufacturer": "LENOVO",
      "serialNumber": "MJ2DEF34",
      "userPrincipalName": "jane.smith@company.com"
    }
  ]
}
```

### How it maps to your use case

| Field | What it tells you |
|-------|-------------------|
| `osVersion: "10.0.22631.4602"` | Build `22631` = **Windows 11 23H2**. You map the build number to the subversion using a lookup table (see Step 2). |
| `osVersion: "10.0.19045.4170"` | Build `19045` = **Windows 10 22H2** — EOL Oct 14, 2025. This device is at risk. |
| `model` + `manufacturer` | Needed in Phase 2 to look up Lenovo-specific drivers and hardware compatibility. |
| `userPrincipalName` | Who to notify about the upgrade. |

### Build-to-subversion mapping (key examples)

| Build prefix | Subversion | Edition-dependent EOL |
|-------------|------------|----------------------|
| `10.0.19041` | Windows 10 2004 | Already EOL |
| `10.0.19044` | Windows 10 21H2 | Already EOL |
| `10.0.19045` | Windows 10 22H2 | **Oct 14, 2025** (all editions) |
| `10.0.22000` | Windows 11 21H2 | Already EOL |
| `10.0.22621` | Windows 11 22H2 | **Oct 14, 2025** (Enterprise/Education) |
| `10.0.22631` | Windows 11 23H2 | Nov 10, 2026 (Enterprise/Education) |
| `10.0.26100` | Windows 11 24H2 | Oct 12, 2027 (Enterprise/Education) |

Full mapping: [Windows 11 release information](https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information) and [Windows 10 release information](https://learn.microsoft.com/en-us/windows/release-health/release-information).

**Phase 1 output:** Cross-reference device OS build → subversion → EOL date → flag devices within 6-month horizon. This is a deterministic date comparison — no AI needed for the logic, just the data join.

---

## STEP 2: Get EOL dates per subversion (Phase 1)

### What you're doing
Getting the official end-of-servicing date for each Windows subversion and edition.

### How to access

**Option A — Microsoft Graph Lifecycle API (beta):**
```
GET https://graph.microsoft.com/beta/admin/windows/updates/products
```
Returns Windows products with editions and servicing periods (including end-of-servicing dates).

Permission: `WindowsUpdates.ReadWrite.All`

**Option B — endoflife.date API (free, no auth):**
```
GET https://endoflife.date/api/windows.json
```
No authentication needed. Returns all Windows release cycles with EOL dates.

**Option C — Hard-code from Microsoft Lifecycle page:**
[Microsoft Lifecycle — Windows 11 Enterprise and Education](https://learn.microsoft.com/en-us/lifecycle/products/windows-11-enterprise-and-education)

EOL dates change only when Microsoft announces new feature updates (~once/year). A hard-coded table refreshed annually is viable for Phase 1.

### What data you get back (endoflife.date example)

```json
[
  {
    "cycle": "11-24H2",
    "releaseDate": "2024-10-01",
    "eol": "2027-10-12",
    "latest": "10.0.26100.3775",
    "lts": false
  },
  {
    "cycle": "11-23H2",
    "releaseDate": "2023-10-31",
    "eol": "2026-11-10",
    "latest": "10.0.22631.5335",
    "lts": false
  },
  {
    "cycle": "10-22H2",
    "releaseDate": "2022-10-18",
    "eol": "2025-10-14",
    "latest": "10.0.19045.5737",
    "lts": false
  }
]
```

Note: endoflife.date returns a single EOL date per cycle. Enterprise/Education editions have longer EOL dates than Home/Pro. For edition-specific dates, use the Microsoft Graph lifecycle API or the Microsoft Lifecycle page directly.

### How it maps to your use case

Join this with Step 1. For each device: `device.osVersion` → build prefix → subversion cycle → `eol` date → compute `days_remaining = eol - today`. If `days_remaining < 180` → device is at risk.

---

## STEP 3: Generate the at-risk device list (Phase 1 — the agent output)

### What you're doing
Combining Steps 1 + 2 to produce the list the IT admin needs.

### The logic (pseudocode)

```
for each device in intune_devices:
    subversion = build_to_subversion(device.osVersion)
    eol_date = lifecycle_data[subversion][device.edition]
    days_remaining = eol_date - today

    if days_remaining < 0:
        device.risk = "RED — Past EOL"
    elif days_remaining < 180:
        device.risk = "AMBER — EOL within 6 months"
    else:
        device.risk = "GREEN — Compliant"
```

### What the admin sees (example output in IT Assist)

> **Fleet OS EOL Risk Summary**
>
> | Risk | Count | Details |
> |------|-------|---------|
> | RED — Past EOL | 12 | Windows 10 22H2 — EOL passed Oct 14, 2025 |
> | AMBER — Within 6 months | 48 | Windows 11 22H2 Enterprise — EOL Oct 14, 2025 (120 days) |
> | GREEN — Compliant | 1,940 | Windows 11 23H2+ |
>
> **Devices at immediate risk (RED):**
>
> | Device | Model | OS | EOL | User |
> |--------|-------|----|-----|------|
> | LAPTOP-ABC123 | ThinkPad T14 Gen 3 | Win 10 22H2 | Oct 14, 2025 | john.doe@ |
> | DESKTOP-XYZ789 | ThinkCentre M90q | Win 10 22H2 | Oct 14, 2025 | jane.smith@ |

### How the user queries this (natural language in IT Assist)

- "Which devices are running an OS that reaches EOL within 3 months?"
- "How many devices are still on Windows 10?"
- "Show me all devices on Windows 11 22H2"
- "What's our fleet's OS EOL risk posture?"

**This is Phase 1. Pure data join + natural language interface. No driver assessment, no upgrade actions.**

---

## STEP 4: Pre-upgrade readiness check (Phase 2)

### What you're doing
Before pushing an OS upgrade to at-risk devices, checking which ones will succeed and which will fail due to driver/app/hardware issues.

### How to access — Intune Compatibility Report

**Prerequisites (verify these first):**

1. **Device-level telemetry — verify current state:**
   - In Intune admin center → Devices → Configuration profiles → look for any profile that configures `System/AllowTelemetry`
   - If NO policy exists: devices default to "Required" (level 1) — **you're good**
   - If a policy exists: check the value. Must be ≥ 1 (Required). If set to 0 (Off), that's a problem.
   - Source: [AllowTelemetry policy reference](https://admx.help/?Category=Windows_11_2022&Policy=Microsoft.Policies.DataCollection::AllowTelemetry) — *"If you disable or do not configure this policy setting, the device will send required diagnostic data"*

2. **Tenant-level Intune toggle — verify current state:**
   - In Intune admin center → Tenant administration → Connectors and tokens → Windows data
   - Check if "Enable features that require Windows diagnostic data in processor configuration" is **On** or **Off**
   - If Off: flip to On (30-second change, requires Intune admin)
   - Source: [Enable use of Windows diagnostic data by Intune](https://learn.microsoft.com/en-us/intune/intune-service/protect/data-enable-windows-data)

3. **License attestation:**
   - On the same Windows data page: "I confirm that my tenant owns one of these licenses" → toggle On
   - Required licenses: Windows E3/E5, M365 E3/E5, M365 Business Premium, or equivalent
   - Source: same as above

**Generating the report:**

1. In Intune admin center → Reports → Device management → Windows updates → Reports tab
2. Select **Windows Feature Update Device Readiness Report**
3. Choose **Target OS** (e.g. "Windows 11, version 24H2")
4. Choose **Scope tags** (which devices to assess)
5. Click **Generate report** (takes a few minutes)

Source: [Use Compatibility Reports for Windows Updates in Intune](https://learn.microsoft.com/en-us/intune/device-updates/windows/compatibility-reports)

### What data you get back

Per device:

| Column | Example value | What it means |
|--------|--------------|---------------|
| Device name | LAPTOP-ABC123 | The device |
| Manufacturer | LENOVO | |
| Model | ThinkPad T14 Gen 3 | |
| OS Version | 10.0.19045.4170 | Current OS |
| Readiness status | **High risk** | Overall verdict for this device against target OS |
| Sys req issues | 0 | Hardware requirements met (TPM, CPU, etc.) |
| App issues | 1 | One app with known compatibility problem |
| Driver issues | 2 | **Two drivers with known compatibility problems** |

Drill-down into driver issues for a specific device:

| Driver name | Vendor | Version | Issue |
|------------|--------|---------|-------|
| Intel SST Audio Controller | Intel | 10.29.0.5152 | **Driver won't migrate to new OS** — check with vendor for compatible driver |
| Synaptics Fingerprint Sensor | Synaptics | 5.1.330.26 | **Blocking upgrade** — can't upgrade |

Issue types (from Microsoft's compatibility database):
- **"Driver won't migrate to new OS"** — driver disappears after upgrade; check if Windows Update has a replacement
- **"Blocking upgrade"** — upgrade will fail; driver must be updated or removed first
- **"New driver installed during upgrade"** — Windows Update replaces it automatically; no action needed

Source: [Compatibility report issue descriptions](https://learn.microsoft.com/en-us/intune/device-updates/windows/compatibility-reports#issue-descriptions)

### How it maps to your use case

This is the **"can I actually upgrade this device?"** answer. Combined with the EOL risk from Phase 1:

| Device | EOL risk (Phase 1) | Readiness (Phase 2) | Action |
|--------|-------------------|---------------------|--------|
| LAPTOP-ABC123 | RED — Win 10 past EOL | High risk — 2 driver issues | Fix drivers first, then upgrade |
| DESKTOP-XYZ789 | RED — Win 10 past EOL | Low risk | Safe to push upgrade |
| LAPTOP-DEF456 | AMBER — Win 11 22H2 | Replace device | Hardware can't run target OS — replacement needed |
| LAPTOP-GHI789 | GREEN — Win 11 24H2 | (no check needed) | Already compliant |

---

## STEP 5: Find available driver updates (Phase 2)

### What you're doing
For devices that have driver blockers (from Step 4), finding what newer drivers are available.

### Option A: Windows Autopatch Driver Catalog (drivers on Windows Update)

**How to access:**

1. **Enroll devices in driver management** (one-time per device):
```
POST https://graph.microsoft.com/beta/admin/windows/updates/updatableAssets/enrollAssets
Content-Type: application/json

{
  "updateCategory": "driver",
  "assets": [
    {
      "@odata.type": "#microsoft.graph.windowsUpdates.azureADDevice",
      "id": "{azure-ad-device-id}"
    }
  ]
}
```

2. **Create a deployment audience and add devices:**
```
POST https://graph.microsoft.com/beta/admin/windows/updates/deploymentAudiences
```
Then add members to the audience.

3. **Browse applicable (newer) drivers:**
```
GET https://graph.microsoft.com/beta/admin/windows/updates/deploymentAudiences/{audience-id}/applicableContent?$expand=catalogEntry,matchedDevices
```

Source: [Deploy a driver update using Windows Autopatch](https://learn.microsoft.com/en-us/graph/windowsupdates-manage-driver-update)

**What you get back:**
```json
{
  "catalogEntry": {
    "displayName": "Intel - net - 23.50.0.7",
    "manufacturer": "Intel",
    "driverClass": "Net",
    "version": "23.50.0.7",
    "releaseDateTime": "2024-03-15T00:00:00Z"
  },
  "matchedDevices": [
    { "deviceId": "fb95f07d-...", "recommendedBy": ["Microsoft", "Intel"] }
  ]
}
```

**Covers:** Drivers published to Windows Update by OEMs (Intel, Realtek, NVIDIA, some Lenovo drivers).
**Does NOT cover:** Drivers Lenovo distributes only through Vantage / System Update / Thin Installer.

### Option B: Lenovo Driver Catalog (Lenovo's own repository)

**How to access:**

Fetch the model-specific catalog XML. For a ThinkPad T14 Gen 4 (machine type 21HD):
```
GET https://download.lenovo.com/catalog/21HD_Win11.xml
```

Or use PowerShell:
```powershell
# Using LSUClient (open-source)
Install-Module -Name LSUClient
Get-LSUpdate -Model 21HD

# Using Lenovo's official module
Install-Module -Name Lenovo.Client.Scripting
Find-LnvUpdate -MachineType 21HD
```

Source: [LSUClient docs](https://jantari.github.io/LSUClient-docs/docs/cmdlets/get-lsupdate/) | [Lenovo Client Scripting Module](https://docs.lenovocdrt.com/guides/lcsm/lcsm_top/)

**What you get back:** XML with package entries per model:
```xml
<Package id="n3hf402w">
  <Title>Intel Wireless LAN Driver - 11 (64-bit)</Title>
  <Version>23.50.0.7</Version>
  <Severity>Recommended</Severity>
  <RebootType>3</RebootType>
  <Category>Networking: Wireless LAN</Category>
</Package>
```

**Covers:** ALL drivers Lenovo publishes for that model — including Lenovo-specific ones not on Windows Update.
**Limitation:** Tells you what's available, not whether the current installed version blocks an OS upgrade (that's the compatibility report's job).

### How Options A + B together map to your use case

For a device flagged in Step 4 with a driver blocker:

1. **Compatibility report (Step 4)** says: "Intel SST Audio Controller v10.29.0.5152 — blocks upgrade to 24H2"
2. **Autopatch catalog (Option A)** says: "Intel SST Audio v10.29.00.5714 available on Windows Update for this device"
3. **Or Lenovo catalog (Option B)** says: "Intel SST Audio v10.30.00.5800 available in Lenovo's repository for model 21HD"
4. **Agent decision:** Newer driver exists → update driver → then push OS upgrade

If neither catalog has a newer driver → "Device is on latest available driver but it still blocks the upgrade. Options: wait for OEM fix, stay on current OS (accept security risk), or replace hardware."

---

---

## STEP 0 (Alternative for Phase 1): WUfB Reports — Microsoft Already Partially Solves This

### What you're doing
Before building anything custom, check if Windows Update for Business Reports already gives you the EOS data you need.

### How to access

**Setup (one-time):**
1. Azure Portal → create or pick a Log Analytics workspace
2. Enroll into WUfB Reports: Azure Portal → Monitor → Workbooks → find/set up "Windows Update for Business reports"
3. Configure devices to send data (via Intune policy or script)
4. Source: [Enable WUfB Reports](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-enable)

**Access the workbook:**
1. Azure Portal → Monitor → Workbooks → "Windows Update for Business reports"
2. Feature updates tab → tiles show:
   - **"In service feature update"** — devices on supported OS
   - **"End of service feature update"** — devices on unsupported OS (past EOS)
   - **"Nearing EOS"** — devices within 18 months of EOS
3. **Safeguard holds** chart — devices Microsoft is blocking from upgrading

**Access the raw data (for custom queries):**
1. Azure Portal → Log Analytics workspace → Logs
2. Run KQL queries against the tables:

```kql
// Devices on Windows with their current OS version
UCClient
| where OSFamily == "Windows"
| project DeviceName, OSVersion, OSEdition, OSServicingBranch, OSArchitecture

// Driver update status per device — with OEM and driver name
UCClientUpdateStatus
| where UpdateCategory == "Driver"
| project DeviceName, UpdateDisplayName, UpdateManufacturer, ClientState, ClientSubstate, TimeGenerated

// Driver update failures
UCUpdateAlert
| where UpdateCategory == "Driver"
| project DeviceName, AlertSubtype, ErrorCode, Description, Recommendation, TimeGenerated
```

### What data you get back

**Feature Updates tab (Phase 1 relevance):**
- Count of devices past end of service
- Count of devices nearing EOS (18-month window — you'd need custom KQL for 6 months)
- Safeguard holds — devices Microsoft is blocking from feature updates

**Driver tables (Phase 2 relevance):**
- `UpdateManufacturer`: the OEM (Intel, Lenovo, Synaptics, Realtek, etc.)
- `UpdateDisplayName`: the driver name and version (e.g. "Intel - net - 23.50.0.7")
- `ClientState`: Offering / Installing / Installed / Failed
- `UCUpdateAlert`: error codes + recommendations when driver updates fail

### How it helps your use case

| WUfB Reports gives you | IT Assist feature use |
|------------------------|---------------------|
| Devices past EOS + nearing EOS | Phase 1: at-risk device identification (customize threshold from 18mo → 6mo via KQL) |
| Driver update manufacturer + display name | Phase 2: know which OEM driver is installed, which was offered, whether it installed or failed |
| Driver update failure alerts with error codes | Phase 2: detect failed driver updates, surface error + recommendation to admin |
| Data in Log Analytics (KQL queryable) | Both phases: programmatic access via Azure Monitor API — can feed into IT Assist's natural language query layer |

### What it does NOT give you
- No proactive compatibility prediction ("will this driver block a future OS upgrade?") — that's still the Intune Compatibility Report
- No Lenovo-specific drivers outside Windows Update
- "Nearing EOS" threshold is 18 months in the workbook — not your 6-month requirement (custom query needed)
- No device-level "build → friendly subversion name" mapping — still need the lookup table

---

## Summary: Data Flow Map

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: "Which devices will soon be unsupported?"              │
│                                                                 │
│  Intune Graph API ──→ Device list + OS build number             │
│         +                                                       │
│  MS Lifecycle API ──→ EOL date per subversion/edition           │
│         =                                                       │
│  AT-RISK DEVICE LIST (Red / Amber / Green)                      │
│                                                                 │
│  Data needed:  ✅ Already available via existing Intune APIs     │
│  New setup:    None (just new API queries)                      │
│  Effort:       Low — data join + natural language interface     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: "Can I actually upgrade these devices?"                │
│                                                                 │
│  Intune Compatibility Report ──→ Per-device readiness +         │
│                                  specific driver/app blockers   │
│         +                                                       │
│  Autopatch Driver Catalog ──→ Newer drivers on Windows Update   │
│         +                                                       │
│  Lenovo Driver Catalog ──→ Newer drivers from Lenovo's repo     │
│         =                                                       │
│  UPGRADE PLAN per device:                                       │
│    • Ready → push OS upgrade                                    │
│    • Driver blocker + fix available → update driver, then OS    │
│    • Driver blocker + no fix → wait / accept risk / replace HW  │
│    • Hardware blocker → replace device                          │
│                                                                 │
│  Data needed:  Compatibility report (needs telemetry + toggle)  │
│  New setup:    Tenant toggle (30 sec) + possibly Autopatch      │
│                enrollment (policy decision)                     │
│  Effort:       Medium — multiple data sources + orchestration   │
└─────────────────────────────────────────────────────────────────┘
```
