<?php
/**
 * Device Behavior Timeline - Forensic Event Viewer
 * 
 * FORENSIC UI RULES:
 * - Each entry = one logged event
 * - UTC timestamp always visible
 * - SNAPSHOT events labeled
 * - Raw log references clickable
 * - No inference or smoothing
 */

require_once '../includes/header.php';
?>

<style>
.timeline-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

.retention-notice {
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 4px;
    padding: 12px 16px;
    margin-bottom: 20px;
    font-size: 14px;
}

.timeline-filters {
    background: #1e1e1e;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
}

.filter-group {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    align-items: center;
}

.filter-label {
    font-weight: 600;
    color: #a0a0a0;
    margin-right: 10px;
}

.category-filters label {
    margin-right: 15px;
    cursor: pointer;
}

.timeline-events {
    position: relative;
    padding-left: 40px;
}

.timeline-line {
    position: absolute;
    left: 20px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #444;
}

.timeline-event {
    position: relative;
    margin-bottom: 20px;
    background: #1e1e1e;
    border-radius: 8px;
    padding: 16px;
    border-left: 4px solid #666;
    cursor: pointer;
    transition: all 0.2s;
}

.timeline-event:hover {
    background: #252525;
    transform: translateX(4px);
}

.timeline-event.category-DEVICE { border-left-color: #2196F3; }
.timeline-event.category-APP { border-left-color: #4CAF50; }
.timeline-event.category-NETWORK { border-left-color: #9C27B0; }
.timeline-event.category-POWER { border-left-color: #FF9800; }

.timeline-event::before {
    content: '';
    position: absolute;
    left: -46px;
    top: 24px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #666;
    border: 3px solid #0a0a0a;
}

.event-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
}

.event-type {
    font-size: 16px;
    font-weight: 600;
    color: #fff;
}

.event-timestamp {
    font-family: 'Courier New', monospace;
    font-size: 13px;
    color: #a0a0a0;
}

.event-meta {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 8px;
}

.event-badge {
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
}

.badge-category { background: #333; color: #aaa; }
.badge-source { background: #1a4d2e; color: #4ade80; }
.badge-snapshot { background: #854d0e; color: #fbbf24; }
.badge-confidence { background: #1e3a8a; color: #93c5fd; }

.event-details {
    display: none;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #333;
}

.event-details.visible {
    display: block;
}

.detail-row {
    display: flex;
    padding: 6px 0;
    font-size: 13px;
}

.detail-label {
    width: 150px;
    color: #a0a0a0;
    font-weight: 600;
}

.detail-value {
    flex: 1;
    color: #fff;
    font-family: 'Courier New', monospace;
}

.raw-reference {
    color: #60a5fa;
    cursor: pointer;
    text-decoration: underline;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #a0a0a0;
}
</style>

<div class="content-wrapper">
    <div class="timeline-container">
        <h1><i class="fas fa-clock"></i> Device Behavior Timeline</h1>
        <p style="color: #a0a0a0; margin-bottom: 20px;">
            Forensic reconstruction of device events from logcat and dumpsys sources
        </p>

        <!-- RETENTION NOTICE (MANDATORY) -->
        <div class="retention-notice" id="retentionNotice" style="display: none;">
            <strong><i class="fas fa-exclamation-triangle"></i> Retention Limitation:</strong>
            <span id="retentionText"></span>
        </div>

        <!-- Extraction Controls -->
        <div style="margin-bottom: 20px;">
            <button id="extractTimelineBtn" class="btn btn-primary">
                <i class="fas fa-history"></i> Extract Timeline
            </button>
            <button id="refreshBtn" class="btn btn-secondary" style="margin-left: 10px;">
                <i class="fas fa-sync"></i> Refresh
            </button>
        </div>

        <!-- Filters -->
        <div class="timeline-filters">
            <div class="filter-group">
                <span class="filter-label">Categories:</span>
                <div class="category-filters">
                    <label>
                        <input type="checkbox" class="category-filter" value="DEVICE" checked>
                        <i class="fas fa-mobile-alt" style="color: #2196F3;"></i> Device
                    </label>
                    <label>
                        <input type="checkbox" class="category-filter" value="APP" checked>
                        <i class="fas fa-th" style="color: #4CAF50;"></i> App
                    </label>
                    <label>
                        <input type="checkbox" class="category-filter" value="NETWORK" checked>
                        <i class="fas fa-wifi" style="color: #9C27B0;"></i> Network
                    </label>
                    <label>
                        <input type="checkbox" class="category-filter" value="POWER" checked>
                        <i class="fas fa-battery-three-quarters" style="color: #FF9800;"></i> Power
                    </label>
                </div>
            </div>

            <div class="filter-group" style="margin-top: 15px;">
                <span class="filter-label">Time Range:</span>
                <input type="datetime-local" id="timeStart" class="form-control" style="width: 200px;">
                <span style="color: #a0a0a0;">to</span>
                <input type="datetime-local" id="timeEnd" class="form-control" style="width: 200px;">
                <button id="applyFiltersBtn" class="btn btn-sm btn-success">Apply</button>
                <button id="resetFiltersBtn" class="btn btn-sm btn-secondary">Reset</button>
            </div>
        </div>

        <!-- Stats Summary -->
        <div id="statsRow" style="display: none; margin-bottom: 20px;">
            <div style="background: #1e1e1e; border-radius: 8px; padding: 16px;">
                <strong>Total Events:</strong> <span id="totalEvents">0</span> |
                <strong>Device:</strong> <span id="deviceCount">0</span> |
                <strong>App:</strong> <span id="appCount">0</span> |
                <strong>Network:</strong> <span id="networkCount">0</span> |
                <strong>Power:</strong> <span id="powerCount">0</span>
            </div>
        </div>

        <!-- Timeline -->
        <div class="timeline-events">
            <div class="timeline-line"></div>
            <div id="timelineContainer"></div>
        </div>

        <!-- Empty State -->
        <div id="emptyState" class="empty-state">
            <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 16px; display: block;"></i>
            <p>No timeline data available</p>
            <p style="font-size: 14px;">Click "Extract Timeline" to begin</p>
        </div>
    </div>
</div>

<script src="../assets/js/timeline-viewer.js"></script>

<script>
// Initialize timeline viewer
let timelineViewer;

document.addEventListener('DOMContentLoaded', function() {
    timelineViewer = new TimelineViewer('timelineContainer');
    
    // Auto-load if data exists
    timelineViewer.loadTimeline();
    
    // Extract timeline button
    document.getElementById('extractTimelineBtn').addEventListener('click', function() {
        const btn = this;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Extracting...';
        
        fetch('../api/timeline-acquisition.php?action=extract')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`Timeline extraction complete!\n\nTotal events: ${data.total_events}\n\nCheck console for audit log.`);
                    console.log('Extraction Audit Log:', data.audit_log);
                    timelineViewer.loadTimeline();
                } else {
                    // Check if instructions are provided
                    if (data.instructions) {
                        const msg = data.error + '\n\n' + data.instructions.join('\n');
                        alert(msg);
                        console.error('Technical error:', data.technical_error);
                    } else {
                        alert('Error: ' + (data.error || 'Unknown error'));
                        if (data.trace) console.error(data.trace);
                    }
                }
            })
            .catch(error => {
                alert('Error extracting timeline: ' + error.message);
                console.error(error);
            })
            .finally(() => {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-history"></i> Extract Timeline';
            });
    });
    
    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', function() {
        timelineViewer.loadTimeline();
    });
    
    // Filter listeners
    document.querySelectorAll('.category-filter').forEach(cb => {
        cb.addEventListener('change', function() {
            timelineViewer.applyFilters();
        });
    });
    
    document.getElementById('applyFiltersBtn').addEventListener('click', function() {
        timelineViewer.applyFilters();
    });
    
    document.getElementById('resetFiltersBtn').addEventListener('click', function() {
        document.querySelectorAll('.category-filter').forEach(cb => cb.checked = true);
        document.getElementById('timeStart').value = '';
        document.getElementById('timeEnd').value = '';
        timelineViewer.applyFilters();
    });
});
</script>

<?php require_once '../includes/footer.php'; ?>
