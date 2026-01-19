<?php
/**
 * Android Forensic Tool - Call Logs Page
 * Call history analysis with DataTables
 */
$pageTitle = 'Call Logs - Android Forensic Tool';
$basePath = '../';
require_once '../includes/header.php';
require_once '../includes/sidebar.php';

// Parse Call logs
function parseCallLogs()
{
    $logsPath = getLogsPath();
    $callFile = $logsPath . '/call_logs.txt';
    $records = [];

    if (!file_exists($callFile)) {
        return $records;
    }

    $content = file_get_contents($callFile);
    $lines = explode("\n", $content);

    foreach ($lines as $line) {
        if (strpos($line, 'Row:') === false)
            continue;

        $record = [
            'contact' => 'Unknown',
            'date' => '--',
            'time' => '--',
            'duration' => '0:00',
            'type' => 'Unknown'
        ];

        // Extract number
        if (preg_match('/number=([^,]+)/', $line, $match)) {
            $record['contact'] = trim($match[1]);
        }

        // Extract date
        if (preg_match('/date=(\d+)/', $line, $match)) {
            $timestamp = (int) (intval($match[1]) / 1000);
            $record['date'] = date('Y-m-d', $timestamp);
            $record['time'] = date('H:i:s', $timestamp);
            $record['timestamp'] = $timestamp;
        }

        // Extract duration
        if (preg_match('/duration=(\d+)/', $line, $match)) {
            $seconds = intval($match[1]);
            $mins = floor($seconds / 60);
            $secs = $seconds % 60;
            $record['duration'] = sprintf('%d:%02d', $mins, $secs);
            $record['durationSec'] = $seconds;
        }

        // Extract type
        if (preg_match('/type=(\d+)/', $line, $match)) {
            switch ($match[1]) {
                case '1':
                    $record['type'] = 'Incoming';
                    break;
                case '2':
                    $record['type'] = 'Outgoing';
                    break;
                case '3':
                    $record['type'] = 'Missed';
                    break;
                default:
                    $record['type'] = 'Unknown';
            }
        }

        $records[] = $record;
    }

    return $records;
}

// Get frequent callers
function getFrequentCallers($records, $limit = 5)
{
    $counts = [];
    foreach ($records as $r) {
        $contact = $r['contact'];
        if (!isset($counts[$contact])) {
            $counts[$contact] = 0;
        }
        $counts[$contact]++;
    }
    arsort($counts);
    return array_slice($counts, 0, $limit, true);
}

$callRecords = parseCallLogs();
$totalCalls = count($callRecords);
$incomingCount = count(array_filter($callRecords, fn($r) => $r['type'] === 'Incoming'));
$outgoingCount = count(array_filter($callRecords, fn($r) => $r['type'] === 'Outgoing'));
$missedCount = count(array_filter($callRecords, fn($r) => $r['type'] === 'Missed'));
$frequentCallers = getFrequentCallers($callRecords);

// Total call duration
$totalDuration = array_sum(array_column($callRecords, 'durationSec'));
$totalHours = floor($totalDuration / 3600);
$totalMins = floor(($totalDuration % 3600) / 60);
?>

<!-- Main Content Wrapper -->
<main class="app-main">
    <!-- Content Header -->
    <div class="app-content-header">
        <div class="container-fluid">
            <div class="row">
                <div class="col-sm-6">
                    <h3 class="mb-0">
                        <i class="fas fa-phone me-2 text-forensic-blue"></i>Call Logs
                    </h3>
                </div>
                <div class="col-sm-6">
                    <ol class="breadcrumb float-sm-end">
                        <li class="breadcrumb-item"><a href="../index.php">Home</a></li>
                        <li class="breadcrumb-item active">Call Logs</li>
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
                <div class="col-xl-3 col-lg-6 col-sm-6">
                    <div class="info-box">
                        <span class="info-box-icon bg-info"><i class="fas fa-phone"></i></span>
                        <div class="info-box-content">
                            <span class="info-box-text">Total Calls</span>
                            <span class="info-box-number"><?= number_format($totalCalls) ?></span>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-lg-6 col-sm-6">
                    <div class="info-box">
                        <span class="info-box-icon bg-success"><i class="fas fa-phone-volume"></i></span>
                        <div class="info-box-content">
                            <span class="info-box-text">Incoming</span>
                            <span class="info-box-number"><?= number_format($incomingCount) ?></span>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-lg-6 col-sm-6">
                    <div class="info-box">
                        <span class="info-box-icon bg-primary"><i class="fas fa-phone-alt"></i></span>
                        <div class="info-box-content">
                            <span class="info-box-text">Outgoing</span>
                            <span class="info-box-number"><?= number_format($outgoingCount) ?></span>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-lg-6 col-sm-6">
                    <div class="info-box">
                        <span class="info-box-icon bg-danger"><i class="fas fa-phone-slash"></i></span>
                        <div class="info-box-content">
                            <span class="info-box-text">Missed</span>
                            <span class="info-box-number"><?= number_format($missedCount) ?></span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <!-- Call Records Table -->
                <div class="col-lg-8">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-list me-2"></i>Call Records
                            </h3>
                            <div class="card-tools">
                                <div class="btn-group">
                                    <button class="btn btn-sm btn-outline-primary"
                                        onclick="exportTableData('callTable', 'csv')">
                                        <i class="fas fa-file-csv me-1"></i>CSV
                                    </button>
                                    <button class="btn btn-sm btn-outline-success"
                                        onclick="exportTableData('callTable', 'excel')">
                                        <i class="fas fa-file-excel me-1"></i>Excel
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                            <?php if ($totalCalls > 0): ?>
                                <table id="callTable" class="table table-striped table-hover" style="width:100%">
                                    <thead>
                                        <tr>
                                            <th><i class="fas fa-user me-1"></i>Contact</th>
                                            <th><i class="fas fa-calendar me-1"></i>Date</th>
                                            <th><i class="fas fa-clock me-1"></i>Time</th>
                                            <th><i class="fas fa-stopwatch me-1"></i>Duration</th>
                                            <th><i class="fas fa-phone me-1"></i>Type</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($callRecords as $call): ?>
                                            <tr>
                                                <td>
                                                    <i class="fas fa-user-circle me-2 text-muted"></i>
                                                    <strong><?= htmlspecialchars($call['contact']) ?></strong>
                                                </td>
                                                <td><?= htmlspecialchars($call['date']) ?></td>
                                                <td><?= htmlspecialchars($call['time']) ?></td>
                                                <td>
                                                    <i class="fas fa-clock me-1 text-muted"></i>
                                                    <?= htmlspecialchars($call['duration']) ?>
                                                </td>
                                                <td>
                                                    <?php
                                                    $typeClass = match ($call['type']) {
                                                        'Incoming' => 'bg-success',
                                                        'Outgoing' => 'bg-info',
                                                        'Missed' => 'bg-danger',
                                                        default => 'bg-secondary'
                                                    };
                                                    $typeIcon = match ($call['type']) {
                                                        'Incoming' => 'fa-arrow-down',
                                                        'Outgoing' => 'fa-arrow-up',
                                                        'Missed' => 'fa-phone-slash',
                                                        default => 'fa-question'
                                                    };
                                                    ?>
                                                    <span class="badge <?= $typeClass ?>">
                                                        <i class="fas <?= $typeIcon ?> me-1"></i><?= $call['type'] ?>
                                                    </span>
                                                </td>
                                            </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            <?php else: ?>
                                <div class="text-center py-5">
                                    <i class="fas fa-phone-slash fa-4x text-muted mb-3"></i>
                                    <h5>No Call Logs Found</h5>
                                    <p class="text-muted">Extract logs from a device to view call history.</p>
                                    <a href="extract-logs.php" class="btn btn-forensic">
                                        <i class="fas fa-download me-2"></i>Extract Logs
                                    </a>
                                </div>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>

                <!-- Sidebar Stats -->
                <div class="col-lg-4">
                    <!-- Call Duration -->
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-hourglass-half me-2"></i>Total Call Time
                            </h3>
                        </div>
                        <div class="card-body text-center">
                            <h2 class="text-forensic-blue mb-0">
                                <?= $totalHours ?>h <?= $totalMins ?>m
                            </h2>
                            <p class="text-muted">Total duration of all calls</p>
                        </div>
                    </div>

                    <!-- Most Frequent Callers -->
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-fire me-2"></i>Most Frequent
                            </h3>
                        </div>
                        <div class="card-body p-0">
                            <ul class="list-group list-group-flush">
                                <?php if (!empty($frequentCallers)): ?>
                                    <?php $rank = 1;
                                    foreach ($frequentCallers as $contact => $count): ?>
                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                            <div>
                                                <span
                                                    class="badge bg-<?= $rank <= 3 ? 'warning' : 'secondary' ?> me-2">#<?= $rank ?></span>
                                                <?= htmlspecialchars($contact) ?>
                                            </div>
                                            <span class="badge bg-primary rounded-pill"><?= $count ?> calls</span>
                                        </li>
                                        <?php $rank++; endforeach; ?>
                                <?php else: ?>
                                    <li class="list-group-item text-center text-muted">No data</li>
                                <?php endif; ?>
                            </ul>
                        </div>
                    </div>

                    <!-- Call Type Chart -->
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-chart-pie me-2"></i>Call Distribution
                            </h3>
                        </div>
                        <div class="card-body">
                            <div class="chart-container" style="height: 200px;">
                                <canvas id="callDistChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</main>

<?php
$additionalScripts = <<<SCRIPT
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Initialize DataTable
    if (document.getElementById('callTable')) {
        initDataTable('callTable', {
            order: [[1, 'desc'], [2, 'desc']]
        });
    }
    
    // Call Distribution Chart
    createChart('callDistChart', 'doughnut', {
        labels: ['Incoming', 'Outgoing', 'Missed'],
        datasets: [{
            data: [{$incomingCount}, {$outgoingCount}, {$missedCount}],
            backgroundColor: [
                chartColors.success,
                chartColors.primary,
                chartColors.danger
            ],
            borderWidth: 0
        }]
    }, {
        plugins: {
            legend: {
                position: 'bottom',
                labels: { padding: 10 }
            }
        }
    });
});
</script>
SCRIPT;

require_once '../includes/footer.php';
?>