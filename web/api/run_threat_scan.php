<?php
header('Content-Type: application/json');

$baseDir = dirname(dirname(__DIR__));
$scriptPath = $baseDir . '/analysis/threat_detector.py';

$command = "python \"$scriptPath\" 2>&1";
$output = [];
$returnCode = 0;

exec($command, $output, $returnCode);

if ($returnCode === 0) {
    echo json_encode(['success' => true, 'message' => 'Scan complete', 'output' => $output]);
} else {
    echo json_encode(['success' => false, 'error' => 'Script failed', 'details' => $output]);
}
?>
