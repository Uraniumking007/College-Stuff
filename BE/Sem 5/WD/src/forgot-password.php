<?php
require_once 'auth.php';
require_once 'database.php';

$auth = new Auth();
$message = '';
$messageType = '';

// Check if user is already logged in
if ($auth->isLoggedIn()) {
    header('Location: dashboard.php');
    exit;
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    
    if (empty($email)) {
        $message = 'Please enter your email address';
        $messageType = 'error';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $message = 'Please enter a valid email address';
        $messageType = 'error';
    } else {
        try {
            $pdo = getDBConnection();
            
            // Check if email exists
            $stmt = $pdo->prepare("SELECT id, username FROM users WHERE email = ? AND is_active = 1");
            $stmt->execute([$email]);
            $user = $stmt->fetch();
            
            if ($user) {
                // Generate reset token
                $token = bin2hex(random_bytes(32));
                $expires = date('Y-m-d H:i:s', strtotime('+1 hour'));
                
                // Store reset token
                $stmt = $pdo->prepare("
                    INSERT INTO password_reset_tokens (user_id, token, expires_at) 
                    VALUES (?, ?, ?)
                    ON DUPLICATE KEY UPDATE token = VALUES(token), expires_at = VALUES(expires_at)
                ");
                $stmt->execute([$user['id'], $token, $expires]);
                
                // In a real application, you would send an email here
                // For demo purposes, we'll just show the token
                $message = 'Password reset link sent! (Demo: Token: ' . $token . ')';
                $messageType = 'success';
            } else {
                $message = 'If an account with that email exists, a password reset link has been sent.';
                $messageType = 'success'; // Don't reveal if email exists or not
            }
            
        } catch (PDOException $e) {
            $message = 'An error occurred. Please try again later.';
            $messageType = 'error';
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forgot Password - <?php echo SITE_NAME; ?></title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#667eea',
                        secondary: '#764ba2'
                    }
                }
            }
        }
    </script>
</head>
<body class="min-h-screen bg-gradient-to-br from-primary to-secondary flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-2xl p-8 w-full max-w-md">
        <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Forgot Password?</h1>
            <p class="text-gray-600 leading-relaxed">No worries! Enter your email address and we'll send you a link to reset your password.</p>
        </div>
        
        <?php if ($message): ?>
            <div class="p-4 rounded-lg mb-6 text-center <?php echo $messageType === 'error' ? 'bg-red-100 text-red-700 border border-red-300' : 'bg-green-100 text-green-700 border border-green-300'; ?>">
                <?php echo htmlspecialchars($message); ?>
            </div>
        <?php endif; ?>
        
        <form method="POST" action="">
            <div class="mb-8">
                <label for="email" class="block text-gray-700 font-medium mb-2">Email Address</label>
                <input type="email" id="email" name="email" value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>" required 
                       class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-primary transition-colors">
            </div>
            
            <button type="submit" class="w-full bg-gradient-to-r from-primary to-secondary text-white font-semibold py-3 px-6 rounded-lg hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200">
                Send Reset Link
            </button>
        </form>
        
        <div class="text-center mt-8">
            <div class="flex items-center justify-center space-x-4">
                <a href="login.php" class="text-primary hover:underline font-medium">Back to Login</a>
                <span class="text-gray-400">|</span>
                <a href="register.php" class="text-primary hover:underline font-medium">Create Account</a>
            </div>
        </div>
    </div>
</body>
</html>
