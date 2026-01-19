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

$lastPosition = 0;
$logFile = getLogsPath() . '/android_logcat.txt';

// Main loop - stream new log lines
while (true) {
    // Check if client disconnected
    if (connection_aborted()) {
        break;
    }

    // Check if log file exists
    if (file_exists($logFile)) {
        $currentSize = filesize($logFile);

        if ($currentSize > $lastPosition) {
            $handle = fopen($logFile, 'r');
            fseek($handle, $lastPosition);

            while (($line = fgets($handle)) !== false) {
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

            $lastPosition = ftell($handle);
            fclose($handle);
        }
    }

    // Send heartbeat every 5 seconds
    sendEvent(['status' => 'alive', 'time' => date('H:i:s')], 'heartbeat');

    // Wait before checking again
    sleep(1);
}

// Send disconnect message
sendEvent(['status' => 'disconnected'], 'status');
