<?php
/**
 * Android Forensic Tool - Export Report API
 * Generates PDF/HTML forensic report
 */
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once '../includes/config.php';

$response = [
    'success' => false,
    'filename' => null,
    'downloadUrl' => null,
    'error' => null
];

// Get export options
$input = json_decode(file_get_contents('php://input'), true) ?? [];
$format = $input['format'] ?? 'html';
$includeLogcat = $input['includeLogcat'] ?? true;
$includeSms = $input['includeSms'] ?? true;
$includeCalls = $input['includeCalls'] ?? true;
$includeLocation = $input['includeLocation'] ?? true;
$includeThreats = $input['includeThreats'] ?? true;

$logsPath = getLogsPath();
$exportPath = dirname($logsPath) . '/exports';

// Create exports directory if not exists
if (!is_dir($exportPath)) {
    mkdir($exportPath, 0755, true);
}

try {
    $timestamp = date('Y-m-d_H-i-s');
    $filename = "forensic_report_{$timestamp}";

    // Collect data
    $data = [
        'generated' => date('Y-m-d H:i:s'),
        'device' => 'Android Device',
        'sections' => []
    ];

    // SMS Data
    if ($includeSms && file_exists($logsPath . '/sms_logs.txt')) {
        $content = file_get_contents($logsPath . '/sms_logs.txt');
        $data['sections']['sms'] = [
            'title' => 'SMS Messages',
            'count' => substr_count($content, 'Row:'),
            'sample' => substr($content, 0, 2000)
        ];
    }

    // Call Data
    if ($includeCalls && file_exists($logsPath . '/call_logs.txt')) {
        $content = file_get_contents($logsPath . '/call_logs.txt');
        $data['sections']['calls'] = [
            'title' => 'Call Logs',
            'count' => substr_count($content, 'Row:'),
            'sample' => substr($content, 0, 2000)
        ];
    }

    // Location Data
    if ($includeLocation && file_exists($logsPath . '/location_logs.txt')) {
        $content = file_get_contents($logsPath . '/location_logs.txt');
        $data['sections']['location'] = [
            'title' => 'Location Data',
            'count' => substr_count($content, 'Location['),
            'sample' => substr($content, 0, 2000)
        ];
    }

    // Logcat Data
    if ($includeLogcat && file_exists($logsPath . '/android_logcat.txt')) {
        $lines = file($logsPath . '/android_logcat.txt');
        $data['sections']['logcat'] = [
            'title' => 'System Logs (Logcat)',
            'count' => count($lines),
            'sample' => implode("\n", array_slice($lines, 0, 100))
        ];
    }

    // Generate HTML Report
    $html = generateHtmlReport($data);
    $htmlFile = $exportPath . "/{$filename}.html";
    file_put_contents($htmlFile, $html);

    $response['success'] = true;
    $response['filename'] = "{$filename}.html";
    $response['downloadUrl'] = "exports/{$filename}.html";

} catch (Exception $e) {
    $response['error'] = $e->getMessage();
}

echo json_encode($response);

/**
 * Generate HTML Report
 */
function generateHtmlReport($data)
{
    $html = <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Android Forensic Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 40px; text-align: center; margin-bottom: 30px; border-radius: 10px; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .section { background: white; border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .section h2 { color: #1e3c72; border-bottom: 2px solid #2a5298; padding-bottom: 10px; margin-bottom: 20px; }
        .stat-box { display: inline-block; background: #f0f4f8; padding: 15px 25px; border-radius: 8px; margin-right: 15px; margin-bottom: 10px; }
        .stat-box .value { font-size: 2rem; font-weight: bold; color: #1e3c72; }
        .stat-box .label { font-size: 0.9rem; color: #666; }
        .log-preview { background: #0d1117; color: #c9d1d9; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 0.85rem; overflow-x: auto; max-height: 400px; overflow-y: auto; white-space: pre-wrap; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 0.9rem; }
        @media print { body { background: white; } .section { box-shadow: none; border: 1px solid #ddd; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Android Forensic Report</h1>
            <p>Generated: {$data['generated']}</p>
        </div>
HTML;

    foreach ($data['sections'] as $key => $section) {
        $html .= <<<HTML
        <div class="section">
            <h2>{$section['title']}</h2>
            <div class="stat-box">
                <div class="value">{$section['count']}</div>
                <div class="label">Total Records</div>
            </div>
            <h4 style="margin-top: 20px; margin-bottom: 10px;">Sample Data:</h4>
            <div class="log-preview">{$section['sample']}</div>
        </div>
HTML;
    }

    $html .= <<<HTML
        <div class="footer">
            <p>This report was generated by Android Forensic Tool</p>
            <p>© 2024 - For authorized forensic use only</p>
        </div>
    </div>
</body>
</html>
HTML;

    return $html;
}
