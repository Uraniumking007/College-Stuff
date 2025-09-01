<?php
require_once 'auth.php';

$auth = new Auth();

// Check if user is logged in
if (!$auth->isLoggedIn()) {
    header('Location: login.php');
    exit;
}

$user = $auth->getCurrentUser();
$message = '';
$messageType = '';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $current_password = $_POST['current_password'] ?? '';
    $new_password = $_POST['new_password'] ?? '';
    $confirm_password = $_POST['confirm_password'] ?? '';
    
    // Validate input
    if (empty($current_password) || empty($new_password) || empty($confirm_password)) {
        $message = 'All fields are required';
        $messageType = 'error';
    } elseif ($new_password !== $confirm_password) {
        $message = 'New passwords do not match';
        $messageType = 'error';
    } elseif (strlen($new_password) < 8) {
        $message = 'New password must be at least 8 characters long';
        $messageType = 'error';
    } else {
        try {
            $pdo = getDBConnection();
            
            // Verify current password
            $stmt = $pdo->prepare("SELECT password_hash FROM users WHERE id = ?");
            $stmt->execute([$user['id']]);
            $current_user = $stmt->fetch();
            
            if (!password_verify($current_password, $current_user['password_hash'])) {
                $message = 'Current password is incorrect';
                $messageType = 'error';
            } else {
                // Hash new password
                $new_password_hash = password_hash($new_password, PASSWORD_BCRYPT, ['cost' => HASH_COST]);
                
                // Update password
                $stmt = $pdo->prepare("UPDATE users SET password_hash = ? WHERE id = ?");
                $stmt->execute([$new_password_hash, $user['id']]);
                
                $message = 'Password changed successfully!';
                $messageType = 'success';
                
                // Clear form
                $_POST = [];
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
    <title>Change Password - <?php echo SITE_NAME; ?></title>
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
<body class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="text-2xl font-bold text-primary">
                        <?php echo SITE_NAME; ?>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <ul class="flex space-x-8">
                        <li><a href="dashboard.php" class="text-gray-700 hover:text-primary px-4 py-2 rounded-lg font-medium transition-colors">Dashboard</a></li>
                        <li><a href="profile.php" class="text-gray-700 hover:text-primary px-4 py-2 rounded-lg font-medium transition-colors">Profile</a></li>
                        <li><a href="change-password.php" class="bg-primary text-white px-4 py-2 rounded-lg font-medium">Change Password</a></li>
                    </ul>
                    <a href="dashboard.php?logout=1" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">Logout</a>
                </div>
            </div>
        </div>
    </nav>
    
    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="bg-white rounded-xl shadow-lg p-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Change Password</h1>
            
            <?php if ($message): ?>
                <div class="p-4 rounded-lg mb-6 text-center <?php echo $messageType === 'error' ? 'bg-red-100 text-red-700 border border-red-300' : 'bg-green-100 text-green-700 border border-green-300'; ?>">
                    <?php echo htmlspecialchars($message); ?>
                </div>
            <?php endif; ?>
            
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
                <h4 class="text-lg font-semibold text-blue-800 mb-3">Password Requirements:</h4>
                <ul class="text-blue-700 space-y-1">
                    <li class="flex items-center"><span class="mr-2">•</span>At least 8 characters long</li>
                    <li class="flex items-center"><span class="mr-2">•</span>Should be different from your current password</li>
                    <li class="flex items-center"><span class="mr-2">•</span>Consider using a mix of letters, numbers, and symbols</li>
                </ul>
            </div>
            
            <form method="POST" action="">
                <div class="mb-6">
                    <label for="current_password" class="block text-gray-700 font-medium mb-2">Current Password</label>
                    <input type="password" id="current_password" name="current_password" required 
                           class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-primary transition-colors">
                </div>
                
                <div class="mb-6">
                    <label for="new_password" class="block text-gray-700 font-medium mb-2">New Password</label>
                    <input type="password" id="new_password" name="new_password" required 
                           class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-primary transition-colors">
                </div>
                
                <div class="mb-8">
                    <label for="confirm_password" class="block text-gray-700 font-medium mb-2">Confirm New Password</label>
                    <input type="password" id="confirm_password" name="confirm_password" required 
                           class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-primary transition-colors">
                </div>
                
                <div class="flex gap-4 justify-center">
                    <button type="submit" class="bg-primary hover:bg-primary/90 text-white px-8 py-3 rounded-lg font-medium transition-colors">
                        Change Password
                    </button>
                    <a href="dashboard.php" class="bg-gray-500 hover:bg-gray-600 text-white px-8 py-3 rounded-lg font-medium transition-colors">
                        Cancel
                    </a>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
