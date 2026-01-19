<?php
/**
 * Android Forensic Tool - Extract API
 * Triggers log extraction from connected Android device
 */
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once '../includes/config.php';

$response = [
    'success' => false,
    'message' => '',
    'stats' => null,
    'error' => null
];

// Get request options
$input = json_decode(file_get_contents('php://input'), true) ?? [];
$extractLogcat = $input['logcat'] ?? true;
$extractCalls = $input['calls'] ?? true;
$extractSms = $input['sms'] ?? true;
$extractLocation = $input['location'] ?? true;

$logsPath = getLogsPath();

// Ensure logs directory exists
if (!is_dir($logsPath)) {
    mkdir($logsPath, 0755, true);
}

try {
    $stats = ['logcat' => 0, 'calls' => 0, 'sms' => 0, 'locations' => 0];

    // Extract Logcat
    if ($extractLogcat) {
        $output = [];
        exec('adb logcat -d -v time 2>&1', $output, $returnCode);

        if ($returnCode === 0 && !empty($output)) {
            file_put_contents($logsPath . '/android_logcat.txt', implode("\n", $output));
            $stats['logcat'] = count($output);
        }
    }

    // Extract Call Logs
    if ($extractCalls) {
        $output = [];
        exec('adb shell content query --uri content://call_log/calls 2>&1', $output, $returnCode);

        if ($returnCode === 0) {
            $content = implode("\n", $output);
            file_put_contents($logsPath . '/call_logs.txt', $content);
            $stats['calls'] = substr_count($content, 'Row:');
        }
    }

    // Extract SMS Logs
    if ($extractSms) {
        $output = [];
        exec('adb shell content query --uri content://sms 2>&1', $output, $returnCode);

        if ($returnCode === 0) {
            $content = implode("\n", $output);
            file_put_contents($logsPath . '/sms_logs.txt', $content);
            $stats['sms'] = substr_count($content, 'Row:');
        }
    }

    // Extract Location Data
    if ($extractLocation) {
        $output = [];
        exec('adb shell dumpsys location 2>&1', $output, $returnCode);

        if ($returnCode === 0) {
            $content = implode("\n", $output);
            file_put_contents($logsPath . '/location_logs.txt', $content);
            $stats['locations'] = substr_count($content, 'Location[');
        }
    }

    $response['success'] = true;
    $response['message'] = 'Logs extracted successfully!';
    $response['stats'] = $stats;

} catch (Exception $e) {
    $response['error'] = $e->getMessage();
}

echo json_encode($response);
