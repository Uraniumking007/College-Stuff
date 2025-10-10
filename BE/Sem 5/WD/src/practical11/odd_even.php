<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Odd or Even Number Checker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
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
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .even {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .odd {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .examples {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        .examples h3 {
            color: #495057;
            margin-bottom: 15px;
        }
        .examples p {
            margin: 5px 0;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔢 Odd or Even Number Checker</h1>
        
        <form method="POST">
            <div class="form-group">
                <label for="number">Enter a number:</label>
                <input type="number" id="number" name="number" required placeholder="Enter any integer">
            </div>
            <button type="submit">Check Number</button>
        </form>

        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['number'])) {
            $number = $_POST['number'];
            
            if (is_numeric($number)) {
                $result = ($number % 2 == 0) ? "EVEN" : "ODD";
                $class = ($number % 2 == 0) ? "even" : "odd";
                
                echo "<div class='result $class'>";
                echo "The number <strong>$number</strong> is <strong>$result</strong>";
                echo "</div>";
            } else {
                echo "<div class='result odd'>Please enter a valid number!</div>";
            }
        }
        ?>

        <div class="examples">
            <h3>📚 Examples:</h3>
            <?php
            
            $testNumbers = [2, 7, 10, 15, 22, 33, 100, 101];
            
            foreach ($testNumbers as $num) {
                $result = ($num % 2 == 0) ? "EVEN" : "ODD";
                echo "<p><strong>$num</strong> is <strong>$result</strong></p>";
            }
            ?>
        </div>
    </div>
</body>
</html>
