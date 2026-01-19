# Web Interface Documentation

Complete documentation for the PHP web interface of the Android Forensic Tool.

---

## 🌐 Overview

The web interface provides a modern, responsive dashboard built with:
- **PHP 8+** - Backend processing
- **AdminLTE 4** - UI framework (Bootstrap 5)
- **Chart.js** - Data visualization
- **Leaflet.js** - Map integration
- **Font Awesome 6** - Icons

---

## 📁 Directory Structure

```
web/
├── index.php              # Main dashboard
├── includes/
│   ├── config.php         # Configuration
│   ├── header.php         # HTML head section
│   ├── sidebar.php        # Navigation sidebar
│   └── footer.php         # Footer + scripts
├── api/
│   ├── clear-data.php     # Clear extracted data
│   ├── device-status.php  # Check device connection
│   ├── export-report.php  # Generate reports
│   ├── extract.php        # Extract logs from device
│   ├── filter.php         # Filter logs
│   ├── live-stream.php    # Real-time log streaming
│   ├── scan-threats.php   # Threat analysis
│   └── stats.php          # Dashboard statistics
├── pages/
│   ├── call-logs.php      # Call history viewer
│   ├── extract-logs.php   # Log extraction page
│   ├── filter-logs.php    # Log filtering interface
│   ├── graphs.php         # Data visualization
│   ├── live-monitor.php   # Real-time monitoring
│   ├── location.php       # Location data + map
│   ├── logcat.php         # Logcat viewer
│   ├── sms-messages.php   # SMS viewer
│   └── threats.php        # Threat analysis page
└── assets/
    ├── css/
    │   └── custom.css     # Custom styles
    └── js/
        └── custom.js      # Custom JavaScript
```

---

## 📄 Include Files

### `includes/config.php`

**Purpose**: Central configuration matching Python `config.py`.

**Key Constants**:
```php
define('DEBUG_MODE', true);
define('BASE_PATH', dirname(__DIR__));
define('LOGS_PATH', dirname(BASE_PATH) . '/logs');
define('APP_NAME', 'Android Forensic Tool');
define('APP_VERSION', '2.0.0');
```

**Arrays**:
- `$THEME` - Color palette
- `$LOG_TYPES` - Log type patterns with icons/colors
- `$SEVERITY_LEVELS` - Log severity configuration
- `$TIME_RANGES` - Time filter options

**Helper Functions**:
| Function | Returns | Description |
|----------|---------|-------------|
| `getLogsPath()` | `string` | Get resolved logs directory path |
| `readLogFile($filename)` | `string` | Safely read log file contents |
| `getCurrentPage()` | `string` | Get current page for menu highlighting |

---

### `includes/header.php`

**Purpose**: HTML head section and navigation bar.

**Included Resources**:
- AdminLTE CSS
- Bootstrap 5
- Font Awesome 6
- Chart.js
- Custom CSS

**Variables Expected**:
- `$pageTitle` - Page title
- `$basePath` - Relative path to web root

---

### `includes/sidebar.php`

**Purpose**: Left navigation sidebar.

**Menu Structure**:
```
📊 Dashboard
├── Extract Logs
├── Filter Logs
├── Live Monitor
├── Logcat Viewer
├── SMS Messages
├── Call Logs
├── Location Data
├── Graphs
└── Threats
```

---

### `includes/footer.php`

**Purpose**: Footer and JavaScript includes.

**Included Scripts**:
- Bootstrap Bundle
- AdminLTE JS
- Chart.js
- Leaflet.js (maps)
- Custom JS

---

## 📊 Dashboard (`index.php`)

**Purpose**: Main landing page with KPI overview.

**Key Sections**:

1. **KPI Small Boxes**:
   - Total SMS messages
   - Total call records
   - Location points
   - Threats detected

2. **Quick Actions Card**:
   - Extract Logs button
   - Scan Threats button
   - Clear Data button

3. **Device Information Card**:
   - Connection status
   - Device model
   - Android version

4. **Charts**:
   - Call Type Distribution (pie chart)
   - Log Activity Timeline (line chart)

**Server-Side Function**:
```php
function getStats() {
    // Returns array with:
    // - smsCount, callCount, locationCount, threatCount
    // - lastExtraction timestamp
}
```

---

## 📄 Feature Pages (`pages/`)

### `extract-logs.php`

**Purpose**: Extract logs from connected Android device.

**Features**:
- Device connection status indicator
- Extract All Logs button
- Individual extraction options (Logcat, Calls, SMS, Location)
- Progress indicator
- Extraction results display

**API Calls**:
- `GET api/device-status.php` - Check connection
- `POST api/extract.php` - Perform extraction

---

### `filter-logs.php`

**Purpose**: Advanced log filtering interface.

**Filter Options**:
- Keyword search
- Log type selection
- Severity level
- Time range
- Regular expression support

**API Calls**:
- `POST api/filter.php` - Apply filters

---

### `live-monitor.php`

**Purpose**: Real-time logcat streaming.

**Features**:
- Start/Stop monitoring buttons
- Auto-scroll toggle
- Log type color coding
- Search within stream
- Pause/Resume

**Technology**:
- Server-Sent Events (SSE) via `api/live-stream.php`
- Or long-polling fallback

---

### `logcat.php`

**Purpose**: View and analyze extracted logcat.

**Features**:
- Paginated log display
- Syntax highlighting by severity
- Search/filter within page
- Jump to line
- Export options

---

### `sms-messages.php`

**Purpose**: SMS message viewer.

**Features**:
- Sortable table (date, contact, type)
- Type filter (Sent/Received)
- Contact search
- Message preview
- Export to CSV

**Table Columns**:
| Column | Description |
|--------|-------------|
| Date | Message date |
| Time | Message time |
| Contact | Phone number |
| Type | Sent/Received |
| Message | Content preview |

---

### `call-logs.php`

**Purpose**: Call history viewer.

**Features**:
- Sortable table
- Type filter (Incoming/Outgoing/Missed)
- Duration statistics
- Frequent callers chart
- Export to CSV

**Table Columns**:
| Column | Description |
|--------|-------------|
| Date | Call date |
| Time | Call time |
| Contact | Phone number |
| Type | Incoming/Outgoing/Missed |
| Duration | Call length |

---

### `location.php`

**Purpose**: Location data viewer with map.

**Features**:
- Interactive Leaflet map
- Location markers with popups
- Provider filter (GPS/Network/Fused)
- Timeline view
- Accuracy indicators

**Map Integration**:
```javascript
// Leaflet.js map initialization
var map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Add location markers
locations.forEach(loc => {
    L.marker([loc.lat, loc.lng])
        .bindPopup(`<b>${loc.provider}</b><br>${loc.time}`)
        .addTo(map);
});
```

---

### `graphs.php`

**Purpose**: Data visualization page.

**Charts Available**:
1. **Log Activity Over Time** - Line chart of log frequency
2. **Log Type Distribution** - Pie chart by category
3. **Severity Distribution** - Bar chart by level
4. **Call Type Analysis** - Pie chart (Incoming/Outgoing/Missed)
5. **Top Callers** - Horizontal bar chart
6. **Activity Heatmap** - Hour/day activity matrix

---

### `threats.php`

**Purpose**: Security threat analysis.

**Features**:
- Risk score gauge (0-100)
- Risk level indicator (Low/Medium/High/Critical)
- Threat list by category
- Detailed threat descriptions
- Line number references
- Export threat report

**API Calls**:
- `GET api/scan-threats.php` - Run threat scan

---

## 🔌 API Endpoints (`api/`)

### `device-status.php`

**Method**: GET

**Response**:
```json
{
    "connected": true,
    "device_id": "XXXXXX",
    "model": "Pixel 5",
    "android_version": "12"
}
```

---

### `extract.php`

**Method**: POST

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | "all", "logcat", "calls", "sms", "location" |

**Response**:
```json
{
    "success": true,
    "message": "Logs extracted successfully",
    "stats": {
        "logcat_lines": 5234,
        "call_records": 156,
        "sms_records": 89,
        "location_points": 23
    }
}
```

---

### `filter.php`

**Method**: POST

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `keyword` | string | Search keyword |
| `log_type` | string | Log category filter |
| `severity` | string | V/D/I/W/E/F |
| `time_range` | string | Time filter |
| `regex` | boolean | Use regex mode |

**Response**:
```json
{
    "success": true,
    "total_lines": 1234,
    "filtered_lines": 89,
    "results": [
        {"line": 1, "content": "...", "severity": "E"},
        ...
    ]
}
```

---

### `live-stream.php`

**Method**: GET (Server-Sent Events)

**Response Format** (SSE):
```
event: log
data: {"timestamp":"12:34:56","severity":"I","tag":"System","message":"..."}

event: status
data: {"connected":true}
```

---

### `scan-threats.php`

**Method**: GET

**Response**:
```json
{
    "success": true,
    "risk_score": 45,
    "risk_level": "MEDIUM",
    "threats": [
        {
            "type": "network",
            "severity": "high",
            "description": "Suspicious network activity",
            "line_number": 1234,
            "content": "..."
        }
    ],
    "scan_stats": {
        "lines_scanned": 5000,
        "malware_checks": 5000,
        "threats_found": 3
    }
}
```

---

### `stats.php`

**Method**: GET

**Response**:
```json
{
    "sms_count": 89,
    "call_count": 156,
    "location_count": 23,
    "threat_count": 3,
    "logcat_lines": 5234,
    "last_extraction": "2024-01-15T10:30:00Z"
}
```

---

### `export-report.php`

**Method**: GET

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `format` | string | "pdf" or "html" |

**Response**: File download or JSON error

---

### `clear-data.php`

**Method**: POST

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | "all", "logcat", "calls", "sms", "location" |

**Response**:
```json
{
    "success": true,
    "message": "Data cleared successfully"
}
```

---

## 🎨 Custom Assets

### `assets/css/custom.css`

**Purpose**: Custom styling for forensic theme.

**Key Styles**:
```css
/* Forensic color palette */
:root {
    --forensic-primary: #1e1e2e;
    --forensic-accent: #89b4fa;
    --forensic-success: #a6e3a1;
    --forensic-warning: #fab387;
    --forensic-danger: #f38ba8;
}

/* Custom small boxes */
.small-box.bg-forensic-blue { ... }
.small-box.bg-forensic-orange { ... }
.small-box.bg-forensic-red { ... }

/* Log severity colors */
.log-verbose { color: var(--bs-secondary); }
.log-debug { color: var(--bs-info); }
.log-info { color: var(--bs-primary); }
.log-warning { color: var(--bs-warning); }
.log-error { color: var(--bs-danger); }
.log-fatal { color: #dc3545; font-weight: bold; }
```

---

### `assets/js/custom.js`

**Purpose**: Custom JavaScript functionality.

**Key Functions**:
```javascript
// Device status checker
function checkDeviceStatus() { ... }

// Log extraction
function extractLogs(type) { ... }

// Live monitoring
function startMonitoring() { ... }
function stopMonitoring() { ... }

// Chart initialization
function initializeCharts() { ... }

// Map helper functions
function initializeMap() { ... }
function addLocationMarkers(locations) { ... }
```

---

## 🚀 Running the Web Interface

### Development Server

```bash
cd web
php -S localhost:8000
```

Then open http://localhost:8000 in your browser.

### Production Deployment

For production, use a proper web server:

**Apache** (`.htaccess`):
```apache
RewriteEngine On
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.php [L]
```

**Nginx**:
```nginx
location / {
    try_files $uri $uri/ /index.php?$query_string;
}

location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
}
```

---

## 📋 Requirements

- PHP 8.0+
- Python 3.8+ (for ADB operations)
- ADB in PATH
- Write access to `logs/` directory

**PHP Extensions**:
- `json`
- `mbstring`
- `fileinfo`

---

## 🔒 Security Notes

1. **Local Access Only**: By default, PHP dev server only accepts localhost connections
2. **No Authentication**: Tool assumes physical access means authorization
3. **File Access**: PHP has read/write access to logs directory
4. **ADB Commands**: Executed via Python scripts, not directly from PHP
