<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prime Numbers Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
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
            background-color: #dc3545;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #c82333;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background-color: #f8d7da;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
        }
        .prime-numbers {
            font-family: 'Courier New', monospace;
            font-size: 16px;
            line-height: 1.6;
            color: #721c24;
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
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
        .examples .prime-numbers {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .info {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #17a2b8;
        }
        .warning {
            background-color: #fff3cd;
            color: #856404;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #ffc107;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔢 Prime Numbers Generator</h1>
        
        <div class="info">
            <strong>What are Prime Numbers?</strong><br>
            A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.
            <br>First few prime numbers: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, ...
        </div>
        
        <form method="POST">
            <div class="form-group">
                <label for="count">Enter how many prime numbers you want:</label>
                <input type="number" id="count" name="count" min="1" max="100" required placeholder="Enter a number between 1-100">
            </div>
            <button type="submit">Generate Prime Numbers</button>
        </form>

        <?php
        function isPrime($number) {
            if ($number < 2) return false;
            if ($number == 2) return true;
            if ($number % 2 == 0) return false;
            
            for ($i = 3; $i <= sqrt($number); $i += 2) {
                if ($number % $i == 0) return false;
            }
            return true;
        }

        function generatePrimes($count) {
            $primes = [];
            $number = 2;
            
            while (count($primes) < $count) {
                if (isPrime($number)) {
                    $primes[] = $number;
                }
                $number++;
            }
            
            return $primes;
        }

        if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['count'])) {
            $count = (int)$_POST['count'];
            
            if ($count > 0 && $count <= 100) {
                $primes = generatePrimes($count);
                
                echo "<div class='result'>";
                echo "<h3>First $count Prime Numbers:</h3>";
                echo "<div class='prime-numbers'>";
                echo implode(", ", $primes);
                echo "</div>";
                echo "<p><strong>Total prime numbers generated: " . count($primes) . "</strong></p>";
                echo "</div>";
                
                if ($count > 50) {
                    echo "<div class='warning'>";
                    echo "<strong>Note:</strong> Generating many prime numbers may take a moment.";
                    echo "</div>";
                }
            } else {
                echo "<div class='result'>Please enter a valid number between 1 and 100!</div>";
            }
        }
        ?>

        <div class="examples">
            <h3>📚 Example Prime Numbers:</h3>
            
            <?php
            $exampleCounts = [5, 10, 20];
            
            foreach ($exampleCounts as $count) {
                $primes = generatePrimes($count);
                
                echo "<div class='examples'>";
                echo "<h4>First $count Prime Numbers:</h4>";
                echo "<div class='prime-numbers'>";
                echo implode(", ", $primes);
                echo "</div>";
                echo "<p><strong>Count: " . count($primes) . " numbers</strong></p>";
                echo "</div>";
            }
            ?>
        </div>
    </div>
</body>
</html>
