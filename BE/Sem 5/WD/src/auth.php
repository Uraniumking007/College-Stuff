<?php
require_once 'config.php';
require_once 'database.php';

/**
 * Authentication class for user management
 */
class Auth {
    private $pdo;
    
    public function __construct() {
        $this->pdo = getDBConnection();
        $this->startSecureSession();
    }
    
    /**
     * Start a secure session
     */
    private function startSecureSession() {
        if (session_status() === PHP_SESSION_NONE) {
            // Set secure session parameters
            ini_set('session.cookie_httponly', 1);
            ini_set('session.cookie_secure', 0); // Set to 1 if using HTTPS, default is 0
            ini_set('session.use_strict_mode', 1);
            ini_set('session.cookie_samesite', 'Strict');
            
            session_start();
        }
        
        // Regenerate session ID periodically for security
        if (!isset($_SESSION['last_regeneration'])) {
            session_regenerate_id(true);
            $_SESSION['last_regeneration'] = time();
        } elseif (time() - $_SESSION['last_regeneration'] > 300) { // 5 minutes = 300 seconds
            session_regenerate_id(true);
            $_SESSION['last_regeneration'] = time();
        }
    }
    
    /**
     * Register a new user
     */
    public function register($username, $email, $password) {
        try {
            // Validate input
            if (empty($username) || empty($email) || empty($password)) {
                return ['success' => false, 'message' => 'All fields are required'];
            }
            
            if (strlen($username) < 3 || strlen($username) > 50) {
                return ['success' => false, 'message' => 'Username must be between 3 and 50 characters'];
            }
            
            if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
                return ['success' => false, 'message' => 'Invalid email format'];
            }
            
            if (strlen($password) < 8) {
                return ['success' => false, 'message' => 'Password must be at least 8 characters long'];
            }
            
            // Check if username or email already exists
            $stmt = $this->pdo->prepare("SELECT id FROM users WHERE username = ? OR email = ?");
            $stmt->execute([$username, $email]);
            
            if ($stmt->fetch()) {
                return ['success' => false, 'message' => 'Username or email already exists'];
            }
            
            // Hash password
            $password_hash = password_hash($password, PASSWORD_BCRYPT, ['cost' => HASH_COST]);
            
            // Insert new user
            $stmt = $this->pdo->prepare("
                INSERT INTO users (username, email, password_hash) 
                VALUES (?, ?, ?)
            ");
            $stmt->execute([$username, $email, $password_hash]);
            
            return ['success' => true, 'message' => 'User registered successfully'];
            
        } catch (PDOException $e) {
            return ['success' => false, 'message' => 'Registration failed: ' . $e->getMessage()];
        }
    }
    
    /**
     * Login user
     */
    public function login($username, $password) {
        try {
            // Check if account is locked
            $stmt = $this->pdo->prepare("
                SELECT id, username, password_hash, login_attempts, locked_until, is_active 
                FROM users 
                WHERE (username = ? OR email = ?)
            ");
            $stmt->execute([$username, $username]);
            $user = $stmt->fetch();
            
            if (!$user) {
                return ['success' => false, 'message' => 'Invalid credentials'];
            }
            
            if (!$user['is_active']) {
                return ['success' => false, 'message' => 'Account is deactivated'];
            }
            
            // Check if account is locked
            if ($user['locked_until'] && strtotime($user['locked_until']) > time()) {
                $remaining = ceil((strtotime($user['locked_until']) - time()) / 60);
                return ['success' => false, 'message' => "Account is locked. Try again in {$remaining} minutes"];
            }
            
            // Verify password
            if (!password_verify($password, $user['password_hash'])) {
                // Increment login attempts
                $this->incrementLoginAttempts($user['id']);
                return ['success' => false, 'message' => 'Invalid credentials'];
            }
            
            // Reset login attempts on successful login
            $this->resetLoginAttempts($user['id']);
            
            // Update last login
            $stmt = $this->pdo->prepare("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?");
            $stmt->execute([$user['id']]);
            
            // Set session
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            $_SESSION['login_time'] = time();
            
            // Store session in database
            $this->storeSession($user['id']);
            
            return ['success' => true, 'message' => 'Login successful'];
            
        } catch (PDOException $e) {
            return ['success' => false, 'message' => 'Login failed: ' . $e->getMessage()];
        }
    }
    
    /**
     * Logout user
     */
    public function logout() {
        // Remove session from database
        if (isset($_SESSION['user_id'])) {
            $this->removeSession($_SESSION['user_id']);
        }
        
        // Destroy session
        session_destroy();
        session_start();
        
        return ['success' => true, 'message' => 'Logged out successfully'];
    }
    
    /**
     * Check if user is logged in
     */
    public function isLoggedIn() {
        if (!isset($_SESSION['user_id'])) {
            return false;
        }
        
        // Check session timeout
        if (time() - $_SESSION['login_time'] > SESSION_TIMEOUT) {
            $this->logout();
            return false;
        }
        
        // Update session activity
        $_SESSION['login_time'] = time();
        $this->updateSessionActivity($_SESSION['user_id']);
        
        return true;
    }
    
    /**
     * Get current user data
     */
    public function getCurrentUser() {
        if (!$this->isLoggedIn()) {
            return null;
        }
        
        try {
            $stmt = $this->pdo->prepare("SELECT id, username, email, created_at, last_login FROM users WHERE id = ?");
            $stmt->execute([$_SESSION['user_id']]);
            return $stmt->fetch();
        } catch (PDOException $e) {
            return null;
        }
    }
    
    /**
     * Increment login attempts
     */
    private function incrementLoginAttempts($user_id) {
        try {
            $stmt = $this->pdo->prepare("
                UPDATE users 
                SET login_attempts = login_attempts + 1,
                    locked_until = CASE 
                        WHEN login_attempts + 1 >= ? THEN DATE_ADD(NOW(), INTERVAL ? SECOND)
                        ELSE locked_until
                    END
                WHERE id = ?
            ");
            $stmt->execute([MAX_LOGIN_ATTEMPTS, LOCKOUT_TIME, $user_id]);
        } catch (PDOException $e) {
            // Log error silently
        }
    }
    
    /**
     * Reset login attempts
     */
    private function resetLoginAttempts($user_id) {
        try {
            $stmt = $this->pdo->prepare("
                UPDATE users 
                SET login_attempts = 0, locked_until = NULL 
                WHERE id = ?
            ");
            $stmt->execute([$user_id]);
        } catch (PDOException $e) {
            // Log error silently
        }
    }
    
    /**
     * Store session in database
     */
    private function storeSession($user_id) {
        try {
            $session_id = session_id();
            $ip_address = $_SERVER['REMOTE_ADDR'] ?? '';
            $user_agent = $_SERVER['HTTP_USER_AGENT'] ?? '';
            
            // Remove old sessions for this user
            $stmt = $this->pdo->prepare("DELETE FROM user_sessions WHERE user_id = ?");
            $stmt->execute([$user_id]);
            
            // Insert new session
            $stmt = $this->pdo->prepare("
                INSERT INTO user_sessions (user_id, session_id, ip_address, user_agent)
                VALUES (?, ?, ?, ?)
            ");
            $stmt->execute([$user_id, $session_id, $ip_address, $user_agent]);
        } catch (PDOException $e) {
            // Log error silently
        }
    }
    
    /**
     * Remove session from database
     */
    private function removeSession($user_id) {
        try {
            $stmt = $this->pdo->prepare("DELETE FROM user_sessions WHERE user_id = ?");
            $stmt->execute([$user_id]);
        } catch (PDOException $e) {
            // Log error silently
        }
    }
    
    /**
     * Update session activity
     */
    private function updateSessionActivity($user_id) {
        try {
            $stmt = $this->pdo->prepare("
                UPDATE user_sessions 
                SET last_activity = CURRENT_TIMESTAMP 
                WHERE user_id = ?
            ");
            $stmt->execute([$user_id]);
        } catch (PDOException $e) {
            // Log error silently
        }
    }
    
    /**
     * Clean up expired sessions
     */
    public function cleanupExpiredSessions() {
        try {
            $stmt = $this->pdo->prepare("
                DELETE FROM user_sessions 
                WHERE last_activity < DATE_SUB(NOW(), INTERVAL ? SECOND)
            ");
            $stmt->execute([SESSION_TIMEOUT]);
        } catch (PDOException $e) {
            // Log error silently
        }
    }
}
?>
