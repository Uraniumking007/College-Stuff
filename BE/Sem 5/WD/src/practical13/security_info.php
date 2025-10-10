<?php
require_once 'auth_config.php';


requireLogin();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Information</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
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
        .security-section {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .security-section h3 {
            color: #333;
            margin-top: 0;
            margin-bottom: 15px;
            border-bottom: 2px solid #4caf50;
            padding-bottom: 10px;
        }
        .security-item {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
            margin: 10px 0;
        }
        .security-item h4 {
            color: #4caf50;
            margin-top: 0;
            margin-bottom: 10px;
        }
        .security-item p {
            color: #666;
            margin: 5px 0;
        }
        .security-item .status {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }
        .status.enabled {
            background-color: #d4edda;
            color: #155724;
        }
        .status.disabled {
            background-color: #f8d7da;
            color: #721c24;
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
        .code-example {
            background-color: #f1f1f1;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
            font-family: monospace;
            font-size: 14px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Security Features & Implementation</h1>
        
        <div class="security-section">
            <h3>Authentication Security</h3>
            
            <div class="security-item">
                <h4>Password Hashing <span class="status enabled">ENABLED</span></h4>
                <p>All passwords are hashed using PHP's <code>password_hash()</code> function with the default algorithm (bcrypt).</p>
                <div class="code-example">

$hashedPassword = password_hash($password, PASSWORD_DEFAULT);


if (password_verify($password, $user['password'])) {
    
}
                </div>
            </div>
            
            <div class="security-item">
                <h4>Session Management <span class="status enabled">ENABLED</span></h4>
                <p>Secure session handling with automatic timeout and regeneration.</p>
                <ul>
                    <li>Session timeout: <?php echo SESSION_TIMEOUT / 60; ?> minutes</li>
                    <li>Automatic session destruction on timeout</li>
                    <li>Session activity tracking</li>
                </ul>
            </div>
            
            <div class="security-item">
                <h4>Remember Me Functionality <span class="status enabled">ENABLED</span></h4>
                <p>Secure "Remember Me" feature using cryptographically secure tokens.</p>
                <ul>
                    <li>Random token generation using <code>random_bytes()</code></li>
                    <li>Token stored in database and secure cookie</li>
                    <li>Cookie expiry: 30 days</li>
                    <li>Token validation on each page load</li>
                </ul>
            </div>
        </div>
        
        <div class="security-section">
            <h3>Input Validation & Sanitization</h3>
            
            <div class="security-item">
                <h4>SQL Injection Prevention <span class="status enabled">ENABLED</span></h4>
                <p>All database queries use prepared statements to prevent SQL injection attacks.</p>
                <div class="code-example">

$stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
$stmt->execute([$email]);
                </div>
            </div>
            
            <div class="security-item">
                <h4>XSS Protection <span class="status enabled">ENABLED</span></h4>
                <p>All user input is sanitized using <code>htmlspecialchars()</code> before display.</p>
                <div class="code-example">

echo htmlspecialchars($userInput);
                </div>
            </div>
            
            <div class="security-item">
                <h4>Input Validation <span class="status enabled">ENABLED</span></h4>
                <p>Comprehensive input validation for all form fields.</p>
                <ul>
                    <li>Email format validation</li>
                    <li>Password strength requirements</li>
                    <li>Required field validation</li>
                    <li>Data type validation</li>
                </ul>
            </div>
        </div>
        
        <div class="security-section">
            <h3>Session Security</h3>
            
            <div class="security-item">
                <h4>Session Configuration <span class="status enabled">ENABLED</span></h4>
                <p>Secure session configuration and management.</p>
                <ul>
                    <li>Session timeout: <?php echo SESSION_TIMEOUT; ?> seconds</li>
                    <li>Automatic session cleanup</li>
                    <li>Session activity monitoring</li>
                    <li>Secure session ID generation</li>
                </ul>
            </div>
            
            <div class="security-item">
                <h4>Access Control <span class="status enabled">ENABLED</span></h4>
                <p>Protected pages require authentication.</p>
                <ul>
                    <li>Login requirement for protected pages</li>
                    <li>Automatic redirect to login page</li>
                    <li>Session validation on each request</li>
                </ul>
            </div>
        </div>
        
        <div class="security-section">
            <h3>Cookie Security</h3>
            
            <div class="security-item">
                <h4>Secure Cookies <span class="status enabled">ENABLED</span></h4>
                <p>Remember me cookies are implemented securely.</p>
                <ul>
                    <li>Cryptographically secure token generation</li>
                    <li>Database token storage</li>
                    <li>Automatic cookie cleanup on logout</li>
                    <li>Token validation on each request</li>
                </ul>
            </div>
        </div>
        
        <div class="security-section">
            <h3>Error Handling</h3>
            
            <div class="security-item">
                <h4>Secure Error Handling <span class="status enabled">ENABLED</span></h4>
                <p>Errors are handled securely without exposing sensitive information.</p>
                <ul>
                    <li>Database errors logged to error log</li>
                    <li>User-friendly error messages</li>
                    <li>No sensitive data exposure in errors</li>
                </ul>
            </div>
        </div>
        
        <div class="navigation">
            <a href="dashboard.php" class="btn btn-primary">Back to Dashboard</a>
            <a href="session_info.php" class="btn btn-primary">Session Information</a>
            <a href="logout.php" class="btn btn-danger">Logout</a>
        </div>
    </div>
</body>
</html>
