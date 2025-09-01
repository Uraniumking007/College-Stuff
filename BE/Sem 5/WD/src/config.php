<?php
// Configuration file for authentication system

// Database configuration
define('DB_HOST', getenv('DB_HOST') ?: 'localhost');
define('DB_NAME', getenv('DB_NAME') ?: 'example');
define('DB_USER', getenv('DB_USER') ?: 'root');
define('DB_PASS', getenv('PASSWORD_FILE_PATH') ? trim(file_get_contents(getenv('PASSWORD_FILE_PATH'))) : '');

// Application configuration
define('SITE_NAME', 'PHP Auth System');
define('SITE_URL', 'http://localhost:9000');

// Security configuration
define('HASH_COST', 12); // For password_hash()
define('SESSION_TIMEOUT', 1800); // 30 minutes in seconds
define('MAX_LOGIN_ATTEMPTS', 5);
define('LOCKOUT_TIME', 900); // 15 minutes in seconds

// Error reporting (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 1);
?>
