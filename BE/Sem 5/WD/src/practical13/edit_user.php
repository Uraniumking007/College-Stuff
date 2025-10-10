<?php
require_once 'config.php';

$userId = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$user = null;
$message = '';
$messageType = '';

if ($userId > 0) {
    try {
        $stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
        $stmt->execute([$userId]);
        $user = $stmt->fetch();
        
        if (!$user) {
            $message = "User not found.";
            $messageType = "error";
        }
    } catch (PDOException $e) {
        $message = "Error fetching user: " . $e->getMessage();
        $messageType = "error";
    }
} else {
    $message = "Invalid user ID.";
    $messageType = "error";
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $user) {
    
    $firstName = trim($_POST['firstName'] ?? '');
    $lastName = trim($_POST['lastName'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $dateOfBirth = $_POST['dateOfBirth'] ?? '';
    $gender = $_POST['gender'] ?? '';
    $address = trim($_POST['address'] ?? '');
    $country = $_POST['country'] ?? '';
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
    
    if (empty($phone)) {
        $errors[] = 'Phone number is required';
    }
    
    if (empty($dateOfBirth)) {
        $errors[] = 'Date of birth is required';
    }
    
    if (empty($gender)) {
        $errors[] = 'Gender is required';
    }
    
    if (empty($country)) {
        $errors[] = 'Country is required';
    }
    
    if (empty($errors)) {
        try {
            $checkEmail = $pdo->prepare("SELECT id FROM users WHERE email = ? AND id != ?");
            $checkEmail->execute([$email, $userId]);
            
            if ($checkEmail->rowCount() > 0) {
                $errors[] = 'Email already exists';
            }
        } catch (PDOException $e) {
            $errors[] = 'Error checking email';
        }
    }
    
    if (!empty($errors)) {
        $message = implode(', ', $errors);
        $messageType = "error";
    } else {
        try {
            $sql = "UPDATE users SET 
                    first_name = ?, 
                    last_name = ?, 
                    email = ?, 
                    phone = ?, 
                    date_of_birth = ?, 
                    gender = ?, 
                    address = ?, 
                    country = ?, 
                    newsletter_subscribed = ?,
                    updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?";
            
            $stmt = $pdo->prepare($sql);
            $result = $stmt->execute([
                $firstName,
                $lastName,
                $email,
                $phone,
                $dateOfBirth,
                $gender,
                $address,
                $country,
                $newsletter,
                $userId
            ]);
            
            if ($result) {
                header("Location: users.php?updated=1");
                exit();
            } else {
                $message = 'Update failed. Please try again.';
                $messageType = "error";
            }
            
        } catch (PDOException $e) {
            error_log("Database error: " . $e->getMessage());
            $message = 'Database error occurred. Please try again.';
            $messageType = "error";
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit User</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        .required {
            color: #e74c3c;
        }
        input[type="text"],
        input[type="email"],
        input[type="tel"],
        input[type="date"],
        select,
        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
            transition: border-color 0.3s;
        }
        input:focus,
        select:focus,
        textarea:focus {
            outline: none;
            border-color: #4caf50;
        }
        .form-row {
            display: flex;
            gap: 15px;
        }
        .form-row .form-group {
            flex: 1;
        }
        .button-group {
            text-align: center;
            margin: 30px 0;
        }
        button {
            background-color: #4caf50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
            transition: background-color 0.3s, transform 0.2s;
        }
        button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }
        .btn-cancel {
            background-color: #f44336;
        }
        .btn-cancel:hover {
            background-color: #d32f2f;
        }
        .error {
            color: #e74c3c;
            font-size: 14px;
            margin-top: 5px;
        }
        .success {
            color: #27ae60;
            font-size: 14px;
            margin-top: 5px;
        }
        .field-info {
            font-size: 12px;
            color: #666;
            margin-top: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Edit User</h2>
        
        <?php if ($message): ?>
            <div class="<?php echo $messageType; ?>">
                <?php echo htmlspecialchars($message); ?>
            </div>
        <?php endif; ?>
        
        <?php if ($user): ?>
            <form method="POST">
                <div class="form-row">
                    <div class="form-group">
                        <label for="firstName">First Name <span class="required">*</span></label>
                        <input type="text" id="firstName" name="firstName" value="<?php echo htmlspecialchars($user['first_name']); ?>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="lastName">Last Name <span class="required">*</span></label>
                        <input type="text" id="lastName" name="lastName" value="<?php echo htmlspecialchars($user['last_name']); ?>" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="email">Email Address <span class="required">*</span></label>
                    <input type="email" id="email" name="email" value="<?php echo htmlspecialchars($user['email']); ?>" required>
                    <div class="field-info">Must be a valid email format</div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="phone">Phone Number <span class="required">*</span></label>
                        <input type="tel" id="phone" name="phone" value="<?php echo htmlspecialchars($user['phone']); ?>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="dateOfBirth">Date of Birth <span class="required">*</span></label>
                        <input type="date" id="dateOfBirth" name="dateOfBirth" value="<?php echo $user['date_of_birth']; ?>" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="gender">Gender <span class="required">*</span></label>
                    <select id="gender" name="gender" required>
                        <option value="">Select your gender</option>
                        <option value="male" <?php echo $user['gender'] === 'male' ? 'selected' : ''; ?>>Male</option>
                        <option value="female" <?php echo $user['gender'] === 'female' ? 'selected' : ''; ?>>Female</option>
                        <option value="other" <?php echo $user['gender'] === 'other' ? 'selected' : ''; ?>>Other</option>
                        <option value="prefer-not-to-say" <?php echo $user['gender'] === 'prefer-not-to-say' ? 'selected' : ''; ?>>Prefer not to say</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="address">Address</label>
                    <textarea id="address" name="address" rows="3" placeholder="Enter your address (optional)"><?php echo htmlspecialchars($user['address']); ?></textarea>
                </div>
                
                <div class="form-group">
                    <label for="country">Country <span class="required">*</span></label>
                    <select id="country" name="country" required>
                        <option value="">Select your country</option>
                        <option value="us" <?php echo $user['country'] === 'us' ? 'selected' : ''; ?>>United States</option>
                        <option value="uk" <?php echo $user['country'] === 'uk' ? 'selected' : ''; ?>>United Kingdom</option>
                        <option value="canada" <?php echo $user['country'] === 'canada' ? 'selected' : ''; ?>>Canada</option>
                        <option value="australia" <?php echo $user['country'] === 'australia' ? 'selected' : ''; ?>>Australia</option>
                        <option value="india" <?php echo $user['country'] === 'india' ? 'selected' : ''; ?>>India</option>
                        <option value="germany" <?php echo $user['country'] === 'germany' ? 'selected' : ''; ?>>Germany</option>
                        <option value="france" <?php echo $user['country'] === 'france' ? 'selected' : ''; ?>>France</option>
                        <option value="japan" <?php echo $user['country'] === 'japan' ? 'selected' : ''; ?>>Japan</option>
                        <option value="other" <?php echo $user['country'] === 'other' ? 'selected' : ''; ?>>Other</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="newsletter" name="newsletter" <?php echo $user['newsletter_subscribed'] ? 'checked' : ''; ?>>
                        Subscribe to our newsletter for updates and offers
                    </label>
                </div>
                
                <div class="button-group">
                    <button type="submit">Update User</button>
                    <a href="users.php"><button type="button" class="btn-cancel">Cancel</button></a>
                </div>
            </form>
        <?php else: ?>
            <div class="error">
                <p>User not found or invalid user ID.</p>
                <a href="users.php">Back to Users List</a>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>
