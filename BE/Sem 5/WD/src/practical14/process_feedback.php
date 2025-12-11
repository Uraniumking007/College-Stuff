<?php
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode([
        'success' => false,
        'message' => 'Method not allowed. Only POST requests are accepted.'
    ]);
    exit;
}

function sanitizeInput($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
    return $data;
}

function validateEmail($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL);
}

function logFeedback($data) {
    $logFile = 'feedback_log.txt';
    $timestamp = date('Y-m-d H:i:s');
    $logEntry = "[$timestamp] " . json_encode($data) . "\n";
    
    if (!file_exists('logs')) {
        mkdir('logs', 0755, true);
    }
    
    file_put_contents('logs/' . $logFile, $logEntry, FILE_APPEND | LOCK_EX);
}

function saveToDatabase($data) {
    try {
        $host = getenv('DB_HOST') ?: 'localhost';
        $dbname = 'feedback_db';
        $username = getenv('DB_USER') ?: 'root';
        $password = getenv('DB_PASSWORD') ?: '';
        
        $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        $createTable = "
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                subject VARCHAR(50) NOT NULL,
                rating INT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ";
        $pdo->exec($createTable);
        
        $stmt = $pdo->prepare("
            INSERT INTO feedback (name, email, subject, rating, message) 
            VALUES (:name, :email, :subject, :rating, :message)
        ");
        
        $stmt->bindParam(':name', $data['name']);
        $stmt->bindParam(':email', $data['email']);
        $stmt->bindParam(':subject', $data['subject']);
        $stmt->bindParam(':rating', $data['rating']);
        $stmt->bindParam(':message', $data['message']);
        
        $stmt->execute();
        
        return true;
    } catch (PDOException $e) {
        error_log("Database error: " . $e->getMessage());
        
        if ($e->getCode() == 1049) {
            error_log("Database 'feedback_db' does not exist. Creating it...");
            try {
                $pdo = new PDO("mysql:host=$host;charset=utf8", $username, $password);
                $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                $pdo->exec("CREATE DATABASE IF NOT EXISTS feedback_db");
                $pdo->exec("USE feedback_db");
                
                $createTable = "
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        subject VARCHAR(50) NOT NULL,
                        rating INT NOT NULL,
                        message TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ";
                $pdo->exec($createTable);
                
                $stmt = $pdo->prepare("
                    INSERT INTO feedback (name, email, subject, rating, message) 
                    VALUES (:name, :email, :subject, :rating, :message)
                ");
                
                $stmt->bindParam(':name', $data['name']);
                $stmt->bindParam(':email', $data['email']);
                $stmt->bindParam(':subject', $data['subject']);
                $stmt->bindParam(':rating', $data['rating']);
                $stmt->bindParam(':message', $data['message']);
                
                $stmt->execute();
                return true;
            } catch (PDOException $e2) {
                error_log("Failed to create database: " . $e2->getMessage());
                return false;
            }
        }
        
        return false;
    }
}

$response = [
    'success' => false,
    'message' => '',
    'data' => null
];

try {
    error_log("Feedback form submission received. POST data: " . print_r($_POST, true));
    
    $name = isset($_POST['name']) ? sanitizeInput($_POST['name']) : '';
    $email = isset($_POST['email']) ? sanitizeInput($_POST['email']) : '';
    $subject = isset($_POST['subject']) ? sanitizeInput($_POST['subject']) : '';
    $rating = isset($_POST['rating']) ? intval($_POST['rating']) : 0;
    $message = isset($_POST['message']) ? sanitizeInput($_POST['message']) : '';
    
    $errors = [];
    
    if (empty($name) || strlen($name) < 2) {
        $errors[] = 'Name must be at least 2 characters long.';
    }
    
    if (empty($email) || !validateEmail($email)) {
        $errors[] = 'Please provide a valid email address.';
    }
    
    if (empty($subject)) {
        $errors[] = 'Please select a subject.';
    }
    
    if ($rating < 1 || $rating > 5) {
        $errors[] = 'Please select a valid rating (1-5).';
    }
    
    if (empty($message) || strlen($message) < 10) {
        $errors[] = 'Message must be at least 10 characters long.';
    }
    
    if (!empty($errors)) {
        $response['message'] = implode(' ', $errors);
        echo json_encode($response);
        exit;
    }
    
    $feedbackData = [
        'name' => $name,
        'email' => $email,
        'subject' => $subject,
        'rating' => $rating,
        'message' => $message,
        'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
        'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown'
    ];
    
    logFeedback($feedbackData);
    
    $dbSaved = saveToDatabase($feedbackData);
    
    if (!$dbSaved) {
        error_log("Failed to save feedback to database");
    }
    
    $emailSent = false;
    if (function_exists('mail')) {
        $to = 'admin@example.com'; 
        $emailSubject = "New Feedback: " . $subject;
        $emailBody = "
            New feedback has been submitted:
            
            Name: $name
            Email: $email
            Subject: $subject
            Rating: $rating/5
            Message: $message
            
            Submitted at: " . date('Y-m-d H:i:s') . "
            IP Address: " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "
        ";
        
        $headers = "From: noreply@example.com\r\n";
        $headers .= "Reply-To: $email\r\n";
        $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
        
        $emailSent = mail($to, $emailSubject, $emailBody, $headers);
    }
    
    $response['success'] = true;
    $response['message'] = 'Feedback submitted successfully!';
    $response['data'] = [
        'submission_id' => uniqid('fb_', true),
        'timestamp' => date('Y-m-d H:i:s'),
        'logged_to_file' => true,
        'saved_to_database' => $dbSaved,
        'email_sent' => $emailSent
    ];
    
    if (!$dbSaved) {
        $response['message'] = 'Feedback received and logged, but there was an issue saving to database.';
    }
    
    error_log("Feedback submitted successfully by: $email");
    
} catch (Exception $e) {
    $response['message'] = 'An unexpected error occurred. Please try again later.';
    error_log("Feedback submission error: " . $e->getMessage());
}

echo json_encode($response);
exit;