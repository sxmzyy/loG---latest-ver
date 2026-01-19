<?php
/**
 * Timeline Acquisition API
 * Provides forensic timeline extraction and event retrieval
 * 
 * Actions:
 * - extract: Trigger log extraction and timeline parsing
 * - get_events: Retrieve timeline events with filtering
 * - get_stats: Event statistics by category
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once '../includes/config.php';
require_once '../includes/services/TimelineAggregator.php';

$action = $_GET['action'] ?? 'get_events';

try {
    switch ($action) {
        case 'extract':
            extractTimeline();
            break;
            
        case 'get_events':
            getEvents();
            break;
            
        case 'get_stats':
            getStats();
            break;
            
        case 'audit':
            getAudit();
            break;
            
        default:
            echo json_encode(['success' => false, 'error' => 'Invalid action']);
    }
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage(),
        'trace' => DEBUG_MODE ? $e->getTraceAsString() : null
    ]);
}

/**
 * Trigger timeline extraction from latest session
 */
function extractTimeline()
{
    try {
        $aggregator = new TimelineAggregator();
        $result = $aggregator->extractTimeline();
        
        // Save to JSON for persistence
        $logsPath = getLogsPath();
        $outputFile = $logsPath . '/forensic_timeline.json';
        
        $data = [
            'extracted_at' => date('c'),
            'events' => array_map(function($event) {
                return $event->toArray();
            }, $result['events']),
            'audit_log' => $result['audit_log'],
            'metadata' => $result['metadata'],
            'retention_notice' => $result['retention_notice']
        ];
        
        file_put_contents($outputFile, json_encode($data, JSON_PRETTY_PRINT));
        
        echo json_encode([
            'success' => true,
            'total_events' => count($result['events']),
            'audit_log' => $result['audit_log'],
            'retention_notice' => $result['retention_notice'],
            'saved_to' => basename($outputFile)
        ]);
        
    } catch (Exception $e) {
        // Check if error is due to missing extraction data
        if (strpos($e->getMessage(), 'No timeline session directory') !== false) {
            echo json_encode([
                'success' => false,
                'error' => 'No timeline data found',
                'instructions' => [
                    'You must first collect logs from your Android device.',
                    'Steps:',
                    '1. Connect your device via ADB',
                    '2. Run: python scripts/extract_timeline_logs.py',
                    '3. Wait for extraction to complete',
                    '4. Click "Extract Timeline" again'
                ],
                'technical_error' => $e->getMessage()
            ]);
        } else {
            echo json_encode([
                'success' => false,
                'error' => $e->getMessage(),
                'trace' => DEBUG_MODE ? $e->getTraceAsString() : null
            ]);
        }
    }
}

/**
 * Get timeline events with filtering
 */
function getEvents()
{
    $logsPath = getLogsPath();
    $timelineFile = $logsPath . '/forensic_timeline.json';
    
    if (!file_exists($timelineFile)) {
        echo json_encode([
            'success' => true,
            'total_events' => 0,
            'events' => [],
            'retention_notice' => 'No timeline data extracted yet. Click "Extract Timeline" to begin.'
        ]);
        return;
    }
    
    $data = json_decode(file_get_contents($timelineFile), true);
    
    // Apply filters
    $category = $_GET['category'] ?? null;
    $start_time = $_GET['start_time'] ?? null;
    $end_time = $_GET['end_time'] ?? null;
    
    $events = $data['events'] ?? [];
    
    if ($category) {
        $events = array_filter($events, function($e) use ($category) {
            return $e['category'] === $category;
        });
    }
    
    if ($start_time) {
        $start_unix = strtotime($start_time);
        $events = array_filter($events, function($e) use ($start_unix) {
            return $e['timestamp_unix'] >= $start_unix;
        });
    }
    
    if ($end_time) {
        $end_unix = strtotime($end_time);
        $events = array_filter($events, function($e) use ($end_unix) {
            return $e['timestamp_unix'] <= $end_unix;
        });
    }
    
    $events = array_values($events); // Re-index
    
    // Calculate stats
    $category_breakdown = [];
    foreach ($events as $event) {
        $cat = $event['category'];
        $category_breakdown[$cat] = ($category_breakdown[$cat] ?? 0) + 1;
    }
    
    // Time range
    $time_range = [
        'start' => !empty($events) ? $events[0]['timestamp_utc'] : null,
        'end' => !empty($events) ? end($events)['timestamp_utc'] : null
    ];
    
    echo json_encode([
        'success' => true,
        'total_events' => count($events),
        'category_breakdown' => $category_breakdown,
        'time_range' => $time_range,
        'events' => $events,
        'extracted_at' => $data['extracted_at'] ?? null,
        'retention_notice' => $data['retention_notice'] ?? 'Timeline limited by logcat buffer retention'
    ]);
}

/**
 * Get event statistics
 */
function getStats()
{
    $logsPath = getLogsPath();
    $timelineFile = $logsPath . '/forensic_timeline.json';
    
    if (!file_exists($timelineFile)) {
        echo json_encode([
            'success' => true,
            'total_events' => 0,
            'category_breakdown' => []
        ]);
        return;
    }
    
    $data = json_decode(file_get_contents($timelineFile), true);
    $events = $data['events'] ?? [];
    
    $stats = [
        'total_events' => count($events),
        'category_breakdown' => [],
        'event_type_breakdown' => []
    ];
    
    foreach ($events as $event) {
        $cat = $event['category'];
        $type = $event['event_type'];
        
        $stats['category_breakdown'][$cat] = ($stats['category_breakdown'][$cat] ?? 0) + 1;
        $stats['event_type_breakdown'][$type] = ($stats['event_type_breakdown'][$type] ?? 0) + 1;
    }
    
    echo json_encode(array_merge(['success' => true], $stats));
}

/**
 * Get forensic audit trail
 */
function getAudit()
{
    $logsPath = getLogsPath();
    $timelineFile = $logsPath . '/forensic_timeline.json';
    
    if (!file_exists($timelineFile)) {
        echo json_encode([
            'success' => false,
            'error' => 'No timeline data available'
        ]);
        return;
    }
    
    $data = json_decode(file_get_contents($timelineFile), true);
    
    echo json_encode([
        'success' => true,
        'audit_log' => $data['audit_log'] ?? [],
        'metadata' => $data['metadata'] ?? [],
        'retention_notice' => $data['retention_notice'] ?? null
    ]);
}
