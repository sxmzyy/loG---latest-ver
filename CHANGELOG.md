# Android Forensic Tool - Changelog

All notable changes to this project will be documented in this file.

---

## [v2.1.0] - 2026-01-20

### 🎉 Production Hardening Release

#### Added
- **Audit Logging System** - Complete chain of custody tracking
  - Logs all user actions with timestamps and IP addresses
  - Session tracking for multi-user environments
  - Export functionality (JSON/CSV)
- **Evidence Hash Verification** - SHA-256 integrity checking
  - Automatic hash generation after extraction
  - Verification system to detect tampering
  - Comprehensive integrity reports
- **Legal Disclaimer Page** - Legal compliance features
  - Authorization requirements
  - GDPR/CCPA compliance notes
  - Prohibited uses documentation
- **System Health Dashboard** - Real-time monitoring
  - ADB connection status
  - Disk space monitoring
  - Hash verification status
  - Audit log health
- **Enhanced Error Handling** - Production-grade reliability
  - Error handler wrapper for Python scripts
  - Detailed error logging
  - User-friendly error messages
- **Comprehensive Documentation** - Professional docs
  - Getting Started guide
  - User Manual with module descriptions
  - Troubleshooting guide
- **API Endpoints** - Programmatic access
  - Hash verification API
  - Audit log export API

#### Changed
- **Orchestrator Improvements** - Better UX
  - Progress indicators ([1/10], [2/10], etc.)
  - Timeout protection (60s per script)
  - Success/failure summary
  - Automatic hash generation post-analysis
- **Sidebar Enhancements** - New navigation
  - System Health link in TOOLS section
  - Legal Disclaimer link in EXPORT section

#### Fixed
- Silent failures in Python scripts
- Missing error feedback for users
- No evidence integrity verification

---

## [v2.0.0] - 2026-01-19

### 🚀 Advanced Forensic Modules Release

#### Added
- **Unified Forensic Timeline** - Merged SMS/Call/Logcat timeline
- **App Privacy & Permission Profiler** - Sensitive permission tracking
- **PII Leak Detector** - Sensitive data exposure detection
- **Network Semantic Analysis** - External connection tracking
- **Social Link Graph** - Communication network visualization (Vis.js)
- **Power Forensics** - Device usage timeline from power events
- **Intent & URL Hunter** - Navigation and deep-link recovery
- **WiFi & Bluetooth Beacon Map** - Location inference
- **Clipboard & Input Reconstruction** - Transient data recovery
- **App Usage Sessionizer** - Forensic screen time analysis

#### Changed
- Enhanced logcat parsing with PID, TID, Priority extraction
- Improved package name attribution across all modules
- Better false-positive filtering in all analyzers

---

## [v1.0.0] - Initial Release

### Core Features
- ADB-based log extraction (Logcat, SMS, Calls, Location)
- Live logcat monitoring
- Timeline visualization
- Threat detection engine
- Filter and search functionality
- AdminLTE-based web interface
- Python GUI for background operations

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes or major feature sets
- **Minor** (2.X.0): New features, backwards compatible
- **Patch** (2.1.X): Bug fixes and minor improvements

---

## Roadmap

### Planned Features
- [ ] PDF report generation with embedded hashes
- [ ] Automated backup system
- [ ] Advanced search across all modules
- [ ] Case management (multiple evidence sets)
- [ ] HTTPS support for remote access
- [ ] Mobile-responsive dashboard
- [ ] Plugin architecture for custom analyzers

---

## Support

For issues or feature requests, review:
- **GETTING_STARTED.md** - Setup and first-use guide
- **USER_MANUAL.md** - Detailed feature documentation
- **TROUBLESHOOTING.md** - Common issues and solutions
