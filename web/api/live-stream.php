<?php
/**
 * Android Forensic Tool - Live Stream API
 * Server-Sent Events for real-time logcat streaming
 */

// SSE headers
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');
header('Connection: keep-alive');
header('X-Accel-Buffering: no');

// Prevent output buffering
if (ob_get_level())
    ob_end_clean();

// Set time limit for long-running connection
set_time_limit(0);

require_once '../includes/config.php';

// Send a message to the client
function sendEvent($data, $event = 'message')
{
    echo "event: {$event}\n";
    echo "data: " . json_encode($data) . "\n\n";
    flush();
}

// Send initial connection message
sendEvent(['status' => 'connected', 'message' => 'Live monitoring started'], 'status');

// Check if ADB is available
$adbPath = 'adb';  // Assumes adb is in PATH
exec('adb devices 2>&1', $output, $returnCode);

if ($returnCode !== 0) {
    sendEvent(['status' => 'error', 'message' => 'ADB not found. Please ensure ADB is installed.'], 'status');
    exit;
}

// Start ADB logcat process
$descriptorspec = array(
    0 => array("pipe", "r"),  // stdin
    1 => array("pipe", "w"),  // stdout
    2 => array("pipe", "w")   // stderr
);

$process = proc_open('adb logcat -v time', $descriptorspec, $pipes);

if (!is_resource($process)) {
    sendEvent(['status' => 'error', 'message' => 'Failed to start logcat'], 'status');
    exit;
}

// Make stdout non-blocking
stream_set_blocking($pipes[1], false);

$lineBuffer = '';
$lastHeartbeat = time();

// Main loop - stream logcat output
while (true) {
    // Check if client disconnected
    if (connection_aborted()) {
        break;
    }

    // Read from logcat
    $data = fread($pipes[1], 4096);
    
    if ($data !== false && $data !== '') {
        $lineBuffer .= $data;
        
        // Process complete lines
        while (($pos = strpos($lineBuffer, "\n")) !== false) {
            $line = substr($lineBuffer, 0, $pos);
            $lineBuffer = substr($lineBuffer, $pos + 1);
            
            $line = trim($line);
            if (!empty($line)) {
                // Parse log level
                $level = 'I';
                if (preg_match('/\s([VDIWEF])\//', $line, $match)) {
                    $level = $match[1];
                }

                // Parse tag
                $tag = 'System';
                if (preg_match('/[VDIWEF]\/([^:]+):/', $line, $match)) {
                    $tag = trim($match[1]);
                }

                sendEvent([
                    'line' => $line,
                    'level' => $level,
                    'tag' => $tag,
                    'timestamp' => date('H:i:s')
                ], 'log');
            }
        }
    }

    // Send heartbeat every 5 seconds
    if (time() - $lastHeartbeat >= 5) {
        sendEvent(['status' => 'alive', 'time' => date('H:i:s')], 'heartbeat');
        $lastHeartbeat = time();
    }

    // Small sleep to prevent CPU overload
    usleep(100000); // 100ms
}

// Cleanup
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_terminate($process);

// Send disconnect message
sendEvent(['status' => 'disconnected'], 'status');

