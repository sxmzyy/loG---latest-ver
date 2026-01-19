<?php
/**
 * Clear Data API Endpoint
 * Clears all extracted log files from the logs directory
 */

header('Content-Type: application/json');

// Allow from same origin
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

// Only allow POST or DELETE requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST' && $_SERVER['REQUEST_METHOD'] !== 'DELETE') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

// Get the logs path
require_once __DIR__ . '/../includes/config.php';

$logsPath = getLogsPath();

$result = [
    'success' => true,
    'filesDeleted' => 0,
    'errors' => []
];

// List of log files to clear
$logFiles = [
    'sms_logs.txt',
    'call_logs.txt',
    'location_logs.txt',
    'android_logcat.txt',
    'contacts_logs.txt',
    'apps_logs.txt',
    'device_info.txt',
    'battery_logs.txt',
    'network_logs.txt',
    'storage_logs.txt'
];

try {
    foreach ($logFiles as $file) {
        $filePath = $logsPath . '/' . $file;
        if (file_exists($filePath)) {
            if (unlink($filePath)) {
                $result['filesDeleted']++;
            } else {
                $result['errors'][] = "Failed to delete: $file";
            }
        }
    }

    // Also try to clear any other .txt files in the logs directory
    if (is_dir($logsPath)) {
        $files = glob($logsPath . '/*.txt');
        foreach ($files as $file) {
            if (unlink($file)) {
                $result['filesDeleted']++;
            }
        }

        // Clear any .json files as well
        $jsonFiles = glob($logsPath . '/*.json');
        foreach ($jsonFiles as $file) {
            if (unlink($file)) {
                $result['filesDeleted']++;
            }
        }
    }

    if (!empty($result['errors'])) {
        $result['success'] = false;
    }

    $result['message'] = $result['filesDeleted'] > 0
        ? "Successfully cleared {$result['filesDeleted']} log file(s)"
        : "No log files found to clear";

} catch (Exception $e) {
    $result['success'] = false;
    $result['error'] = $e->getMessage();
    http_response_code(500);
}

echo json_encode($result);
?>