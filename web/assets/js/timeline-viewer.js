/**
 * TimelineViewer - Forensic Event Timeline UI
 * 
 * FORENSIC UI RULES:
 * - Each DOM entry = one logged event
 * - No visual compression of time gaps
 * - UTC timestamp always shown
 * - Raw log references must be accessible
 * - SNAPSHOT events clearly labeled
 */

class TimelineViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.emptyState = document.getElementById('emptyState');
        this.statsRow = document.getElementById('statsRow');
        this.retentionNotice = document.getElementById('retentionNotice');
        this.retentionText = document.getElementById('retentionText');

        this.allEvents = [];
        this.filteredEvents = [];
    }

    /**
     * Load timeline from API
     */
    async loadTimeline() {
        try {
            const response = await fetch('../api/timeline-acquisition.php?action=get_events');
            const data = await response.json();

            if (!data.success) {
                this.showError(data.error || 'Failed to load timeline');
                return;
            }

            this.allEvents = data.events || [];
            this.filteredEvents = this.allEvents;

            // Show retention notice (MANDATORY)
            if (data.retention_notice) {
                this.retentionText.textContent = data.retention_notice;
                this.retentionNotice.style.display = 'block';
            }

            this.displayStats(data.category_breakdown || {});
            this.renderTimeline();

        } catch (error) {
            this.showError('Error loading timeline: ' + error.message);
        }
    }

    /**
     * Display statistics
     */
    displayStats(breakdown) {
        if (this.filteredEvents.length === 0) {
            this.statsRow.style.display = 'none';
            return;
        }

        document.getElementById('totalEvents').textContent = this.filteredEvents.length;
        document.getElementById('deviceCount').textContent = breakdown.DEVICE || 0;
        document.getElementById('appCount').textContent = breakdown.APP || 0;
        document.getElementById('networkCount').textContent = breakdown.NETWORK || 0;
        document.getElementById('powerCount').textContent = breakdown.POWER || 0;

        this.statsRow.style.display = 'block';
    }

    /**
     * Render timeline events
     * CRITICAL: Each event = one DOM entry (no compression)
     */
    renderTimeline() {
        this.container.innerHTML = '';

        if (this.filteredEvents.length === 0) {
            this.emptyState.style.display = 'block';
            this.statsRow.style.display = 'none';
            return;
        }

        this.emptyState.style.display = 'none';

        // Render each event (FORENSIC: no grouping or compression)
        this.filteredEvents.forEach(event => {
            this.container.appendChild(this.createEventElement(event));
        });
    }

    /**
     * Create event DOM element
     */
    createEventElement(event) {
        const div = document.createElement('div');
        div.className = `timeline-event category-${event.category}`;
        div.dataset.eventId = event.id;

        // Header
        const header = document.createElement('div');
        header.className = 'event-header';

        const eventType = document.createElement('div');
        eventType.className = 'event-type';
        eventType.textContent = this.formatEventType(event.event_type);

        // UTC timestamp (ALWAYS VISIBLE - MANDATORY)
        const timestamp = document.createElement('div');
        timestamp.className = 'event-timestamp';
        timestamp.textContent = event.timestamp_utc;
        timestamp.title = `Local: ${event.timestamp_local}`;

        header.appendChild(eventType);
        header.appendChild(timestamp);

        // Metadata badges
        const meta = document.createElement('div');
        meta.className = 'event-meta';

        // Category badge
        const categoryBadge = document.createElement('span');
        categoryBadge.className = 'event-badge badge-category';
        categoryBadge.textContent = event.category;
        meta.appendChild(categoryBadge);

        // Source badge
        const sourceBadge = document.createElement('span');
        sourceBadge.className = 'event-badge badge-source';
        sourceBadge.textContent = event.source;
        meta.appendChild(sourceBadge);

        // SNAPSHOT label (MANDATORY for dumpsys events)
        if (event.event_nature === 'SNAPSHOT') {
            const snapshotBadge = document.createElement('span');
            snapshotBadge.className = 'event-badge badge-snapshot';
            snapshotBadge.textContent = '⚠ SNAPSHOT';
            snapshotBadge.title = 'State observed at acquisition time';
            meta.appendChild(snapshotBadge);
        }

        // Confidence badge
        const confidenceBadge = document.createElement('span');
        confidenceBadge.className = 'event-badge badge-confidence';
        confidenceBadge.textContent = `Confidence: ${event.confidence}`;
        meta.appendChild(confidenceBadge);

        // Details panel (collapsed by default)
        const details = this.createDetailsPanel(event);

        div.appendChild(header);
        div.appendChild(meta);
        div.appendChild(details);

        // Click to expand details
        div.addEventListener('click', () => {
            details.classList.toggle('visible');
        });

        return div;
    }

    /**
     * Create event details panel
     */
    createDetailsPanel(event) {
        const details = document.createElement('div');
        details.className = 'event-details';

        // Raw reference (MANDATORY - forensic traceability)
        this.addDetailRow(details, 'Raw Reference', event.raw_reference, 'raw-reference');

        // Timestamps
        this.addDetailRow(details, 'UTC Timestamp', event.timestamp_utc);
        this.addDetailRow(details, 'Local Timestamp', event.timestamp_local);
        this.addDetailRow(details, 'Unix Timestamp', event.timestamp_unix);
        this.addDetailRow(details, 'Timezone Offset', event.timezone_offset);

        // Event metadata
        if (event.metadata) {
            Object.entries(event.metadata).forEach(([key, value]) => {
                if (value !== null && value !== undefined) {
                    this.addDetailRow(details, this.formatMetadataKey(key), value);
                }
            });
        }

        return details;
    }

    /**
     * Add detail row
     */
    addDetailRow(container, label, value, className = '') {
        const row = document.createElement('div');
        row.className = 'detail-row';

        const labelEl = document.createElement('div');
        labelEl.className = 'detail-label';
        labelEl.textContent = label + ':';

        const valueEl = document.createElement('div');
        valueEl.className = 'detail-value' + (className ? ' ' + className : '');
        valueEl.textContent = typeof value === 'object' ? JSON.stringify(value) : value;

        row.appendChild(labelEl);
        row.appendChild(valueEl);
        container.appendChild(row);
    }

    /**
     * Apply filters
     * FORENSIC: Filter is removal, not aggregation
     */
    applyFilters() {
        const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked'))
            .map(cb => cb.value);

        const startTime = document.getElementById('timeStart').value;
        const endTime = document.getElementById('timeEnd').value;

        this.filteredEvents = this.allEvents.filter(event => {
            // Category filter
            if (!selectedCategories.includes(event.category)) {
                return false;
            }

            // Time range filter (datetime-local format: YYYY-MM-DDTHH:MM)
            if (startTime) {
                // Parse datetime-local input and convert to Unix timestamp
                const startDate = new Date(startTime);
                const startUnix = Math.floor(startDate.getTime() / 1000);

                if (event.timestamp_unix < startUnix) {
                    return false;
                }
            }

            if (endTime) {
                const endDate = new Date(endTime);
                const endUnix = Math.floor(endDate.getTime() / 1000);

                if (event.timestamp_unix > endUnix) {
                    return false;
                }
            }

            return true;
        });

        // Recalculate stats
        const breakdown = {};
        this.filteredEvents.forEach(e => {
            breakdown[e.category] = (breakdown[e.category] || 0) + 1;
        });

        this.displayStats(breakdown);
        this.renderTimeline();
    }

    /**
     * Format event type for display
     */
    formatEventType(type) {
        return type.replace(/_/g, ' ');
    }

    /**
     * Format metadata key for display
     */
    formatMetadataKey(key) {
        return key.split('_').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    /**
     * Show error message
     */
    showError(message) {
        this.emptyState.innerHTML = `
            <i class="fas fa-exclamation-triangle" style="font-size: 48px; margin-bottom: 16px; display: block; color: #dc2626;"></i>
            <p style="color: #dc2626;">${message}</p>
        `;
        this.emptyState.style.display = 'block';
        this.statsRow.style.display = 'none';
    }
}
