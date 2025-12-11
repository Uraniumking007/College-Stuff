<?php
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

function createUsersTable($pdo) {
    $sql = "CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        date_of_birth DATE NOT NULL,
        gender ENUM('male', 'female', 'other', 'prefer-not-to-say') NOT NULL,
        address TEXT,
        country VARCHAR(50) NOT NULL,
        terms_accepted BOOLEAN DEFAULT FALSE,
        newsletter_subscribed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )";
    
    try {
        $pdo->exec($sql);
        return true;
    } catch(PDOException $e) {
        error_log("Error creating table: " . $e->getMessage());
        return false;
    }
}

createUsersTable($pdo);
?>
