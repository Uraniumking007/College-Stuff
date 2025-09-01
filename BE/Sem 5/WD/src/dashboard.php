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

// Handle logout
if (isset($_GET['logout'])) {
    $result = $auth->logout();
    $message = $result['message'];
    header('Location: login.php?message=' . urlencode('Logged out successfully'));
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - <?php echo SITE_NAME; ?></title>
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
                        <li><a href="dashboard.php" class="bg-primary text-white px-4 py-2 rounded-lg font-medium">Dashboard</a></li>
                        <li><a href="profile.php" class="text-gray-700 hover:text-primary px-4 py-2 rounded-lg font-medium transition-colors">Profile</a></li>
                        <li><a href="change-password.php" class="text-gray-700 hover:text-primary px-4 py-2 rounded-lg font-medium transition-colors">Change Password</a></li>
                    </ul>
                    <a href="?logout=1" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">Logout</a>
                </div>
            </div>
        </div>
    </nav>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="bg-white rounded-xl shadow-lg p-8 mb-8 text-center">
            <h1 class="text-4xl font-bold text-gray-800 mb-4">Welcome back, <?php echo htmlspecialchars($user['username']); ?>! 👋</h1>
            <p class="text-xl text-gray-600">Here's what's happening with your account today.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">Account Status</h3>
                <div class="text-3xl font-bold text-primary mb-2">Active</div>
                <div class="text-sm text-gray-600">Your account is in good standing</div>
            </div>
            
            <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">Member Since</h3>
                <div class="text-3xl font-bold text-primary mb-2"><?php echo date('M Y', strtotime($user['created_at'])); ?></div>
                <div class="text-sm text-gray-600"><?php echo date('F j, Y', strtotime($user['created_at'])); ?></div>
            </div>
            
            <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">Last Login</h3>
                <div class="text-3xl font-bold text-primary mb-2"><?php echo $user['last_login'] ? date('M j', strtotime($user['last_login'])) : 'Never'; ?></div>
                <div class="text-sm text-gray-600"><?php echo $user['last_login'] ? date('F j, Y g:i A', strtotime($user['last_login'])) : 'First time user'; ?></div>
            </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 pb-4 border-b-2 border-gray-100">Account Information</h2>
            
            <div class="flex justify-between items-center py-4 border-b border-gray-100">
                <span class="font-medium text-gray-800">Username:</span>
                <span class="text-gray-600"><?php echo htmlspecialchars($user['username']); ?></span>
            </div>
            
            <div class="flex justify-between items-center py-4 border-b border-gray-100">
                <span class="font-medium text-gray-800">Email:</span>
                <span class="text-gray-600"><?php echo htmlspecialchars($user['email']); ?></span>
            </div>
            
            <div class="flex justify-between items-center py-4 border-b border-gray-100">
                <span class="font-medium text-gray-800">Account Created:</span>
                <span class="text-gray-600"><?php echo date('F j, Y \a\t g:i A', strtotime($user['created_at'])); ?></span>
            </div>
            
            <div class="flex justify-between items-center py-4 border-b border-gray-100">
                <span class="font-medium text-gray-800">Last Login:</span>
                <span class="text-gray-600">
                    <?php if ($user['last_login']): ?>
                        <?php echo date('F j, Y \a\t g:i A', strtotime($user['last_login'])); ?>
                    <?php else: ?>
                        Never
                    <?php endif; ?>
                </span>
            </div>
            
            <div class="flex justify-between items-center py-4">
                <span class="font-medium text-gray-800">Actions:</span>
                <div class="space-x-4">
                    <a href="profile.php" class="bg-primary hover:bg-primary/90 text-white px-6 py-2 rounded-lg font-medium transition-colors">Edit Profile</a>
                    <a href="change-password.php" class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg font-medium transition-colors">Change Password</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
