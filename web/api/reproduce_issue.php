<?php
require_once '../includes/config.php';

$input = ["keyword" => "samuel", "timeRange" => "24h"];
$keyword = $input['keyword'];
$caseSensitive = false;

echo "Keyword: '$keyword'\n";

$logsPath = getLogsPath();
$file = $logsPath . '/android_logcat.txt';
$lines = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

$count = 0;
foreach ($lines as $line) {
    if ($count > 5)
        break;

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

    echo "MATCH: $line\n";
    $count++;
}
?>