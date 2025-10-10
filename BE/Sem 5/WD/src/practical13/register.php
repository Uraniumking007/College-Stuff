<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Registration</title>
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
        input[type="password"],
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
        .clear-btn {
            background-color: #f44336;
        }
        .clear-btn:hover {
            background-color: #d32f2f;
        }
        .view-users-btn {
            background-color: #2196f3;
        }
        .view-users-btn:hover {
            background-color: #1976d2;
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
        <h2>User Registration</h2>
        
        <?php
        
        if (isset($_GET['success'])) {
            echo '<div class="success">Registration successful! <a href="users.php">View all users</a></div>';
        }
        if (isset($_GET['error'])) {
            echo '<div class="error">Error: ' . htmlspecialchars($_GET['error']) . '</div>';
        }
        ?>
        
        <form action="process_registration.php" method="POST">
            <div class="form-row">
                <div class="form-group">
                    <label for="firstName">First Name <span class="required">*</span></label>
                    <input type="text" id="firstName" name="firstName" required>
                </div>
                
                <div class="form-group">
                    <label for="lastName">Last Name <span class="required">*</span></label>
                    <input type="text" id="lastName" name="lastName" required>
                </div>
            </div>
            
            <div class="form-group">
                <label for="email">Email Address <span class="required">*</span></label>
                <input type="email" id="email" name="email" required>
                <div class="field-info">Must be a valid email format</div>
            </div>
            
            <div class="form-group">
                <label for="password">Password <span class="required">*</span></label>
                <input type="password" id="password" name="password" required>
                <div class="field-info">Minimum 8 characters</div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="phone">Phone Number <span class="required">*</span></label>
                    <input type="tel" id="phone" name="phone" required>
                </div>
                
                <div class="form-group">
                    <label for="dateOfBirth">Date of Birth <span class="required">*</span></label>
                    <input type="date" id="dateOfBirth" name="dateOfBirth" required>
                </div>
            </div>
            
            <div class="form-group">
                <label for="gender">Gender <span class="required">*</span></label>
                <select id="gender" name="gender" required>
                    <option value="">Select your gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                    <option value="prefer-not-to-say">Prefer not to say</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="address">Address</label>
                <textarea id="address" name="address" rows="3" placeholder="Enter your address (optional)"></textarea>
            </div>
            
            <div class="form-group">
                <label for="country">Country <span class="required">*</span></label>
                <select id="country" name="country" required>
                    <option value="">Select your country</option>
                    <option value="us">United States</option>
                    <option value="uk">United Kingdom</option>
                    <option value="canada">Canada</option>
                    <option value="australia">Australia</option>
                    <option value="india">India</option>
                    <option value="germany">Germany</option>
                    <option value="france">France</option>
                    <option value="japan">Japan</option>
                    <option value="other">Other</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" id="terms" name="terms" required>
                    I agree to the Terms and Conditions <span class="required">*</span>
                </label>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" id="newsletter" name="newsletter">
                    Subscribe to our newsletter for updates and offers
                </label>
            </div>
            
            <div class="button-group">
                <button type="submit">Register</button>
                <button type="reset" class="clear-btn">Clear Form</button>
                <a href="users.php"><button type="button" class="view-users-btn">View All Users</button></a>
            </div>
        </form>
    </div>
</body>
</html>
