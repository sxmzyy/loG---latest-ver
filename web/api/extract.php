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

    // ==========================================================
    // UNIFIED EXTRACTION PIPELINE (Fix for Empty Logs)
    // ==========================================================
    // Instead of disparate ADB calls, we run the robust Python extractor
    // This ensures full_package_dump.txt is generated correctly with UIDs.
    
    $rootPath = dirname(BASE_PATH);
    // Use full python command if possible, or just 'python'
    // We add buffering to see output clearly
    $cmd = "cd \"$rootPath\" && python scripts/enhanced_extraction.py 2>&1";
    
    $output = [];
    exec($cmd, $output, $returnCode);

    // DEBUG LOGGING
    $debugFile = $logsPath . '/debug_extract.txt';
    $debugContent = "Timestamp: " . date('Y-m-d H:i:s') . "\n";
    $debugContent .= "Command: $cmd\n";
    $debugContent .= "Return Code: $returnCode\n";
    $debugContent .= "Output:\n" . implode("\n", $output) . "\n";
    file_put_contents($debugFile, $debugContent);

    if ($returnCode !== 0) {
        $response['message'] .= " (Extraction failed: Return Code $returnCode. See debug_extract.txt)";
    } else {
        $stats['extraction_status'] = "Complete";
    }

    // ==========================================================
    // EXTRACT SMS, CALLS, AND LOCATION (Missing from enhanced_extraction.py)
    // ==========================================================
    
    // Extract SMS Messages
    if ($extractSms) {
        $smsFile = $logsPath . '/sms_logs.txt';
        $cmd = "adb shell content query --uri content://sms > \"$smsFile\" 2>&1";
        exec($cmd, $output, $returnCode);
    }
    
    // Extract Call Logs
    if ($extractCalls) {
        $callFile = $logsPath . '/call_logs.txt';
        $cmd = "adb shell content query --uri content://call_log/calls > \"$callFile\" 2>&1";
        exec($cmd, $output, $returnCode);
    }
    
    // Extract Location Logs (from dumpsys location)
    if ($extractLocation) {
        $locationFile = $logsPath . '/location_logs.txt';
        $cmd = "adb shell dumpsys location > \"$locationFile\" 2>&1";
        exec($cmd, $output, $returnCode);
    }

    // Update stats based on what the python script created
    if (file_exists($logsPath . '/android_logcat.txt')) {
        $stats['logcat'] = count(file($logsPath . '/android_logcat.txt'));
    }
    if (file_exists($logsPath . '/sms_logs.txt')) {
         $stats['sms'] = substr_count(file_get_contents($logsPath . '/sms_logs.txt'), 'Row:');
    }
    if (file_exists($logsPath . '/call_logs.txt')) {
         $stats['calls'] = substr_count(file_get_contents($logsPath . '/call_logs.txt'), 'Row:');
    }
    if (file_exists($logsPath . '/full_package_dump.txt')) {
        $stats['packages'] = substr_count(file_get_contents($logsPath . '/full_package_dump.txt'), 'package:');
    }

    // Post-Processing: Generate Unified Timeline for Map
    $rootPath = dirname(BASE_PATH);
    $cmd = "cd \"$rootPath\" && python analysis/unified_timeline.py 2>&1";
    $output = [];
    exec($cmd, $output, $returnCode);

    if ($returnCode !== 0) {
        // Log warning but don't fail the whole request
        $response['message'] .= " (Timeline generation failed: " . implode(" ", $output) . ")";
    } else {
        $stats['timeline_events'] = "Generated";
    }

    // Post-Processing: Generate Social Graph
    $cmd = "cd \"$rootPath\" && python analysis/social_graph.py 2>&1";
    $output = [];
    exec($cmd, $output, $returnCode);

    if ($returnCode !== 0) {
        $response['message'] .= " (Social graph generation failed: " . implode(" ", $output) . ")";
    } else {
        $stats['social_graph'] = "Generated";
    }

    // Post-Processing: App Session Analysis (Mule Hunter)
    $cmd = "cd \"$rootPath\" && python analysis/app_sessionizer.py 2>&1";
    $output = [];
    exec($cmd, $output, $returnCode);

    if ($returnCode !== 0) {
        $response['message'] .= " (App analysis failed: " . implode(" ", $output) . ")";
    } else {
        $stats['app_analysis'] = "Generated";
    }

    // Post-Processing: Dual Space / Mule Hunter Analysis (CRITICAL FIX)
    // This was missing, causing the '0 apps detected' issue in Web UI
    $cmd = "cd \"$rootPath\" && python analysis/dual_space_analyzer.py 2>&1";
    $output = [];
    exec($cmd, $output, $returnCode);

    if ($returnCode !== 0) {
        $response['message'] .= " (Dual Space analysis failed: " . implode(" ", $output) . ")";
    } else {
        $stats['dual_space_analysis'] = "Generated";
    }

    $response['success'] = true;
    $response['message'] = 'Logs extracted successfully!';
    $response['stats'] = $stats;

} catch (Exception $e) {
    $response['error'] = $e->getMessage();
}

echo json_encode($response);
