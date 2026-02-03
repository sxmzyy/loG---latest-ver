<?php
/**
 * Android Forensic Tool - Filter API
 * Filters log data based on criteria
 */
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once '../includes/config.php';

// Prevent caching
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

$response = [
    'success' => false,
    'count' => 0,
    'results' => [],
    'error' => null
];

// Get filter parameters
$input = json_decode(file_get_contents('php://input'), true) ?? [];

$logType = $input['logType'] ?? 'all';
$timeRange = $input['timeRange'] ?? 'all';
$severity = $input['severity'] ?? 'all';
$category = $input['category'] ?? 'all';
$keyword = $input['keyword'] ?? '';
$regex = $input['regex'] ?? '';
$caseSensitive = $input['caseSensitive'] ?? false;

$logsPath = getLogsPath();
$results = [];

try {
    // Determine which files to search
    $files = [];
    switch ($logType) {
        case 'logcat':
            $files[] = $logsPath . '/android_logcat.txt';
            break;
        case 'calls':
            $files[] = $logsPath . '/call_logs.txt';
            break;
        case 'sms':
            $files[] = $logsPath . '/sms_logs.txt';
            break;
        case 'location':
            $files[] = $logsPath . '/location_logs.txt';
            break;
        default:
            $files = glob($logsPath . '/*.txt');
    }

    // Calculate time threshold
    $timeThreshold = 0;
    switch ($timeRange) {
        case '1h':
            $timeThreshold = time() - 3600;
            break;
        case '24h':
            $timeThreshold = time() - 86400;
            break;
        case '7d':
            $timeThreshold = time() - 604800;
            break;
        case '30d':
            $timeThreshold = time() - 2592000;
            break;
    }

    // Severity pattern
    $severityPattern = '';
    switch ($severity) {
        case 'verbose':
            $severityPattern = '/\sV\//';
            break;
        case 'debug':
            $severityPattern = '/\sD\//';
            break;
        case 'info':
            $severityPattern = '/\sI\//';
            break;
        case 'warning':
            $severityPattern = '/\sW\//';
            break;
        case 'error':
            $severityPattern = '/\sE\//';
            break;
        case 'fatal':
            $severityPattern = '/\sF\//';
            break;
    }

    // Debug logging - log once per request, not per line
    file_put_contents(LOGS_PATH . '/debug_filter_request.log', date('Y-m-d H:i:s') . " - Input: " . json_encode($input) . "\n", FILE_APPEND);

    // Process each file
    foreach ($files as $file) {
        if (!file_exists($file))
            continue;

        $lines = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        $fileType = basename($file, '.txt');

        foreach ($lines as $line) {
            // Keyword filter
            if (!empty($keyword)) {
                if ($caseSensitive) {
                    if (strpos($line, $keyword) === false)
                        continue;
                } else {
                    if (stripos($line, $keyword) === false)
                        continue;
                }
            }

            // Regex filter
            if (!empty($regex)) {
                $flags = $caseSensitive ? '' : 'i';
                if (!preg_match("/$regex/$flags", $line))
                    continue;
            }

            // Severity filter (for logcat)
            if (!empty($severityPattern) && $fileType === 'android_logcat') {
                if (!preg_match($severityPattern, $line))
                    continue;
            }

            // Category filter
            if ($category !== 'all') {
                global $LOG_TYPES;
                if (isset($LOG_TYPES[ucfirst($category)])) {
                    $pattern = $LOG_TYPES[ucfirst($category)]['pattern'];
                    if (!preg_match($pattern, $line))
                        continue;
                }
            }

            // Extract timestamp and level
            $timestamp = '--';
            $level = 'I';

            if (preg_match('/^(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)/', $line, $match)) {
                $timestamp = $match[1];
            }

            if (preg_match('/\s([VDIWEF])\//', $line, $match)) {
                $level = $match[1];
            }

            // Time filter
            if ($timeThreshold > 0) {
                // Try to parse timestamp
                $logTime = 0;
                // Format: 01-23 13:46:46.045
                if (preg_match('/^(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})/', $line, $match)) {
                    // Assume current year as it's not in the log
                    $logTime = strtotime(date('Y') . '-' . $match[1]);
                }

                if ($logTime > 0 && $logTime < $timeThreshold) {
                    continue;
                }
            }

            $results[] = [
                'timestamp' => $timestamp,
                'type' => str_replace('_', ' ', ucfirst($fileType)),
                'level' => $level,
                'content' => $line // No truncation - send full line
            ];

            // Limit results
            if (count($results) >= 1000)
                break 2;
        }
    }

    $response['success'] = true;
    $response['count'] = count($results);
    $response['results'] = $results;

} catch (Exception $e) {
    $response['error'] = $e->getMessage();
}

echo json_encode($response);
