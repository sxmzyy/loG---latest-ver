<?php
/**
 * Android Forensic Tool - Live Monitoring Page
 * Real-time logcat streaming with Server-Sent Events
 */
$pageTitle = 'Live Monitor - Android Forensic Tool';
$basePath = '../';
require_once '../includes/header.php';
require_once '../includes/sidebar.php';
?>

<!-- Main Content Wrapper -->
<main class="app-main">
    <!-- Content Header -->
    <div class="app-content-header">
        <div class="container-fluid">
            <div class="row">
                <div class="col-sm-6">
                    <h3 class="mb-0">
                        <i class="fas fa-satellite-dish me-2 text-forensic-blue"></i>Live Monitor
                    </h3>
                </div>
                <div class="col-sm-6">
                    <ol class="breadcrumb float-sm-end">
                        <li class="breadcrumb-item"><a href="../index.php">Home</a></li>
                        <li class="breadcrumb-item active">Live Monitor</li>
                    </ol>
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="app-content">
        <div class="container-fluid">

            <!-- Control Panel -->
            <div class="card mb-4">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-4">
                            <button class="btn btn-success btn-lg" id="startMonitorBtn" onclick="startLiveMonitor()">
                                <i class="fas fa-play me-2"></i>Start Monitoring
                            </button>
                            <button class="btn btn-danger btn-lg ms-2" id="stopMonitorBtn" onclick="stopLiveMonitor()"
                                disabled>
                                <i class="fas fa-stop me-2"></i>Stop
                            </button>
                        </div>
                        <div class="col-md-4 text-center">
                            <span id="monitorStatus" class="fs-5">
                                <i class="fas fa-circle text-secondary me-1"></i> Stopped
                            </span>
                            <br>
                            <small class="text-muted" id="logCount">0 lines captured</small>
                        </div>
                        <div class="col-md-4 text-end">
                            <button class="btn btn-outline-secondary" onclick="clearLiveLog()">
                                <i class="fas fa-eraser me-1"></i>Clear
                            </button>
                            <button class="btn btn-outline-primary" onclick="pauseMonitor()">
                                <i class="fas fa-pause me-1"></i>Pause
                            </button>
                            <button class="btn btn-outline-success" onclick="exportLiveLog()">
                                <i class="fas fa-download me-1"></i>Export
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <!-- Log Console -->
                <div class="col-lg-9">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h3 class="card-title mb-0">
                                <i class="fas fa-terminal me-2"></i>Live Log Output
                            </h3>
                            <div class="input-group" style="width: 300px;">
                                <span class="input-group-text"><i class="fas fa-search"></i></span>
                                <input type="text" class="form-control" id="liveSearch" placeholder="Filter logs..."
                                    onkeyup="filterLiveLogs()">
                            </div>
                        </div>
                        <div class="card-body p-0">
                            <div class="log-viewer" id="liveLogConsole" style="height: 600px;">
                                <div class="log-entry log-info">
                                    <span class="text-muted">[Ready]</span> Click "Start Monitoring" to begin real-time
                                    log capture...
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Filters Sidebar -->
                <div class="col-lg-3">
                    <!-- Log Level Filter -->
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-filter me-2"></i>Log Levels
                            </h3>
                        </div>
                        <div class="card-body">
                            <div class="form-check form-switch mb-2">
                                <input class="form-check-input level-filter" type="checkbox" id="levelV" checked
                                    data-level="V">
                                <label class="form-check-label log-verbose" for="levelV">Verbose</label>
                            </div>
                            <div class="form-check form-switch mb-2">
                                <input class="form-check-input level-filter" type="checkbox" id="levelD" checked
                                    data-level="D">
                                <label class="form-check-label log-debug" for="levelD">Debug</label>
                            </div>
                            <div class="form-check form-switch mb-2">
                                <input class="form-check-input level-filter" type="checkbox" id="levelI" checked
                                    data-level="I">
                                <label class="form-check-label log-info" for="levelI">Info</label>
                            </div>
                            <div class="form-check form-switch mb-2">
                                <input class="form-check-input level-filter" type="checkbox" id="levelW" checked
                                    data-level="W">
                                <label class="form-check-label log-warning" for="levelW">Warning</label>
                            </div>
                            <div class="form-check form-switch mb-2">
                                <input class="form-check-input level-filter" type="checkbox" id="levelE" checked
                                    data-level="E">
                                <label class="form-check-label log-error" for="levelE">Error</label>
                            </div>
                            <div class="form-check form-switch">
                                <input class="form-check-input level-filter" type="checkbox" id="levelF" checked
                                    data-level="F">
                                <label class="form-check-label log-fatal" for="levelF">Fatal</label>
                            </div>
                        </div>
                    </div>

                    <!-- Stats -->
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-chart-bar me-2"></i>Live Stats
                            </h3>
                        </div>
                        <div class="card-body p-0">
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item d-flex justify-content-between">
                                    <span class="text-secondary">Verbose</span>
                                    <span class="badge bg-secondary" id="statV">0</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between">
                                    <span class="text-forensic-blue">Debug</span>
                                    <span class="badge bg-info" id="statD">0</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between">
                                    <span class="text-forensic-cyan">Info</span>
                                    <span class="badge bg-primary" id="statI">0</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between">
                                    <span class="text-warning">Warning</span>
                                    <span class="badge bg-warning" id="statW">0</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between">
                                    <span class="text-danger">Error</span>
                                    <span class="badge bg-danger" id="statE">0</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between">
                                    <span class="text-white bg-danger px-1 rounded">Fatal</span>
                                    <span class="badge bg-dark" id="statF">0</span>
                                </li>
                            </ul>
                        </div>
                    </div>

                            <!-- Options -->
                            <div class="card mb-3">
                                <div class="card-header bg-danger text-white">
                                    <h3 class="card-title">
                                        <i class="fas fa-shield-alt me-2"></i>Threats Detected
                                    </h3>
                                </div>
                                <div class="card-body text-center">
                                    <h1 class="display-4 fw-bold text-danger mb-0" id="liveThreatCount">0</h1>
                                    <small class="text-muted">Suspicious Events</small>
                                </div>
                            </div>

                    <!-- Options -->
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-cog me-2"></i>Options
                            </h3>
                        </div>
                        <div class="card-body">
                            <div class="form-check form-switch mb-2">
                                <input class="form-check-input" type="checkbox" id="autoScrollLive" checked>
                                <label class="form-check-label" for="autoScrollLive">Auto-scroll</label>
                            </div>
                            <div class="form-check form-switch mb-2">
                                <input class="form-check-input" type="checkbox" id="showTimestamp" checked>
                                <label class="form-check-label" for="showTimestamp">Show Timestamps</label>
                            </div>
                            <div class="form-check form-switch mb-2">
                                <input class="form-check-input" type="checkbox" id="highlightErrors" checked>
                                <label class="form-check-label" for="highlightErrors">Highlight Errors</label>
                            </div>
                             <div class="form-check form-switch mb-2">
                                <input class="form-check-input" type="checkbox" id="detectThreats" checked>
                                <label class="form-check-label text-danger" for="detectThreats"><strong>Active Threat Detector</strong></label>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small">Max Lines</label>
                                <select class="form-select form-select-sm" id="maxLines">
                                    <option value="500">500</option>
                                    <option value="1000" selected>1000</option>
                                    <option value="2000">2000</option>
                                    <option value="5000">5000</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</main>

<?php
$additionalScripts = <<<'SCRIPT'
<script>
let isPaused = false;
let logLines = [];
let stats = { V: 0, D: 0, I: 0, W: 0, E: 0, F: 0 };
let totalLines = 0;
let threatCount = 0;

// Simple Regex Signatures for Live Detection
const THREAT_PATTERNS = [
    { regex: /com\.spyzie|com\.mspy|com\.flexispy/i, name: "Spyware Package" },
    { regex: /sms intercept|otp.*listen/i, name: "SMS Listener" },
    { regex: /screen.*capture|record.*audio|keylog/i, name: "Surveillance Activity" },
    { regex: /accessibility.*service.*enabled/i, name: "Accessibility Abuse" },
    { regex: /bank.*overlay|inject.*view/i, name: "Banking Troj" }
];

function startLiveMonitor() {
    if (ForensicApp.state.isMonitoring) return;
    
    ForensicApp.state.isMonitoring = true;
    document.getElementById('startMonitorBtn').disabled = true;
    document.getElementById('stopMonitorBtn').disabled = false;
    document.getElementById('monitorStatus').innerHTML = '<i class="fas fa-circle text-success pulse me-1"></i> Live';
    
    const logConsole = document.getElementById('liveLogConsole');
    appendLiveLine('🟢 Live monitoring started...', 'success');
    
    // Simulate live monitoring (in production, use SSE)
    simulateLiveMonitor();
}

function stopLiveMonitor() {
    ForensicApp.state.isMonitoring = false;
    document.getElementById('startMonitorBtn').disabled = false;
    document.getElementById('stopMonitorBtn').disabled = true;
    document.getElementById('monitorStatus').innerHTML = '<i class="fas fa-circle text-secondary me-1"></i> Stopped';
    
    appendLiveLine('🔴 Live monitoring stopped', 'warning');
    
    if (ForensicApp.state.eventSource) {
        ForensicApp.state.eventSource.close();
        ForensicApp.state.eventSource = null;
    }
}

function pauseMonitor() {
    isPaused = !isPaused;
    const btn = event.target;
    if (isPaused) {
        btn.innerHTML = '<i class="fas fa-play me-1"></i>Resume';
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-warning');
        document.getElementById('monitorStatus').innerHTML = '<i class="fas fa-pause text-warning me-1"></i> Paused';
    } else {
        btn.innerHTML = '<i class="fas fa-pause me-1"></i>Pause';
        btn.classList.remove('btn-warning');
        btn.classList.add('btn-outline-primary');
        document.getElementById('monitorStatus').innerHTML = '<i class="fas fa-circle text-success pulse me-1"></i> Live';
    }
}

function checkThreats(lineContent) {
    if (!document.getElementById('detectThreats').checked) return false;

    for (let pattern of THREAT_PATTERNS) {
        if (pattern.regex.test(lineContent)) {
            threatCount++;
            document.getElementById('liveThreatCount').innerText = threatCount;
            // Flash effect
            const card = document.getElementById('liveThreatCount').closest('.card');
            card.classList.add('border-danger');
            setTimeout(() => card.classList.remove('border-danger'), 500);
            return `🚨 THREAT DETECTED: ${pattern.name}`;
        }
    }
    return null;
}

function simulateLiveMonitor() {
    // Sample log lines for simulation
    const sampleLogs = [
        { level: 'I', tag: 'ActivityManager', msg: 'Start proc com.example.app for activity' },
        { level: 'D', tag: 'ViewRootImpl', msg: 'performTraversals: mFirst=false mWillDraw=true' },
        { level: 'W', tag: 'System', msg: 'A resource failed to call close.' },
        { level: 'E', tag: 'AndroidRuntime', msg: 'FATAL EXCEPTION: main' },
        { level: 'I', tag: 'PackageManager', msg: 'Package installed: com.example.newapp' },
        { level: 'D', tag: 'ConnectivityManager', msg: 'NetworkInfo: type=WIFI, state=CONNECTED' },
        { level: 'V', tag: 'AudioTrack', msg: 'setVolume(0.5, 0.5)' },
        { level: 'I', tag: 'GCMonitor', msg: 'GC_CONCURRENT freed 2MB, 45% free' },
        // Add fake threats for testing
        { level: 'W', tag: 'AccessibilityManager', msg: 'Accessibility Service ENABLED for com.mspy.agent' },
        { level: 'I', tag: 'SMSReceiver', msg: 'OTP detected in incoming SMS, broadcasting...' }
    ];
    
    const interval = setInterval(() => {
        if (!ForensicApp.state.isMonitoring) {
            clearInterval(interval);
            return;
        }
        
        if (isPaused) return;
        
        const log = sampleLogs[Math.floor(Math.random() * sampleLogs.length)];
        const timestamp = new Date().toTimeString().split(' ')[0];
        const line = `${timestamp} ${log.level}/${log.tag}: ${log.msg}`;
        
        appendLiveLine(line, getLevelClass(log.level), log.level);
    }, 500);
}

function appendLiveLine(text, levelClass = 'info', level = 'I') {
    const console = document.getElementById('liveLogConsole');
    const maxLines = parseInt(document.getElementById('maxLines').value);
    
    // Check level filter
    const levelInput = document.querySelector(`.level-filter[data-level="${level}"]`);
    if (levelInput && !levelInput.checked) return;
    
    const line = document.createElement('div');
    line.className = `log-entry log-${levelClass}`;
    line.dataset.level = level;
    
    // THREAT DETECTION HOOK
    const threatMsg = checkThreats(text);
    if (threatMsg) {
        line.innerHTML = `<strong>${threatMsg}</strong><br>` + text;
        line.className += ' bg-danger text-white p-2 mb-1 rounded';
    } else {
        line.textContent = text;
    }

    // Highlight errors
    if (!threatMsg && document.getElementById('highlightErrors').checked && (level === 'E' || level === 'F')) {
        line.style.fontWeight = 'bold';
    }
    
    console.appendChild(line);
    logLines.push({ text, level });
    
    // Update stats
    if (stats[level] !== undefined) {
        stats[level]++;
        document.getElementById('stat' + level).textContent = stats[level];
    }
    
    totalLines++;
    document.getElementById('logCount').textContent = totalLines + ' lines captured';
    
    // Limit lines
    while (console.children.length > maxLines) {
        console.removeChild(console.firstChild);
    }
    
    // Auto-scroll
    if (document.getElementById('autoScrollLive').checked) {
        console.scrollTop = console.scrollHeight;
    }
}

function getLevelClass(level) {
    const classes = { V: 'verbose', D: 'debug', I: 'info', W: 'warning', E: 'error', F: 'critical' };
    return classes[level] || 'info';
}

function clearLiveLog() {
    document.getElementById('liveLogConsole').innerHTML = '';
    logLines = [];
    stats = { V: 0, D: 0, I: 0, W: 0, E: 0, F: 0 };
    totalLines = 0;
    
    Object.keys(stats).forEach(level => {
        document.getElementById('stat' + level).textContent = '0';
    });
    document.getElementById('logCount').textContent = '0 lines captured';
    
    appendLiveLine('Console cleared', 'info');
}

function filterLiveLogs() {
    const searchTerm = document.getElementById('liveSearch').value.toLowerCase();
    document.querySelectorAll('#liveLogConsole .log-entry').forEach(line => {
        const matches = !searchTerm || line.textContent.toLowerCase().includes(searchTerm);
        line.style.display = matches ? '' : 'none';
    });
}

function exportLiveLog() {
    const console = document.getElementById('liveLogConsole');
    const text = console.innerText;
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'live_log_' + new Date().toISOString().slice(0, 10) + '.txt';
    a.click();
    URL.revokeObjectURL(url);
    
    showToast('Log exported successfully', 'success');
}

// Level filter change handler
document.querySelectorAll('.level-filter').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        const level = this.dataset.level;
        document.querySelectorAll(`#liveLogConsole .log-entry[data-level="${level}"]`).forEach(line => {
            line.style.display = this.checked ? '' : 'none';
        });
    });
});
</script>
SCRIPT;

require_once '../includes/footer.php';
?>