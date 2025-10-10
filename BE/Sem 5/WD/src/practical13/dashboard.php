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
    <title>User Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
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
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }
        h1 {
            color: #333;
            margin: 0;
        }
        .user-info {
            text-align: right;
        }
        .user-name {
            font-size: 18px;
            font-weight: bold;
            color: #4caf50;
            margin-bottom: 5px;
        }
        .user-email {
            color: #666;
            font-size: 14px;
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
        .btn-danger {
            background-color: #f44336;
            color: white;
        }
        .btn-danger:hover {
            background-color: #d32f2f;
            transform: translateY(-2px);
        }
        .btn-primary {
            background-color: #4caf50;
            color: white;
        }
        .btn-primary:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }
        .btn-info {
            background-color: #2196f3;
            color: white;
        }
        .btn-info:hover {
            background-color: #1976d2;
            transform: translateY(-2px);
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .dashboard-card {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }
        .dashboard-card h3 {
            color: #333;
            margin-top: 0;
            margin-bottom: 15px;
        }
        .dashboard-card p {
            color: #666;
            margin-bottom: 20px;
        }
        .session-info {
            background-color: #e3f2fd;
            border: 1px solid #2196f3;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            color: #1976d2;
        }
        .session-info h4 {
            margin-top: 0;
            color: #1976d2;
        }
        .session-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .session-item {
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #bbdefb;
        }
        .session-item strong {
            display: block;
            color: #1976d2;
            margin-bottom: 5px;
        }
        .features {
            background-color: #f5f5f5;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .features h3 {
            color: #333;
            margin-top: 0;
        }
        .features ul {
            list-style-type: none;
            padding: 0;
        }
        .features li {
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .features li:before {
            content: "✓ ";
            color: #4caf50;
            font-weight: bold;
        }
        .features li:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Your Dashboard</h1>
            <div class="user-info">
                <div class="user-name">Hello, <?php echo htmlspecialchars($user['name']); ?>!</div>
                <div class="user-email"><?php echo htmlspecialchars($user['email']); ?></div>
                <a href="logout.php" class="btn btn-danger">Logout</a>
            </div>
        </div>
        
        <div class="session-info">
            <h4>Session & Authentication Information</h4>
            <div class="session-details">
                <div class="session-item">
                    <strong>Session ID:</strong>
                    <?php echo session_id(); ?>
                </div>
                <div class="session-item">
                    <strong>User ID:</strong>
                    <?php echo $user['id']; ?>
                </div>
                <div class="session-item">
                    <strong>Login Time:</strong>
                    <?php echo date('Y-m-d H:i:s', $_SESSION['last_activity']); ?>
                </div>
                <div class="session-item">
                    <strong>Session Status:</strong>
                    <span style="color: #4caf50;">Active</span>
                </div>
                <div class="session-item">
                    <strong>Remember Me:</strong>
                    <?php echo isset($_COOKIE[COOKIE_NAME]) ? 'Yes' : 'No'; ?>
                </div>
                <div class="session-item">
                    <strong>Session Timeout:</strong>
                    <?php echo SESSION_TIMEOUT / 60; ?> minutes
                </div>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <div class="dashboard-card">
                <h3>User Management</h3>
                <p>View and manage all registered users from Practical 13</p>
                <a href="users.php" class="btn btn-primary">View Users</a>
            </div>
            
            <div class="dashboard-card">
                <h3>Registration System</h3>
                <p>Add new users to the system</p>
                <a href="register.php" class="btn btn-primary">Register User</a>
            </div>
            
            <div class="dashboard-card">
                <h3>Session Management</h3>
                <p>View current session information and manage authentication</p>
                <a href="session_info.php" class="btn btn-info">Session Details</a>
            </div>
            
            <div class="dashboard-card">
                <h3>Security Features</h3>
                <p>Learn about the implemented security measures</p>
                <a href="security_info.php" class="btn btn-info">Security Info</a>
            </div>
        </div>
        
        <div class="features">
            <h3>Authentication System Features</h3>
            <ul>
                <li>Secure session management with automatic timeout</li>
                <li>Remember me functionality using secure cookies</li>
                <li>Password hashing for secure storage</li>
                <li>SQL injection prevention with prepared statements</li>
                <li>XSS protection with input sanitization</li>
                <li>Session regeneration for security</li>
                <li>Automatic logout on session timeout</li>
                <li>Cross-page authentication state management</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="logout.php" class="btn btn-danger">Logout</a>
            <a href="users.php" class="btn btn-primary">Manage Users</a>
        </div>
    </div>
</body>
</html>
