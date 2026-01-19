<?php
/**
 * Android Forensic Tool - Filter API
 * Filters log data based on criteria
 */
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once '../includes/config.php';

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

            $results[] = [
                'timestamp' => $timestamp,
                'type' => str_replace('_', ' ', ucfirst($fileType)),
                'level' => $level,
                'content' => substr($line, 0, 500) // Limit content length
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
