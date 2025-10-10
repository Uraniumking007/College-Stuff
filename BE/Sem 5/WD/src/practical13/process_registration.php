<?php
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    $firstName = trim($_POST['firstName'] ?? '');
    $lastName = trim($_POST['lastName'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $phone = trim($_POST['phone'] ?? '');
    $dateOfBirth = $_POST['dateOfBirth'] ?? '';
    $gender = $_POST['gender'] ?? '';
    $address = trim($_POST['address'] ?? '');
    $country = $_POST['country'] ?? '';
    $terms = isset($_POST['terms']) ? 1 : 0;
    $newsletter = isset($_POST['newsletter']) ? 1 : 0;
    
    $errors = [];
    
    if (empty($firstName)) {
        $errors[] = 'First name is required';
    } elseif (strlen($firstName) < 2 || strlen($firstName) > 50) {
        $errors[] = 'First name must be between 2 and 50 characters';
    }
    
    if (empty($lastName)) {
        $errors[] = 'Last name is required';
    } elseif (strlen($lastName) < 2 || strlen($lastName) > 50) {
        $errors[] = 'Last name must be between 2 and 50 characters';
    }
    
    if (empty($email)) {
        $errors[] = 'Email is required';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Invalid email format';
    }
    
    if (empty($password)) {
        $errors[] = 'Password is required';
    } elseif (strlen($password) < 8) {
        $errors[] = 'Password must be at least 8 characters long';
    }
    
    if (empty($phone)) {
        $errors[] = 'Phone number is required';
    }
    
    if (empty($dateOfBirth)) {
        $errors[] = 'Date of birth is required';
    } else {
        $birthDate = new DateTime($dateOfBirth);
        $today = new DateTime();
        $age = $today->diff($birthDate)->y;
        if ($age < 13) {
            $errors[] = 'You must be at least 13 years old to register';
        }
    }
    
    if (empty($gender)) {
        $errors[] = 'Gender is required';
    }
    
    if (empty($country)) {
        $errors[] = 'Country is required';
    }
    
    if (!$terms) {
        $errors[] = 'You must agree to the terms and conditions';
    }
    
    if (!empty($errors)) {
        $errorMessage = implode(', ', $errors);
        header("Location: register.php?error=" . urlencode($errorMessage));
        exit();
    }
    
    try {
        $checkEmail = $pdo->prepare("SELECT id FROM users WHERE email = ?");
        $checkEmail->execute([$email]);
        
        if ($checkEmail->rowCount() > 0) {
            header("Location: register.php?error=" . urlencode('Email already exists'));
            exit();
        }
        
        $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
        
        $sql = "INSERT INTO users (first_name, last_name, email, password, phone, date_of_birth, gender, address, country, terms_accepted, newsletter_subscribed) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        
        $stmt = $pdo->prepare($sql);
        $result = $stmt->execute([
            $firstName,
            $lastName,
            $email,
            $hashedPassword,
            $phone,
            $dateOfBirth,
            $gender,
            $address,
            $country,
            $terms,
            $newsletter
        ]);
        
        if ($result) {
            header("Location: register.php?success=1");
            exit();
        } else {
            header("Location: register.php?error=" . urlencode('Registration failed. Please try again.'));
            exit();
        }
        
    } catch (PDOException $e) {
        error_log("Database error: " . $e->getMessage());
        header("Location: register.php?error=" . urlencode('Database error occurred. Please try again.'));
        exit();
    }
    
} else {
    header("Location: register.php");
    exit();
}
?>
