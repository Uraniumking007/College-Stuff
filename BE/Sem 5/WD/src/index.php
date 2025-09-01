<?php
require_once 'config.php';
require_once 'auth.php';

$auth = new Auth();
$isLoggedIn = $auth->isLoggedIn();
$user = $isLoggedIn ? $auth->getCurrentUser() : null;
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo SITE_NAME; ?></title>
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
<body class="min-h-screen bg-gradient-to-br from-primary to-secondary">
    <div class="container mx-auto px-4 py-16">
        <div class="text-center mb-16">
            <h1 class="text-5xl font-bold text-white mb-6"><?php echo SITE_NAME; ?></h1>
            <p class="text-xl text-white/90 max-w-2xl mx-auto">
                A secure and modern PHP authentication system with session management, 
                user registration, login, and profile management.
            </p>
        </div>

        <?php if ($isLoggedIn): ?>
            <!-- User is logged in -->
            <div class="max-w-4xl mx-auto">
                <div class="bg-white rounded-2xl shadow-2xl p-8 mb-8">
                    <div class="text-center mb-8">
                        <h2 class="text-3xl font-bold text-gray-800 mb-4">Welcome back, <?php echo htmlspecialchars($user['username']); ?>! 🎉</h2>
                        <p class="text-gray-600">You're successfully logged in to your account.</p>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                        <div class="bg-gray-50 rounded-xl p-6 text-center">
                            <div class="text-2xl font-bold text-primary mb-2">Dashboard</div>
                            <p class="text-gray-600 text-sm">View your account overview</p>
                        </div>
                        <div class="bg-gray-50 rounded-xl p-6 text-center">
                            <div class="text-2xl font-bold text-primary mb-2">Profile</div>
                            <p class="text-gray-600 text-sm">Manage your account details</p>
                        </div>
                        <div class="bg-gray-50 rounded-xl p-6 text-center">
                            <div class="text-2xl font-bold text-primary mb-2">Security</div>
                            <p class="text-gray-600 text-sm">Change password & settings</p>
                        </div>
                    </div>
                    
                    <div class="flex flex-wrap gap-4 justify-center">
                        <a href="dashboard.php" class="bg-primary hover:bg-primary/90 text-white px-8 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:-translate-y-1">
                            Go to Dashboard
                        </a>
                        <a href="profile.php" class="bg-gray-600 hover:bg-gray-700 text-white px-8 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:-translate-y-1">
                            Edit Profile
                        </a>
                        <a href="dashboard.php?logout=1" class="bg-red-500 hover:bg-red-600 text-white px-8 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:-translate-y-1">
                            Logout
                        </a>
                    </div>
                </div>
            </div>
        <?php else: ?>
            <!-- User is not logged in -->
            <div class="max-w-4xl mx-auto">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                    <div class="bg-white rounded-2xl shadow-2xl p-8">
                        <div class="text-center mb-6">
                            <h3 class="text-2xl font-bold text-gray-800 mb-3">New User?</h3>
                            <p class="text-gray-600">Create your account to get started with our secure authentication system.</p>
                        </div>
                        <ul class="text-gray-600 space-y-3 mb-8">
                            <li class="flex items-center"><span class="mr-2 text-green-500">✓</span>Secure password hashing</li>
                            <li class="flex items-center"><span class="mr-2 text-green-500">✓</span>Session management</li>
                            <li class="flex items-center"><span class="mr-2 text-green-500">✓</span>Account protection</li>
                            <li class="flex items-center"><span class="mr-2 text-green-500">✓</span>Profile customization</li>
                        </ul>
                        <a href="register.php" class="block w-full bg-primary hover:bg-primary/90 text-white text-center py-3 px-6 rounded-lg font-semibold transition-all duration-200 transform hover:-translate-y-1">
                            Create Account
                        </a>
                    </div>
                    
                    <div class="bg-white rounded-2xl shadow-2xl p-8">
                        <div class="text-center mb-6">
                            <h3 class="text-2xl font-bold text-gray-800 mb-3">Returning User?</h3>
                            <p class="text-gray-600">Sign in to access your account and manage your profile.</p>
                        </div>
                        <ul class="text-gray-600 space-y-3 mb-8">
                            <li class="flex items-center"><span class="mr-2 text-blue-500">✓</span>Quick login access</li>
                            <li class="flex items-center"><span class="mr-2 text-blue-500">✓</span>Secure authentication</li>
                            <li class="flex items-center"><span class="mr-2 text-blue-500">✓</span>Password recovery</li>
                            <li class="flex items-center"><span class="mr-2 text-blue-500">✓</span>Account dashboard</li>
                        </ul>
                        <a href="login.php" class="block w-full bg-secondary hover:bg-secondary/90 text-white text-center py-3 px-6 rounded-lg font-semibold transition-all duration-200 transform hover:-translate-y-1">
                            Sign In
                        </a>
                    </div>
                </div>
                
                <div class="bg-white rounded-2xl shadow-2xl p-8">
                    <h3 class="text-2xl font-bold text-gray-800 mb-6 text-center">Features</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div class="text-center">
                            <div class="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span class="text-2xl">🔐</span>
                            </div>
                            <h4 class="font-semibold text-gray-800 mb-2">Secure Auth</h4>
                            <p class="text-gray-600 text-sm">BCrypt password hashing with configurable cost</p>
                        </div>
                        <div class="text-center">
                            <div class="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span class="text-2xl">🛡️</span>
                            </div>
                            <h4 class="font-semibold text-gray-800 mb-2">Session Security</h4>
                            <p class="text-gray-600 text-sm">Secure session handling with timeout protection</p>
                        </div>
                        <div class="text-center">
                            <div class="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span class="text-2xl">🚫</span>
                            </div>
                            <h4 class="font-semibold text-gray-800 mb-2">Brute Force Protection</h4>
                            <p class="text-gray-600 text-sm">Account lockout after failed login attempts</p>
                        </div>
                        <div class="text-center">
                            <div class="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span class="text-2xl">📱</span>
                            </div>
                            <h4 class="font-semibold text-gray-800 mb-2">Responsive Design</h4>
                            <p class="text-gray-600 text-sm">Modern UI with Tailwind CSS framework</p>
                        </div>
                    </div>
                </div>
            </div>
        <?php endif; ?>
        
        <div class="text-center mt-16">
            <p class="text-white/70 text-sm">
                Built with PHP, MySQL, and Tailwind CSS | Secure authentication system
            </p>
        </div>
    </div>
</body>
</html>