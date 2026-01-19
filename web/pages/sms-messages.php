<?php
/**
 * Android Forensic Tool - SMS Messages Page
 * Modern view of SMS data with DataTables
 */
$pageTitle = 'SMS Messages - Android Forensic Tool';
$basePath = '../';
require_once '../includes/header.php';
require_once '../includes/sidebar.php';

// Parse SMS logs
function parseSmsLogs()
{
    $logsPath = getLogsPath();
    $smsFile = $logsPath . '/sms_logs.txt';
    $records = [];

    if (!file_exists($smsFile)) {
        return $records;
    }

    $content = file_get_contents($smsFile);
    $lines = explode("\n", $content);

    foreach ($lines as $line) {
        if (strpos($line, 'Row:') === false)
            continue;

        $record = [
            'contact' => 'Unknown',
            'date' => '--',
            'time' => '--',
            'type' => 'Unknown',
            'message' => ''
        ];

        // Extract address
        if (preg_match('/address=([^,]+)/', $line, $match)) {
            $record['contact'] = trim($match[1]);
        }

        // Extract date
        if (preg_match('/date=(\d+)/', $line, $match)) {
            $timestamp = (int) (intval($match[1]) / 1000);
            $record['date'] = date('Y-m-d', $timestamp);
            $record['time'] = date('H:i:s', $timestamp);
        }

        // Extract type
        if (preg_match('/type=(\d+)/', $line, $match)) {
            $record['type'] = $match[1] == '1' ? 'Received' : 'Sent';
        }

        // Extract body
        if (preg_match('/body=([^,]+?)(?:,\s*\w+=|$)/', $line, $match)) {
            $record['message'] = trim($match[1]);
        }

        $records[] = $record;
    }

    return $records;
}

$smsRecords = parseSmsLogs();
$totalSms = count($smsRecords);
$sentCount = count(array_filter($smsRecords, fn($r) => $r['type'] === 'Sent'));
$receivedCount = $totalSms - $sentCount;
?>

<!-- Main Content Wrapper -->
<main class="app-main">
    <!-- Content Header -->
    <div class="app-content-header">
        <div class="container-fluid">
            <div class="row">
                <div class="col-sm-6">
                    <h3 class="mb-0">
                        <i class="fas fa-comment-sms me-2 text-forensic-blue"></i>SMS Messages
                    </h3>
                </div>
                <div class="col-sm-6">
                    <ol class="breadcrumb float-sm-end">
                        <li class="breadcrumb-item"><a href="../index.php">Home</a></li>
                        <li class="breadcrumb-item active">SMS Messages</li>
                    </ol>
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="app-content">
        <div class="container-fluid">

            <!-- Summary Cards -->
            <div class="row mb-4">
                <div class="col-lg-4 col-sm-6">
                    <div class="info-box">
                        <span class="info-box-icon bg-info"><i class="fas fa-comment-sms"></i></span>
                        <div class="info-box-content">
                            <span class="info-box-text">Total Messages</span>
                            <span class="info-box-number"><?= number_format($totalSms) ?></span>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-sm-6">
                    <div class="info-box">
                        <span class="info-box-icon bg-success"><i class="fas fa-envelope"></i></span>
                        <div class="info-box-content">
                            <span class="info-box-text">Received</span>
                            <span class="info-box-number"><?= number_format($receivedCount) ?></span>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-sm-6">
                    <div class="info-box">
                        <span class="info-box-icon bg-primary"><i class="fas fa-paper-plane"></i></span>
                        <div class="info-box-content">
                            <span class="info-box-text">Sent</span>
                            <span class="info-box-number"><?= number_format($sentCount) ?></span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SMS Table -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-list me-2"></i>Message Records
                    </h3>
                    <div class="card-tools">
                        <div class="btn-group">
                            <button class="btn btn-sm btn-outline-primary" onclick="exportTableData('smsTable', 'csv')">
                                <i class="fas fa-file-csv me-1"></i>CSV
                            </button>
                            <button class="btn btn-sm btn-outline-success"
                                onclick="exportTableData('smsTable', 'excel')">
                                <i class="fas fa-file-excel me-1"></i>Excel
                            </button>
                            <button class="btn btn-sm btn-outline-secondary" onclick="window.print()">
                                <i class="fas fa-print me-1"></i>Print
                            </button>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <?php if ($totalSms > 0): ?>
                        <table id="smsTable" class="table table-striped table-hover" style="width:100%">
                            <thead>
                                <tr>
                                    <th><i class="fas fa-user me-1"></i>Contact</th>
                                    <th><i class="fas fa-calendar me-1"></i>Date</th>
                                    <th><i class="fas fa-clock me-1"></i>Time</th>
                                    <th><i class="fas fa-exchange-alt me-1"></i>Type</th>
                                    <th><i class="fas fa-comment me-1"></i>Message</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($smsRecords as $sms): ?>
                                    <tr>
                                        <td>
                                            <i class="fas fa-user-circle me-2 text-muted"></i>
                                            <strong><?= htmlspecialchars($sms['contact']) ?></strong>
                                        </td>
                                        <td><?= htmlspecialchars($sms['date']) ?></td>
                                        <td><?= htmlspecialchars($sms['time']) ?></td>
                                        <td>
                                            <?php if ($sms['type'] === 'Received'): ?>
                                                <span class="badge bg-success"><i
                                                        class="fas fa-arrow-down me-1"></i>Received</span>
                                            <?php else: ?>
                                                <span class="badge bg-info"><i class="fas fa-arrow-up me-1"></i>Sent</span>
                                            <?php endif; ?>
                                        </td>
                                        <td class="text-truncate" style="max-width: 300px;"
                                            title="<?= htmlspecialchars($sms['message']) ?>">
                                            <?= htmlspecialchars($sms['message']) ?>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    <?php else: ?>
                        <div class="text-center py-5">
                            <i class="fas fa-comment-slash fa-4x text-muted mb-3"></i>
                            <h5>No SMS Messages Found</h5>
                            <p class="text-muted">Extract logs from a device to view SMS messages.</p>
                            <a href="extract-logs.php" class="btn btn-forensic">
                                <i class="fas fa-download me-2"></i>Extract Logs
                            </a>
                        </div>
                    <?php endif; ?>
                </div>
            </div>

        </div>
    </div>
</main>

<?php
$additionalScripts = <<<'SCRIPT'
<script>
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('smsTable')) {
        initDataTable('smsTable', {
            order: [[1, 'desc'], [2, 'desc']], // Sort by date, time descending
            columnDefs: [
                { targets: 4, orderable: false } // Message column not sortable
            ]
        });
    }
});
</script>
SCRIPT;

require_once '../includes/footer.php';
?>