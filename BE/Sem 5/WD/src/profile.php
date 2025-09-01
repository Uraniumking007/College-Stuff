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
    $username = trim($_POST['username'] ?? '');
    $email = trim($_POST['email'] ?? '');
    
    // Validate input
    if (empty($username) || empty($email)) {
        $message = 'All fields are required';
        $messageType = 'error';
    } elseif (strlen($username) < 3 || strlen($username) > 50) {
        $message = 'Username must be between 3 and 50 characters';
        $messageType = 'error';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $message = 'Invalid email format';
        $messageType = 'error';
    } else {
        try {
            $pdo = getDBConnection();
            
            // Check if username or email already exists (excluding current user)
            $stmt = $pdo->prepare("SELECT id FROM users WHERE (username = ? OR email = ?) AND id != ?");
            $stmt->execute([$username, $email, $user['id']]);
            
            if ($stmt->fetch()) {
                $message = 'Username or email already exists';
                $messageType = 'error';
            } else {
                // Update user profile
                $stmt = $pdo->prepare("UPDATE users SET username = ?, email = ? WHERE id = ?");
                $stmt->execute([$username, $email, $user['id']]);
                
                $message = 'Profile updated successfully!';
                $messageType = 'success';
                
                // Refresh user data
                $user = $auth->getCurrentUser();
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
    <title>Profile - <?php echo SITE_NAME; ?></title>
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
                        <li><a href="profile.php" class="bg-primary text-white px-4 py-2 rounded-lg font-medium">Profile</a></li>
                        <li><a href="change-password.php" class="text-gray-700 hover:text-primary px-4 py-2 rounded-lg font-medium transition-colors">Change Password</a></li>
                    </ul>
                    <a href="dashboard.php?logout=1" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">Logout</a>
                </div>
            </div>
        </div>
    </nav>
    
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="bg-white rounded-xl shadow-lg p-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Profile Settings</h1>
            
            <?php if ($message): ?>
                <div class="p-4 rounded-lg mb-6 text-center <?php echo $messageType === 'error' ? 'bg-red-100 text-red-700 border border-red-300' : 'bg-green-100 text-green-700 border border-green-300'; ?>">
                    <?php echo htmlspecialchars($message); ?>
                </div>
            <?php endif; ?>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                <div class="bg-gray-50 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4 pb-2 border-b-2 border-gray-200">Account Information</h3>
                    <div class="flex justify-between items-center py-3 border-b border-gray-200">
                        <span class="font-medium text-gray-800">User ID:</span>
                        <span class="text-gray-600">#<?php echo $user['id']; ?></span>
                    </div>
                    <div class="flex justify-between items-center py-3 border-b border-gray-200">
                        <span class="font-medium text-gray-800">Member Since:</span>
                        <span class="text-gray-600"><?php echo date('F j, Y', strtotime($user['created_at'])); ?></span>
                    </div>
                    <div class="flex justify-between items-center py-3">
                        <span class="font-medium text-gray-800">Last Login:</span>
                        <span class="text-gray-600">
                            <?php if ($user['last_login']): ?>
                                <?php echo date('F j, Y g:i A', strtotime($user['last_login'])); ?>
                            <?php else: ?>
                                Never
                            <?php endif; ?>
                        </span>
                    </div>
                </div>
                
                <div class="bg-gray-50 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4 pb-2 border-b-2 border-gray-200">Current Profile</h3>
                    <div class="flex justify-between items-center py-3 border-b border-gray-200">
                        <span class="font-medium text-gray-800">Username:</span>
                        <span class="text-gray-600"><?php echo htmlspecialchars($user['username']); ?></span>
                    </div>
                    <div class="flex justify-between items-center py-3">
                        <span class="font-medium text-gray-800">Email:</span>
                        <span class="text-gray-600"><?php echo htmlspecialchars($user['email']); ?></span>
                    </div>
                </div>
            </div>
            
            <form method="POST" action="" class="mb-8">
                <h3 class="text-xl font-semibold text-gray-800 mb-6">Edit Profile</h3>
                
                <div class="mb-6">
                    <label for="username" class="block text-gray-700 font-medium mb-2">Username</label>
                    <input type="text" id="username" name="username" value="<?php echo htmlspecialchars($user['username']); ?>" required 
                           class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-primary transition-colors">
                </div>
                
                <div class="mb-8">
                    <label for="email" class="block text-gray-700 font-medium mb-2">Email</label>
                    <input type="email" id="email" name="email" value="<?php echo htmlspecialchars($user['email']); ?>" required 
                           class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-primary transition-colors">
                </div>
                
                <div class="flex gap-4 justify-center">
                    <button type="submit" class="bg-primary hover:bg-primary/90 text-white px-8 py-3 rounded-lg font-medium transition-colors">
                        Update Profile
                    </button>
                    <a href="dashboard.php" class="bg-gray-500 hover:bg-gray-600 text-white px-8 py-3 rounded-lg font-medium transition-colors">
                        Cancel
                    </a>
                </div>
            </form>
            
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
                <h3 class="text-lg font-semibold text-yellow-800 mb-3">Account Actions</h3>
                <p class="text-yellow-700 mb-4">Manage your account settings and security preferences.</p>
                <a href="change-password.php" class="bg-primary hover:bg-primary/90 text-white px-6 py-2 rounded-lg font-medium transition-colors">
                    Change Password
                </a>
            </div>
            
            <div class="bg-red-50 border border-red-200 rounded-lg p-6">
                <h4 class="text-lg font-semibold text-red-800 mb-3">⚠️ Danger Zone</h4>
                <p class="text-red-700 mb-4">These actions cannot be undone. Please proceed with caution.</p>
                <button class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-medium transition-colors" 
                        onclick="alert('Account deletion feature not implemented in this demo.')">
                    Delete Account
                </button>
            </div>
        </div>
    </div>
</body>
</html>
