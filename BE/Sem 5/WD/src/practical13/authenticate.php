<?php
require_once 'auth_config.php';

redirectIfLoggedIn();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $remember = isset($_POST['remember']);
    
    if (empty($email) || empty($password)) {
        header("Location: login.php?error=" . urlencode('Please fill in all fields'));
        exit();
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        header("Location: login.php?error=" . urlencode('Invalid email format'));
        exit();
    }
    
    if (authenticateUser($email, $password, $remember)) {
        header("Location: dashboard.php");
        exit();
    } else {
        header("Location: login.php?error=" . urlencode('Invalid email or password'));
        exit();
    }
} else {
    header("Location: login.php");
    exit();
}
?>
