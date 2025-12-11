<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>String Case Converter</title>
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
        textarea {
            width: 100%;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            min-height: 100px;
            resize: vertical;
            font-family: Arial, sans-serif;
        }
        .button-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        button {
            flex: 1;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        .btn-uppercase {
            background-color: #007bff;
            color: white;
        }
        .btn-uppercase:hover {
            background-color: #0056b3;
        }
        .btn-lowercase {
            background-color: #28a745;
            color: white;
        }
        .btn-lowercase:hover {
            background-color: #218838;
        }

        .btn-clear {
            background-color: #6c757d;
            color: white;
        }
        .btn-clear:hover {
            background-color: #5a6268;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        .result h3 {
            margin-top: 0;
            color: #495057;
        }
        .converted-text {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #dee2e6;
            font-family: 'Courier New', monospace;
            font-size: 16px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
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
        <h1>🔤 String Case Converter</h1>
        
        <div class="info">
            <strong>Available Functions:</strong><br>
            • <code>toUpperCase($string)</code> - Converts string to UPPERCASE<br>
            • <code>toLowerCase($string)</code> - Converts string to lowercase
        </div>
        
        <form method="POST">
            <div class="form-group">
                <label for="inputText">Enter your text:</label>
                <textarea id="inputText" name="inputText" placeholder="Type or paste your text here..."><?php echo isset($_POST['inputText']) ? htmlspecialchars($_POST['inputText']) : 'Hello World! This is a sample text for demonstration.'; ?></textarea>
            </div>
            
            <div class="button-group">
                <button type="submit" name="action" value="uppercase" class="btn-uppercase">🔠 UPPERCASE</button>
                <button type="submit" name="action" value="lowercase" class="btn-lowercase">🔡 lowercase</button>
                <button type="submit" name="action" value="clear" class="btn-clear">🗑️ Clear</button>
            </div>
        </form>

        <?php
<<<<<<< HEAD
        // PHP Functions for string conversion
=======
        
>>>>>>> f7ea692be64aab11baa01cb5e55267ad5982c00a
        function toUpperCase($string) {
            return strtoupper($string);
        }

        function toLowerCase($string) {
            return strtolower($string);
        }



<<<<<<< HEAD
        // Handle form submission
=======
        
>>>>>>> f7ea692be64aab11baa01cb5e55267ad5982c00a
        if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['action'])) {
            $action = $_POST['action'];
            $inputText = $_POST['inputText'] ?? '';
            
            if ($action === 'clear') {
                $inputText = '';
            } elseif (!empty($inputText)) {
                $result = '';
                $actionName = '';
                
                switch ($action) {
                    case 'uppercase':
                        $result = toUpperCase($inputText);
                        $actionName = 'UPPERCASE';
                        break;
                    case 'lowercase':
                        $result = toLowerCase($inputText);
                        $actionName = 'lowercase';
                        break;
                }
                
                if ($result !== '') {
                    echo "<div class='result'>";
                    echo "<h3>Converted to $actionName:</h3>";
                    echo "<div class='converted-text'>" . htmlspecialchars($result) . "</div>";
                    echo "</div>";
                }
            }
        }
        ?>




    </div>

    <script>
<<<<<<< HEAD
        // Clear button functionality
=======
        
>>>>>>> f7ea692be64aab11baa01cb5e55267ad5982c00a
        document.querySelector('button[value="clear"]').addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('inputText').value = '';
        });
    </script>
</body>
</html>
