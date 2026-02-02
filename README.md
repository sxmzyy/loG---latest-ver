# Android Forensic Tool

<div align="center">

**Professional Android device forensic analysis with comprehensive log extraction and intelligence modules**

![Version](https://img.shields.io/badge/version-v2.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![PHP](https://img.shields.io/badge/PHP-8%2B-purple)

</div>

---

## 📋 Overview

The Android Forensic Tool is a production-ready forensic analysis platform designed for law enforcement, corporate security, and digital forensic professionals. It extracts comprehensive data from Android devices and provides 10 advanced intelligence modules with built-in chain of custody tracking and evidence integrity verification.

### ✨ Key Features

- **🔍 10 Forensic Intelligence Modules** - Timeline, Privacy, Network, PII, Social Graph, Power Usage, Intents, Beacons, Clipboard, App Sessions
- **🔒 Evidence Integrity** - SHA-256 hash verification for court admissibility
- **📝 Audit Logging** - Complete chain of custody tracking
- **⚖️ Legal Compliance** - Built-in disclaimer and authorization warnings
- **📊 Professional UI** - AdminLTE-based web interface with real-time updates
- **🏥 System Health** - Real-time monitoring and diagnostics
- **📚 Comprehensive Docs** - Getting Started, User Manual, Troubleshooting

---

## 🚀 Quick Start

### Prerequisites

- **Windows 10+** (macOS/Linux compatible with minor modifications)
- **Python 3.7+** with pip
- **ADB (Android Debug Bridge)** installed and in PATH
- **PHP 8.0+** (bundled in project)
- **Android device** with USB Debugging enabled

### Installation

1. **Clone the repository**
   ```powershell
   git clone <repository-url>
   cd loG---latest-ver
   ```

2. **Install Python dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Verify ADB is installed**
   ```powershell
   adb version
   ```
   If not installed, download from [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)

4. **Enable USB Debugging on device**
   - Settings → About Phone → Tap "Build Number" 7 times
   - Settings → Developer Options → Enable "USB Debugging"
   - Connect device and authorize computer

### Running the Tool

1. **Start Python GUI** (background log extraction)
   ```powershell
   python main.py
   ```

2. **Start Web Server** (in new terminal)
   ```powershell
   powershell -ExecutionPolicy Bypass -File start-server.ps1
   ```

3. **Access Web Interface**
   ```
   http://127.0.0.1:8080
   ```

4. **Extract Logs**
   - Navigate to "Extract Logs" in sidebar
   - Select data types (Logcat, SMS, Calls, Location)
   - Click "Start Extraction"
   - Wait for completion

5. **View Forensic Intelligence**
   - All modules auto-populate after extraction
   - Navigate via sidebar under "FORENSIC INTELLIGENCE"

---

## 📦 Project Structure

```
loG---latest-ver/
├── analysis/              # Python forensic analysis scripts
│   ├── unified_timeline.py
│   ├── privacy_analyzer.py
│   ├── pii_detector.py
│   ├── network_analyzer.py
│   ├── social_graph.py
│   ├── power_forensics.py
│   ├── intent_hunter.py
│   ├── beacon_map.py
│   ├── clipboard_forensics.py
│   ├── app_sessionizer.py
│   ├── evidence_hasher.py  # Hash verification
│   ├── run_analysis.py     # Orchestrator
│   └── generate_sample_data.py  # Test data generator
├── web/                   # PHP web interface
│   ├── pages/            # Forensic module pages
│   ├── includes/         # PHP components
│   ├── assets/           # CSS/JS/images
│   └── api/              # API endpoints
├── logs/                  # Extracted data (created at runtime)
├── docs/                  # Documentation
│   ├── GETTING_STARTED.md
│   ├── USER_MANUAL.md
│   └── TROUBLESHOOTING.md
├── php/                   # Bundled PHP runtime
├── main.py               # Python GUI launcher
├── start-server.ps1      # Web server launcher
├── requirements.txt      # Python dependencies
└── CHANGELOG.md          # Version history
```

---

## 🔍 Forensic Modules

| Module | Purpose | Key Features |
|--------|---------|--------------|
| **Advanced Timeline** | Unified event timeline | Merges SMS/Calls/Logcat chronologically |
| **Privacy Profiler** | Permission tracking | Monitors Location, Camera, Mic, Contacts access |
| **Network Intelligence** | External connections | IPs, domains, frequency analysis |
| **PII Leak Detector** | Sensitive data exposure | Emails, tokens, GPS, API keys, credentials |
| **Social Link Graph** | Communication network | Interactive Vis.js graph visualization |
| **Power Forensics** | Device usage patterns | Screen on/off, charging, usage timeline |
| **Intent & URL Hunter** | Navigation recovery | Browser history, maps, deep links |
| **Beacon Map** | Location inference | WiFi SSIDs, Bluetooth devices, frequency |
| **Clipboard Recovery** | Transient data | Copied text, keyboard suggestions, 2FA codes |
| **App Sessionizer** | Screen time analysis | Precise app usage durations (to-the-second) |

---

## ⚖️ Legal & Compliance

### ⚠️ **IMPORTANT: Legal Authorization Required**

You **MUST** have one of the following before using this tool:
- Valid court order or search warrant
- Written consent from device owner
- Corporate authorization (company-owned device)
- Parental/guardian rights (minor's device)

**Unauthorized access to devices is a federal crime in most jurisdictions.**

### Chain of Custody Features

✅ **Audit Trail** - All actions logged with timestamps and IP addresses  
✅ **Hash Verification** - SHA-256 cryptographic integrity checking  
✅ **Legal Disclaimer** - Built-in warnings and authorization requirements  
✅ **Evidence Metadata** - Complete file provenance tracking  

Access the Legal Disclaimer via: **Web Interface → Sidebar → Legal Disclaimer**

---

## 📊 System Health Monitoring

The built-in **System Health** dashboard provides real-time diagnostics:

- ✅ ADB connection status
- ✅ Disk space monitoring
- ✅ Python availability
- ✅ Log file status
- ✅ Hash verification results
- ✅ Audit log health

---

## 🔒 Evidence Integrity Workflow

### 1. Generate Hashes (After Extraction)
Automatic after each extraction, or manually:
```powershell
cd analysis
python evidence_hasher.py hash
```

### 2. Verify Integrity (Before Court Presentation)
Via web interface:
- System Health → Verify Hashes button

Or command line:
```powershell
python evidence_hasher.py verify
```

### 3. Export Audit Log
System Health → Export Audit Log (JSON or CSV)

---

## 🧪 Testing & Demo

### Generate Sample Data

For testing or demonstration without a real device:

```powershell
cd analysis
python generate_sample_data.py
```

This creates realistic test data for all 10 forensic modules.

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[Getting Started](docs/GETTING_STARTED.md)** | 5-minute quick start guide |
| **[User Manual](docs/USER_MANUAL.md)** | Complete feature reference |
| **[Troubleshooting](docs/TROUBLESHOOTING.md)** | Common issues and solutions |
| **[Changelog](CHANGELOG.md)** | Version history and updates |

---

## 🐛 Troubleshooting

**Device not detected?**
```powershell
adb kill-server
adb start-server
adb devices
```

**Python dependencies missing?**
```powershell
pip install -r requirements.txt
```

**Web interface won't load?**
- Check if PHP server is running
- Verify port 8080 is not in use
- Run as Administrator if needed

For detailed solutions, see [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 🔄 Updating

1. Pull latest changes:
   ```powershell
   git pull origin main
   ```

2. Update dependencies:
   ```powershell
   pip install -r requirements.txt --upgrade
   ```

3. Check CHANGELOG.md for breaking changes

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## ⚠️ Disclaimer

This software is provided "AS IS" without warranty of any kind. The developers are **not liable** for:
- Misuse of the tool for illegal purposes
- Data loss or corruption during extraction
- Legal consequences arising from unauthorized use
- Inaccuracies in analysis results

**Use responsibly and ethically.**

---

## 📞 Support

- **Documentation**: Check `docs/` folder
- **System Health**: Use built-in health dashboard
- **Error Logs**: Review `logs/error_log.json`
- **Issues**: Create GitHub issue with reproduction steps

---

## 🙏 Acknowledgments

- **AdminLTE** - UI framework
- **Vis.js** - Network graph visualization
- **Chart.js** - Data visualization
- **Android Debug Bridge** - Device communication

---

<div align="center">

**⭐ Star this repo if it helped your forensic investigation! ⭐**

Made with ❤️ for digital forensic professionals

</div>
