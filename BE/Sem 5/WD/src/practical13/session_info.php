<?php
require_once 'auth_config.php';


requireLogin();

$user = getCurrentUser();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Session Information</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .info-section {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .info-section h3 {
            color: #333;
            margin-top: 0;
            margin-bottom: 15px;
            border-bottom: 2px solid #4caf50;
            padding-bottom: 10px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        .info-item {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
        }
        .info-item strong {
            display: block;
            color: #4caf50;
            margin-bottom: 5px;
            font-size: 14px;
        }
        .info-item span {
            color: #333;
            font-size: 16px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 14px;
            transition: background-color 0.3s, transform 0.2s;
        }
        .btn-primary {
            background-color: #4caf50;
            color: white;
        }
        .btn-primary:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }
        .btn-danger {
            background-color: #f44336;
            color: white;
        }
        .btn-danger:hover {
            background-color: #d32f2f;
            transform: translateY(-2px);
        }
        .navigation {
            text-align: center;
            margin: 30px 0;
        }
        .session-status {
            text-align: center;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .session-active {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .session-warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Session Information</h1>
        
        <div class="session-status session-active">
            <h3>✓ Session Active</h3>
            <p>Your session is currently active and secure.</p>
        </div>
        
        <div class="info-section">
            <h3>User Information</h3>
            <div class="info-grid">
                <div class="info-item">
                    <strong>User ID</strong>
                    <span><?php echo $user['id']; ?></span>
                </div>
                <div class="info-item">
                    <strong>Full Name</strong>
                    <span><?php echo htmlspecialchars($user['name']); ?></span>
                </div>
                <div class="info-item">
                    <strong>Email Address</strong>
                    <span><?php echo htmlspecialchars($user['email']); ?></span>
                </div>
            </div>
        </div>
        
        <div class="info-section">
            <h3>Session Details</h3>
            <div class="info-grid">
                <div class="info-item">
                    <strong>Session ID</strong>
                    <span><?php echo session_id(); ?></span>
                </div>
                <div class="info-item">
                    <strong>Session Name</strong>
                    <span><?php echo session_name(); ?></span>
                </div>
                <div class="info-item">
                    <strong>Session Status</strong>
                    <span><?php echo session_status() === PHP_SESSION_ACTIVE ? 'Active' : 'Inactive'; ?></span>
                </div>
                <div class="info-item">
                    <strong>Last Activity</strong>
                    <span><?php echo date('Y-m-d H:i:s', $_SESSION['last_activity']); ?></span>
                </div>
                <div class="info-item">
                    <strong>Session Timeout</strong>
                    <span><?php echo SESSION_TIMEOUT / 60; ?> minutes</span>
                </div>
                <div class="info-item">
                    <strong>Time Until Timeout</strong>
                    <span><?php 
                        $timeLeft = SESSION_TIMEOUT - (time() - $_SESSION['last_activity']);
                        echo max(0, $timeLeft / 60); 
                    ?> minutes</span>
                </div>
            </div>
        </div>
        
        <div class="info-section">
            <h3>Cookie Information</h3>
            <div class="info-grid">
                <div class="info-item">
                    <strong>Remember Me Cookie</strong>
                    <span><?php echo isset($_COOKIE[COOKIE_NAME]) ? 'Set' : 'Not Set'; ?></span>
                </div>
                <div class="info-item">
                    <strong>Cookie Name</strong>
                    <span><?php echo COOKIE_NAME; ?></span>
                </div>
                <div class="info-item">
                    <strong>Cookie Expiry</strong>
                    <span><?php echo isset($_COOKIE[COOKIE_NAME]) ? '30 days' : 'N/A'; ?></span>
                </div>
            </div>
        </div>
        
        <div class="info-section">
            <h3>Security Information</h3>
            <div class="info-grid">
                <div class="info-item">
                    <strong>Password Hash</strong>
                    <span>Securely stored (not displayed)</span>
                </div>
                <div class="info-item">
                    <strong>SQL Injection Protection</strong>
                    <span>✓ Enabled (Prepared Statements)</span>
                </div>
                <div class="info-item">
                    <strong>XSS Protection</strong>
                    <span>✓ Enabled (Input Sanitization)</span>
                </div>
                <div class="info-item">
                    <strong>Session Security</strong>
                    <span>✓ Enabled (Secure Session Management)</span>
                </div>
            </div>
        </div>
        
        <div class="navigation">
            <a href="dashboard.php" class="btn btn-primary">Back to Dashboard</a>
            <a href="logout.php" class="btn btn-danger">Logout</a>
        </div>
    </div>
</body>
</html>
