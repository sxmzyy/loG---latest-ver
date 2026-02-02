# Android Forensic Tool - User Manual

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Core Features](#core-features)
3. [Forensic Intelligence Modules](#forensic-intelligence-modules)
4. [Evidence Management](#evidence-management)
5. [Best Practices](#best-practices)

---

## System Overview

The Android Forensic Tool is a comprehensive solution for extracting, analyzing, and presenting digital evidence from Android devices. It combines Python-based log extraction with a professional web interface for visualization and reporting.

### Architecture

```
Android Device (via ADB)
    ↓
Python Extraction Scripts (main.py)
    ↓
Raw Log Files (logs/*.txt)
    ↓
Python Analysis Scripts (analysis/*.py)
    ↓
Structured JSON Data (logs/*.json)
    ↓
PHP Web Interface (web/pages/*.php)
    ↓
User (Browser)
```

---

## Core Features

### 1. Log Extraction

**Location**: Sidebar → Extract Logs

**What it does**: Connects to the device via ADB and extracts:
- **Logcat**: System logs with timestamps
- **SMS Messages**: Complete message history
- **Call Logs**: Incoming, outgoing, and missed calls
- **Location Data**: GPS coordinates and cell tower info

**How to use**:
1. Ensure device is connected (check System Health)
2. Navigate to "Extract Logs"
3. Select data types to extract
4. Click "Start Extraction"
5. Wait for completion confirmation

**Output**: Raw `.txt` files in `logs/` directory

### 2. Live Monitor

**Location**: Sidebar → Live Monitor

**What it does**: Real-time streaming of device logcat

**How to use**:
1. Click "Start Monitoring"
2. Log messages appear in real-time
3. Use filters to focus on specific priority levels or tags
4. Click "Stop Monitoring" when done

**Use cases**:
- Monitor app behavior during testing
- Capture crash logs as they occur
- Observe network requests in real-time

### 3. Filter Logs

**Location**: Sidebar → Tools → Filter Logs

**What it does**: Search and filter extracted logcat by:
- Time range
- Priority level (Verbose, Debug, Info, Warning, Error, Fatal)
- Tag/Package name
- Text content

**How to use**:
1. Select filters (time, priority, search term)
2. Click "Apply Filters"
3. Export filtered results if needed

---

## Forensic Intelligence Modules

### 1. Advanced Timeline

**Purpose**: Unified chronological view of all events (SMS, Calls, Logcat)

**Key Features**:
- Merged timeline from multiple sources
- Color-coded event types
- Clickable events for detailed view
- Export timeline for documentation

**Forensic Value**: Establish sequence of events for incident reconstruction

**How to interpret**:
- Blue = Logcat event
- Green = SMS message
- Orange = Phone call
- Look for clusters of activity around critical times

---

### 2. Privacy Profiler

**Purpose**: Identify apps accessing sensitive permissions

**Monitored Categories**:
- 📍 Location
- 📷 Camera
- 🎤 Microphone
- 📇 Contacts
- 👆 Biometrics (fingerprint/face)
- 📋 Clipboard

**Key Features**:
- App attribution (shows which package accessed what)
- Frequency counts
- Raw log evidence

**Forensic Value**: Prove unauthorized surveillance or privacy violations

**Red flags**:
- Unknown apps accessing location
- Excessive microphone access
- Apps reading clipboard frequently

---

### 3. Network Intelligence

**Purpose**: External IP addresses and domains contacted by the device

**What it detects**:
- IP addresses (IPv4 and IPv6)
- Domain names
- Hit frequency (how many times each connection occurred)

**Key Features**:
- Filters out system domains (android.com, google.com)
- Shows last context (when the connection was made)
- Sortable by frequency

**Forensic Value**: Identify C&C servers, data exfiltration, or suspicious connections

**Red flags**:
- Unknown foreign IPs
- Tor/VPN endpoints
- Rapid-fire connections to same host

---

### 4. PII Leak Detector

**Purpose**: Scan for personally identifiable information in logs

**Detected Types**:
- Email addresses
- Auth/Bearer tokens
- GPS coordinates
- API/Secret keys
- Passwords (pattern matching)
- IMEI/Device IDs

**Key Features**:
- Automatic sensitive data highlighting
- Line number reference
- Raw log evidence
- False positive filtering (ignores common noise)

**Forensic Value**: Prove data mishandling or security vulnerabilities

**Critical**: Review all findings - some may be test data or false positives

---

### 5. Social Link Graph

**Purpose**: Visualize communication network

**What it shows**:
- Interactive graph
- Device as center node
- Contacts as peripheral nodes
- Edge thickness = communication frequency

**Key Features**:
- Zoom and pan controls
- Click nodes for details
- Identify communication clusters

**Forensic Value**: Identify key contacts or suspicious communication patterns

**How to interpret**:
- Thick lines = frequent communication
- Isolated nodes = rarely contacted
- Clusters = groups of connected individuals

---

### 6. Power Forensics

**Purpose**: Reconstruct physical device usage timeline

**Events Tracked**:
- Screen ON/OFF
- User Present (device unlocked)
- Charging (AC/USB)
- Battery unplugged
- Device shutdown/boot

**Key Features**:
- Timeline chart showing device states
- Duration calculations
- Event log with timestamps

**Forensic Value**: Establish if device was actively used during critical time

**Use cases**:
- Alibi verification ("Device was idle during the incident")
- Usage pattern analysis
- Battery forensics

---

### 7. Intent & URL Hunter

**Purpose**: Recover user navigation and app deep links

**What it captures**:
- Android Intents (VIEW, SEARCH, SEND, etc.)
- URLs (http, https, content, file)
- App component launches
- Deep link activations

**Key Features**:
- Clickable URLs (open in new tab)
- Intent action and data displayed
- Raw log evidence

**Forensic Value**: Recover browsing history, map searches, intent-based evidence

**Examples**:
- Google Maps navigation to specific address
- Browser searches not in history
- App-to-app data sharing

---

### 8. WiFi & Bluetooth Beacon Map

**Purpose**: Location inference via network signatures

**What it detects**:
- WiFi SSIDs (networks the device connected to or scanned)
- Bluetooth devices (MAC addresses and names)
- Connection frequency
- First/last seen timestamps

**Key Features**:
- Sortable by frequency
- Context viewer (raw logs)
- Deduplication

**Forensic Value**: Prove physical presence at locations

**Examples**:
- "Device connected to 'Starbucks_Guest' 10 times" = Regular visits
- Home WiFi SSID establishes residence
- Car Bluetooth proves vehicle ownership

---

### 9. Clipboard Recovery

**Purpose**: Recover transient clipboard data

**What it captures**:
- Copied text (ClipboardService logs)
- Input method activity (keyboard suggestions, text length)
- Package attribution

**Key Features**:
- Automatic sensitive data detection (passwords, OTPs, CVV)
- Red highlighting for sensitive items
- Separate clipboard and IME tabs

**Forensic Value**: Recover critical transient data

**Examples**:
- 2FA codes
- Copied passwords
- Crypto wallet addresses
- Confidential messages

**WARNING**: Very sensitive - handle with care

---

### 10. App Usage Sessionizer

**Purpose**: Forensic screen time analysis

**What it calculates**:
- App foreground durations (precise to the second)
- Session count per app
- Average session length
- First and last use timestamps

**Key Features**:
- Bar chart of top apps
- Detailed session log
- Total screen time

**Forensic Value**: Establish app usage patterns

**Examples**:
- "Suspect used WhatsApp for 45 minutes starting at 10:12 PM"
- "Gambling app usage correlates with financial losses"
- "Social media addiction pattern"

---

## Evidence Management

### Chain of Custody

**Required Steps**:
1. Document authorization (court order, consent, etc.)
2. Extract logs with audit trail enabled
3. Generate SHA-256 hashes immediately after extraction
4. Store original files in write-protected location
5. Work only with copies for analysis
6. Verify hashes before court presentation
7. Export audit log with evidence package

### Hash Verification Workflow

**When to generate hashes**:
- Immediately after extraction
- After each analysis session

**When to verify hashes**:
- Before analysis (daily, if long investigation)
- Before exporting reports
- Before court presentation

**Command**:
```powershell
cd analysis
python evidence_hasher.py verify
```

**Interpreting results**:
- ✅ All verified = Evidence integrity maintained
- ✗ Tampered = Investigate immediately, may indicate:
  - Accidental file modification
  - Malicious tampering
  - Disk corruption

### Audit Trail

**What is logged**:
- Every page view
- All extractions
- Analysis runs
- Exports and downloads
- System errors

**How to access**:
- System Health → Export Audit Log
- File location: `logs/audit_log.json`

**What to include in court package**:
- Full audit log (JSON or CSV)
- Hash verification report
- Integrity certificate

---

## Best Practices

### DO:
✅ Always verify legal authorization first
✅ Generate hashes immediately after extraction
✅ Document every step with screenshots
✅ Export audit logs with evidence
✅ Use System Health before critical operations
✅ Keep multiple backups in encrypted storage
✅ Verify hashes before every court presentation
✅ Review Legal Disclaimer regularly

### DON'T:
❌ Modify original extracted files
❌ Run analysis without hash backup
❌ Delete audit logs
❌ Share evidence via unsecured channels
❌ Analyze devices without authorization
❌ Trust results without verification
❌ Forget to document chain of custody

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Dashboard | Alt+D |
| Extract Logs | Alt+E |
| System Health | Alt+H |
| Legal Disclaimer | Alt+L |

---

## File Locations

| Type | Location |
|------|----------|
| Raw Logs | `logs/*.txt` |
| Analysis Results | `logs/*.json` |
| Audit Trail | `logs/audit_log.json` |
| Hash Metadata | `logs/evidence_metadata.json` |
| Error Log | `logs/error_log.json` |

---

## Support & Resources

- **Getting Started Guide**: `docs/GETTING_STARTED.md`
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`
- **Legal Disclaimer**: Web interface → Sidebar → Legal Disclaimer
- **System Status**: Web interface → System Health

---

**Remember**: This tool is only as reliable as its operator. Always follow proper forensic procedures and legal requirements.
