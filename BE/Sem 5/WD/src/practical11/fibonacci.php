<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fibonacci Series Generator</title>
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
            background-color: #28a745;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #218838;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background-color: #e9ecef;
            border-radius: 5px;
            border-left: 4px solid #28a745;
        }
        .fibonacci-series {
            font-family: 'Courier New', monospace;
            font-size: 16px;
            line-height: 1.6;
            color: #495057;
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
        .examples .fibonacci-series {
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
    </style>
</head>
<body>
    <div class="container">
        <h1>🌿 Fibonacci Series Generator</h1>
        
        <div class="info">
            <strong>What is Fibonacci Series?</strong><br>
            A sequence where each number is the sum of the two preceding ones, usually starting with 0 and 1.
            <br>Example: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
        </div>
        
        <form method="POST">
            <div class="form-group">
                <label for="limit">Enter the limit (up to which number):</label>
                <input type="number" id="limit" name="limit" min="1" max="1000" required placeholder="Enter a positive number">
            </div>
            <button type="submit">Generate Fibonacci Series</button>
        </form>

        <?php
        function generateFibonacci($limit) {
            $fibonacci = [0, 1];
            $i = 2;
            
            while (true) {
                $next = $fibonacci[$i-1] + $fibonacci[$i-2];
                if ($next > $limit) {
                    break;
                }
                $fibonacci[] = $next;
                $i++;
            }
            
            return $fibonacci;
        }

        if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['limit'])) {
            $limit = (int)$_POST['limit'];
            
            if ($limit > 0) {
                $series = generateFibonacci($limit);
                $count = count($series);
                
                echo "<div class='result'>";
                echo "<h3>Fibonacci Series up to $limit:</h3>";
                echo "<div class='fibonacci-series'>";
                echo implode(", ", $series);
                echo "</div>";
                echo "<p><strong>Total numbers in series: $count</strong></p>";
                echo "</div>";
            } else {
                echo "<div class='result'>Please enter a positive number!</div>";
            }
        }
        ?>

        <div class="examples">
            <h3>📚 Example Series:</h3>
            
            <?php
            $exampleLimits = [10, 50, 100];
            
            foreach ($exampleLimits as $limit) {
                $series = generateFibonacci($limit);
                $count = count($series);
                
                echo "<div class='examples'>";
                echo "<h4>Fibonacci Series up to $limit:</h4>";
                echo "<div class='fibonacci-series'>";
                echo implode(", ", $series);
                echo "</div>";
                echo "<p><strong>Count: $count numbers</strong></p>";
                echo "</div>";
            }
            ?>
        </div>
    </div>
</body>
</html>
