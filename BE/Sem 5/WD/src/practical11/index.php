<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Practical 11 - PHP Scripts Collection</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #007bff;
            padding-bottom: 15px;
        }
        .script-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .script-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-decoration: none;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .script-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .script-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        .script-card:hover::before {
            left: 100%;
        }
        .script-card h3 {
            margin: 0 0 15px 0;
            font-size: 20px;
            font-weight: bold;
        }
        .script-card p {
            margin: 0;
            opacity: 0.9;
            line-height: 1.5;
        }
        .script-card .icon {
            font-size: 24px;
            margin-bottom: 15px;
            display: block;
        }
        .description {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #17a2b8;
        }
        .description h2 {
            color: #495057;
            margin-top: 0;
        }
        .description ul {
            color: #6c757d;
            line-height: 1.6;
        }
        .description li {
            margin-bottom: 8px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background-color: #e9ecef;
            border-radius: 5px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Practical 11 - PHP Scripts Collection</h1>
        
        <div class="description">
            <h2>📋 Overview</h2>
            <p>This collection contains PHP scripts demonstrating various programming concepts and algorithms:</p>
            <ul>
                <li><strong>Odd/Even Checker:</strong> Determines if a number is odd or even</li>
                <li><strong>Fibonacci Series:</strong> Generates Fibonacci sequence up to a given limit</li>
                <li><strong>Prime Numbers:</strong> Generates the first N prime numbers</li>
                <li><strong>Student Marks:</strong> Finds the student with highest marks among 10 students</li>
                <li><strong>String Converter:</strong> Converts strings to uppercase, lowercase, and title case</li>
            </ul>
        </div>

        <div class="script-grid">
            <a href="odd_even.php" class="script-card">
                <span class="icon">🔢</span>
                <h3>Odd or Even Checker</h3>
                <p>Check if a number is odd or even with interactive form and examples</p>
            </a>

            <a href="fibonacci.php" class="script-card">
                <span class="icon">🌿</span>
                <h3>Fibonacci Series Generator</h3>
                <p>Generate Fibonacci sequence up to a given number with detailed explanations</p>
            </a>

            <a href="prime_numbers.php" class="script-card">
                <span class="icon">🔢</span>
                <h3>Prime Numbers Generator</h3>
                <p>Generate the first N prime numbers with efficient algorithm and examples</p>
            </a>

            <a href="student_marks.php" class="script-card">
                <span class="icon">🏆</span>
                <h3>Student Marks - Highest Score Finder</h3>
                <p>Find the student with highest marks among 10 students with data visualization</p>
            </a>

            <a href="string_converter.php" class="script-card">
                <span class="icon">🔤</span>
                <h3>String Case Converter</h3>
                <p>Convert strings to uppercase, lowercase, and title case with interactive interface</p>
            </a>
        </div>

        <div class="footer">
            <p><strong>Instructions:</strong> Click on any card above to run the corresponding PHP script</p>
            <p><strong>Note:</strong> All scripts include both functionality and examples for learning purposes</p>
        </div>
    </div>
</body>
</html>
