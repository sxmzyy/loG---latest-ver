# API Reference

Complete API documentation for the Android Forensic Tool web interface.

---

## 📡 Base URL

```
http://localhost:8000/api/
```

---

## 🔐 Authentication

Currently, no authentication is required. The tool is designed for local forensic workstations.

---

## 📋 Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/device-status.php` | GET | Check device connection |
| `/api/extract.php` | POST | Extract logs from device |
| `/api/filter.php` | POST | Filter log entries |
| `/api/live-stream.php` | GET | Stream logs in real-time |
| `/api/scan-threats.php` | GET | Scan for security threats |
| `/api/stats.php` | GET | Get dashboard statistics |
| `/api/export-report.php` | GET | Generate forensic report |
| `/api/clear-data.php` | POST | Clear extracted data |

---

## 📱 Device Status

### `GET /api/device-status.php`

Check if an Android device is connected via ADB.

**Request**:
```http
GET /api/device-status.php HTTP/1.1
Host: localhost:8000
```

**Response** (Connected):
```json
{
    "connected": true,
    "device_id": "R58N51XXXXX",
    "model": "SM-G991B",
    "android_version": "13",
    "manufacturer": "samsung"
}
```

**Response** (Not Connected):
```json
{
    "connected": false,
    "error": "No device connected"
}
```

**Response** (ADB Not Found):
```json
{
    "connected": false,
    "error": "ADB not found. Please install Android SDK Platform Tools."
}
```

---

## 📥 Log Extraction

### `POST /api/extract.php`

Extract logs from connected Android device.

**Request**:
```http
POST /api/extract.php HTTP/1.1
Host: localhost:8000
Content-Type: application/x-www-form-urlencoded

type=all
```

**Parameters**:

| Parameter | Type | Required | Values | Description |
|-----------|------|----------|--------|-------------|
| `type` | string | Yes | `all`, `logcat`, `calls`, `sms`, `location` | Type of logs to extract |

**Response** (Success):
```json
{
    "success": true,
    "message": "All logs extracted successfully",
    "extraction_time": "2024-01-15T10:30:45Z",
    "stats": {
        "logcat_lines": 12543,
        "call_records": 234,
        "sms_records": 156,
        "location_points": 45
    },
    "buffer_info": {
        "duration_hours": 168.5,
        "duration_days": 7.02,
        "oldest_log": "2024-01-08T10:15:00Z"
    }
}
```

**Response** (Partial Success):
```json
{
    "success": true,
    "message": "Extraction completed with warnings",
    "warnings": [
        "SMS extraction requires root access on this device",
        "Location logs may be incomplete"
    ],
    "stats": {
        "logcat_lines": 12543,
        "call_records": 234,
        "sms_records": 0,
        "location_points": 12
    }
}
```

**Response** (Failure):
```json
{
    "success": false,
    "error": "No device connected",
    "code": "DEVICE_NOT_FOUND"
}
```

**Error Codes**:
| Code | Description |
|------|-------------|
| `DEVICE_NOT_FOUND` | No Android device connected |
| `ADB_NOT_FOUND` | ADB not installed or not in PATH |
| `PERMISSION_DENIED` | Device rejected ADB connection |
| `EXTRACTION_FAILED` | Generic extraction error |

---

## 🔍 Log Filtering

### `POST /api/filter.php`

Filter extracted log entries.

**Request**:
```http
POST /api/filter.php HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "keyword": "error",
    "log_type": "Crash",
    "severity": "E",
    "time_range": "past_24_hours",
    "regex": false,
    "limit": 100,
    "offset": 0
}
```

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keyword` | string | No | `""` | Search keyword |
| `log_type` | string | No | `"all"` | Log category filter |
| `severity` | string | No | `"all"` | Severity filter (V/D/I/W/E/F) |
| `time_range` | string | No | `"all_time"` | Time range filter |
| `regex` | boolean | No | `false` | Enable regex mode |
| `limit` | integer | No | `100` | Max results per page |
| `offset` | integer | No | `0` | Pagination offset |

**Log Type Values**:
- `all` - All log types
- `Application` - App-specific logs
- `System` - System logs
- `Crash` - Crashes and exceptions
- `GC` - Garbage collection
- `Network` - Network activity
- `Broadcast` - Broadcast events
- `Service` - Service lifecycle
- `Device` - Device/hardware

**Time Range Values**:
- `all_time` - No time filter
- `past_1_hour` - Last 1 hour
- `past_24_hours` - Last 24 hours
- `past_7_days` - Last 7 days

**Response**:
```json
{
    "success": true,
    "total_lines": 12543,
    "filtered_count": 234,
    "page": 1,
    "total_pages": 3,
    "results": [
        {
            "line_number": 1523,
            "timestamp": "01-15 10:23:45.123",
            "severity": "E",
            "tag": "AndroidRuntime",
            "content": "FATAL EXCEPTION: main",
            "log_type": "Crash"
        },
        {
            "line_number": 1524,
            "timestamp": "01-15 10:23:45.124",
            "severity": "E",
            "tag": "AndroidRuntime",
            "content": "java.lang.NullPointerException",
            "log_type": "Crash"
        }
    ]
}
```

---

## 📺 Live Streaming

### `GET /api/live-stream.php`

Stream logs in real-time using Server-Sent Events (SSE).

**Request**:
```http
GET /api/live-stream.php HTTP/1.1
Host: localhost:8000
Accept: text/event-stream
```

**Query Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter` | string | No | `""` | Filter keyword |
| `severity` | string | No | `"all"` | Min severity level |

**Response** (SSE Stream):
```
event: connected
data: {"status": "connected", "device": "SM-G991B"}

event: log
data: {"timestamp": "10:23:45.123", "severity": "I", "tag": "ActivityManager", "message": "Start proc 1234:com.example/u0a123"}

event: log
data: {"timestamp": "10:23:45.456", "severity": "W", "tag": "NetworkMonitor", "message": "Network changed"}

event: heartbeat
data: {"timestamp": "2024-01-15T10:23:50Z"}

event: disconnected
data: {"status": "disconnected", "reason": "Device unplugged"}
```

**Event Types**:
| Event | Description |
|-------|-------------|
| `connected` | Connection established |
| `log` | New log entry |
| `heartbeat` | Keep-alive (every 30s) |
| `error` | Error occurred |
| `disconnected` | Device disconnected |

**JavaScript Client Example**:
```javascript
const eventSource = new EventSource('/api/live-stream.php');

eventSource.addEventListener('log', (event) => {
    const log = JSON.parse(event.data);
    console.log(`[${log.severity}] ${log.tag}: ${log.message}`);
});

eventSource.addEventListener('error', () => {
    console.log('Connection lost');
    eventSource.close();
});
```

---

## 🛡️ Threat Scanning

### `GET /api/scan-threats.php`

Scan extracted logs for security threats.

**Request**:
```http
GET /api/scan-threats.php HTTP/1.1
Host: localhost:8000
```

**Query Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `force` | boolean | No | `false` | Force rescan |

**Response**:
```json
{
    "success": true,
    "scan_time": "2024-01-15T10:35:00Z",
    "duration_seconds": 2.34,
    "risk_score": 65,
    "risk_level": "HIGH",
    "summary": {
        "total_threats": 8,
        "critical": 2,
        "high": 3,
        "medium": 2,
        "low": 1
    },
    "threats": [
        {
            "id": 1,
            "type": "malware",
            "category": "Known Malware Package",
            "severity": "critical",
            "description": "Detected known malware: com.spyware.fake",
            "line_number": 4523,
            "content": "I/ActivityManager: Start proc 5678:com.spyware.fake/u0a200",
            "recommendation": "Remove this application immediately"
        },
        {
            "id": 2,
            "type": "network",
            "category": "Data Exfiltration",
            "severity": "high",
            "description": "Suspicious data upload to unknown server",
            "line_number": 5234,
            "content": "D/OkHttp: POST http://malicious.server/upload",
            "recommendation": "Investigate network traffic"
        }
    ],
    "scan_stats": {
        "lines_scanned": 12543,
        "patterns_checked": 45,
        "malware_matches": 2,
        "network_anomalies": 3,
        "privilege_attempts": 2,
        "suspicious_behaviors": 1
    }
}
```

**Risk Levels**:
| Score | Level | Description |
|-------|-------|-------------|
| 0-25 | LOW | Minimal security concerns |
| 26-50 | MEDIUM | Some suspicious activity detected |
| 51-75 | HIGH | Significant security threats |
| 76-100 | CRITICAL | Severe security compromise |

---

## 📊 Dashboard Statistics

### `GET /api/stats.php`

Get dashboard statistics and summaries.

**Request**:
```http
GET /api/stats.php HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
    "success": true,
    "generated_at": "2024-01-15T10:40:00Z",
    "counts": {
        "sms": 156,
        "calls": 234,
        "locations": 45,
        "threats": 8,
        "logcat_lines": 12543
    },
    "last_extraction": "2024-01-15T10:30:45Z",
    "call_breakdown": {
        "incoming": 89,
        "outgoing": 112,
        "missed": 33
    },
    "sms_breakdown": {
        "received": 98,
        "sent": 58
    },
    "recent_activity": [
        {
            "type": "extraction",
            "time": "2024-01-15T10:30:45Z",
            "description": "All logs extracted"
        },
        {
            "type": "scan",
            "time": "2024-01-15T10:35:00Z",
            "description": "Threat scan completed"
        }
    ]
}
```

---

## 📄 Report Export

### `GET /api/export-report.php`

Generate and download forensic report.

**Request**:
```http
GET /api/export-report.php?format=pdf HTTP/1.1
Host: localhost:8000
```

**Query Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `format` | string | No | `"html"` | Output format (`pdf` or `html`) |
| `include` | string | No | `"all"` | Sections to include |

**Include Options** (comma-separated):
- `all` - All sections
- `summary` - Executive summary
- `device` - Device information
- `calls` - Call log analysis
- `sms` - SMS analysis
- `location` - Location data
- `threats` - Threat analysis
- `timeline` - Activity timeline

**Response** (Success):
```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="forensic_report_20240115_103500.pdf"

[PDF Binary Content]
```

**Response** (HTML format):
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Disposition: attachment; filename="forensic_report_20240115_103500.html"

<!DOCTYPE html>
<html>
...
</html>
```

**Response** (Error):
```json
{
    "success": false,
    "error": "No logs available. Please extract logs first.",
    "code": "NO_DATA"
}
```

---

## 🗑️ Clear Data

### `POST /api/clear-data.php`

Clear extracted log data.

**Request**:
```http
POST /api/clear-data.php HTTP/1.1
Host: localhost:8000
Content-Type: application/x-www-form-urlencoded

type=all&confirm=true
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | Yes | Data type to clear |
| `confirm` | boolean | Yes | Must be `true` to confirm |

**Type Values**:
- `all` - All extracted data
- `logcat` - Logcat logs only
- `calls` - Call logs only
- `sms` - SMS logs only
- `location` - Location data only
- `exports` - Generated reports only

**Response**:
```json
{
    "success": true,
    "message": "All data cleared successfully",
    "cleared": {
        "logcat": true,
        "calls": true,
        "sms": true,
        "location": true
    },
    "cleared_at": "2024-01-15T10:45:00Z"
}
```

---

## 🔧 Error Handling

All endpoints return errors in a consistent format:

```json
{
    "success": false,
    "error": "Human-readable error message",
    "code": "ERROR_CODE",
    "details": {
        "additional": "context"
    }
}
```

**Common Error Codes**:

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `DEVICE_NOT_FOUND` | 404 | No device connected |
| `ADB_NOT_FOUND` | 500 | ADB not installed |
| `PERMISSION_DENIED` | 403 | Access denied |
| `INVALID_PARAMETER` | 400 | Bad request parameter |
| `NO_DATA` | 404 | No data available |
| `EXTRACTION_FAILED` | 500 | Extraction error |
| `SCAN_FAILED` | 500 | Threat scan error |
| `INTERNAL_ERROR` | 500 | Server error |

---

## 📝 Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider adding:

```php
// Example rate limiting
$maxRequests = 100;
$timeWindow = 60; // seconds

if (isRateLimited($_SERVER['REMOTE_ADDR'], $maxRequests, $timeWindow)) {
    http_response_code(429);
    echo json_encode(['error' => 'Too many requests']);
    exit;
}
```

---

## 🔄 Pagination

Endpoints returning lists support pagination:

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | `100` | Items per page |
| `offset` | integer | `0` | Skip items |
| `page` | integer | `1` | Page number (alternative) |

**Response includes**:
```json
{
    "pagination": {
        "page": 1,
        "limit": 100,
        "offset": 0,
        "total": 234,
        "total_pages": 3,
        "has_next": true,
        "has_prev": false
    }
}
```

---

## 🧪 Testing the API

### Using cURL

```bash
# Check device status
curl http://localhost:8000/api/device-status.php

# Extract all logs
curl -X POST http://localhost:8000/api/extract.php -d "type=all"

# Filter logs
curl -X POST http://localhost:8000/api/filter.php \
  -H "Content-Type: application/json" \
  -d '{"keyword":"error","severity":"E"}'

# Get stats
curl http://localhost:8000/api/stats.php

# Scan threats
curl http://localhost:8000/api/scan-threats.php

# Export report
curl -O http://localhost:8000/api/export-report.php?format=html
```

### Using JavaScript Fetch

```javascript
// Extract logs
async function extractLogs() {
    const response = await fetch('/api/extract.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'type=all'
    });
    return await response.json();
}

// Filter logs
async function filterLogs(keyword, severity) {
    const response = await fetch('/api/filter.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keyword, severity })
    });
    return await response.json();
}
```
