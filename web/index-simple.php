<!DOCTYPE html>
<html>

<head>
    <title>Android Forensic Tool - Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #1e1e2e;
            color: #cdd6f4;
            padding: 20px;
        }

        .box {
            background: #252538;
            padding: 20px;
            margin: 10px 0;
            border-radius: 8px;
        }

        h1 {
            color: #89b4fa;
        }
    </style>
</head>

<body>
    <h1>🔍 Android Forensic Tool</h1>
    <div class="box">
        <h2>Dashboard Loading...</h2>
        <p>Server Time:
            <?= date('Y-m-d H:i:s') ?>
        </p>
        <p>If you see this, PHP is working!</p>
        <p><a href="test.php" style="color: #89b4fa;">Test Simple Page</a></p>
    </div>
</body>

</html>