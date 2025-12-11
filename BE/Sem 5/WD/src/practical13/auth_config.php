<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

$host = getenv('DB_HOST') ?: 'db';
$dbname = getenv('DB_NAME') ?: 'web_development';
$username = getenv('DB_USER') ?: 'root';
$password = getenv('DB_PASSWORD') ?: '';

try {
    $pdo_temp = new PDO("mysql:host=$host;charset=utf8", $username, $password);
    $pdo_temp->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $pdo_temp->exec("CREATE DATABASE IF NOT EXISTS `$dbname`");
    
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    
} catch(PDOException $e) {
    $error_message = "Database connection failed: " . $e->getMessage();
    
    if (strpos($e->getMessage(), 'No such file or directory') !== false) {
        $error_message .= "\n\nDocker-specific solutions:\n";
        $error_message .= "1. Make sure Docker containers are running: docker-compose up -d\n";
        $error_message .= "2. Check if the database container is healthy: docker-compose ps\n";
        $error_message .= "3. Restart the database container: docker-compose restart db\n";
        $error_message .= "4. Check database logs: docker-compose logs db\n";
    } elseif (strpos($e->getMessage(), 'Access denied') !== false) {
        $error_message .= "\n\nPossible solutions:\n";
        $error_message .= "1. Check your MySQL username and password\n";
        $error_message .= "2. Make sure the user has proper permissions\n";
        $error_message .= "3. Verify Docker environment variables\n";
    }
    
    die($error_message);
}

define('COOKIE_NAME', 'remember_me');
define('COOKIE_EXPIRE', time() + (30 * 24 * 60 * 60));
define('SESSION_TIMEOUT', 1800);

function isLoggedIn() {
    return isset($_SESSION['user_id']) && !empty($_SESSION['user_id']);
}

function checkSessionTimeout() {
    if (isset($_SESSION['last_activity'])) {
        if (time() - $_SESSION['last_activity'] > SESSION_TIMEOUT) {
            session_unset();
            session_destroy();
            return false;
        }
    }
    $_SESSION['last_activity'] = time();
    return true;
}

function requireLogin() {
    if (!isLoggedIn() || !checkSessionTimeout()) {
        header("Location: login.php");
        exit();
    }
}

function redirectIfLoggedIn() {
    if (isLoggedIn() && checkSessionTimeout()) {
        header("Location: dashboard.php");
        exit();
    }
}

function authenticateUser($email, $password, $remember = false) {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("SELECT id, first_name, last_name, email, password FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();
        
        if ($user && password_verify($password, $user['password'])) {
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['user_name'] = $user['first_name'] . ' ' . $user['last_name'];
            $_SESSION['user_email'] = $user['email'];
            $_SESSION['last_activity'] = time();
            
            if ($remember) {
                $token = bin2hex(random_bytes(32));
                setcookie(COOKIE_NAME, $token, COOKIE_EXPIRE, '/');
                
                $stmt = $pdo->prepare("UPDATE users SET remember_token = ? WHERE id = ?");
                $stmt->execute([$token, $user['id']]);
            }
            
            return true;
        }
        return false;
    } catch (PDOException $e) {
        error_log("Authentication error: " . $e->getMessage());
        return false;
    }
}

function checkRememberMe() {
    global $pdo;
    
    if (isset($_COOKIE[COOKIE_NAME]) && !isLoggedIn()) {
        $token = $_COOKIE[COOKIE_NAME];
        
        try {
            $stmt = $pdo->prepare("SELECT id, first_name, last_name, email FROM users WHERE remember_token = ?");
            $stmt->execute([$token]);
            $user = $stmt->fetch();
            
            if ($user) {
                $_SESSION['user_id'] = $user['id'];
                $_SESSION['user_name'] = $user['first_name'] . ' ' . $user['last_name'];
                $_SESSION['user_email'] = $user['email'];
                $_SESSION['last_activity'] = time();
                
                return true;
            } else {
                setcookie(COOKIE_NAME, '', time() - 3600, '/');
            }
        } catch (PDOException $e) {
            error_log("Remember me error: " . $e->getMessage());
        }
    }
    return false;
}

function logoutUser() {
    global $pdo;
    
    if (isset($_SESSION['user_id'])) {
        try {
            $stmt = $pdo->prepare("UPDATE users SET remember_token = NULL WHERE id = ?");
            $stmt->execute([$_SESSION['user_id']]);
        } catch (PDOException $e) {
            error_log("Logout error: " . $e->getMessage());
        }
    }
    
    setcookie(COOKIE_NAME, '', time() - 3600, '/');
    
    session_unset();
    session_destroy();
}

function getCurrentUser() {
    if (isLoggedIn()) {
        return [
            'id' => $_SESSION['user_id'],
            'name' => $_SESSION['user_name'],
            'email' => $_SESSION['user_email']
        ];
    }
    return null;
}

function addRememberTokenColumn($pdo) {
    try {
        $stmt = $pdo->query("SHOW COLUMNS FROM users LIKE 'remember_token'");
        if ($stmt->rowCount() == 0) {
            $pdo->exec("ALTER TABLE users ADD COLUMN remember_token VARCHAR(64) NULL");
        }
    } catch(PDOException $e) {
        error_log("Error adding remember_token column: " . $e->getMessage());
    }
}

addRememberTokenColumn($pdo);

checkRememberMe();
?>
