<?php
require_once 'auth.php';

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
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';
    
    if (empty($username) || empty($password)) {
        $message = 'Please enter both username and password';
        $messageType = 'error';
    } else {
        $result = $auth->login($username, $password);
        $message = $result['message'];
        $messageType = $result['success'] ? 'success' : 'error';
        
        if ($result['success']) {
            // Redirect to dashboard after successful login
            header('Location: dashboard.php');
            exit;
        }
    }
}

// Check for registration success message
if (isset($_GET['message'])) {
    $message = $_GET['message'];
    $messageType = 'success';
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - <?php echo SITE_NAME; ?></title>
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
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Welcome Back</h1>
            <p class="text-gray-600">Sign in to your account</p>
        </div>
        
        <?php if ($message): ?>
            <div class="p-4 rounded-lg mb-6 text-center <?php echo $messageType === 'error' ? 'bg-red-100 text-red-700 border border-red-300' : 'bg-green-100 text-green-700 border border-green-300'; ?>">
                <?php echo htmlspecialchars($message); ?>
            </div>
        <?php endif; ?>
        
        <form method="POST" action="">
            <div class="mb-6">
                <label for="username" class="block text-gray-700 font-medium mb-2">Username or Email</label>
                <input type="text" id="username" name="username" value="<?php echo htmlspecialchars($_POST['username'] ?? ''); ?>" required 
                       class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-primary transition-colors">
            </div>
            
            <div class="mb-8">
                <label for="password" class="block text-gray-700 font-medium mb-2">Password</label>
                <input type="password" id="password" name="password" required 
                       class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-primary transition-colors">
            </div>
            
            <button type="submit" class="w-full bg-gradient-to-r from-primary to-secondary text-white font-semibold py-3 px-6 rounded-lg hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200">
                Sign In
            </button>
        </form>
        
        <div class="text-center mt-6">
            <a href="forgot-password.php" class="text-gray-500 hover:text-primary text-sm transition-colors">Forgot your password?</a>
        </div>
        
        <div class="text-center mt-8">
            <p class="text-gray-600">Don't have an account? 
                <a href="register.php" class="text-primary hover:underline font-medium">Register here</a>
            </p>
        </div>
    </div>
</body>
</html>
