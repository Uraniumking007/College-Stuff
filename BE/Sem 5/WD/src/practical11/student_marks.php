<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Marks - Highest Score Finder</title>
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
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            background-color: #6f42c1;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            margin-top: 10px;
        }
        button:hover {
            background-color: #5a32a3;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background-color: #e2e3e5;
            border-radius: 5px;
            border-left: 4px solid #6f42c1;
        }
        .winner {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .student-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: white;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .student-table th, .student-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .student-table th {
            background-color: #6f42c1;
            color: white;
            font-weight: bold;
        }
        .student-table tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .student-table tr:hover {
            background-color: #e9ecef;
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
        .info {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #17a2b8;
        }
        .form-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .form-row {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        .form-row input {
            flex: 1;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 Student Marks - Highest Score Finder</h1>
        
        <div class="info">
            <strong>How it works:</strong><br>
            This script finds the student with the highest marks among 10 students. 
            You can either use the pre-defined data or enter your own student data.
        </div>



        <!-- Custom Student Input Form -->
        <div class="form-container">
            <h3>📝 Enter Your Own Student Data</h3>
            <form method="POST">
                <?php
                for ($i = 1; $i <= 10; $i++) {
                    echo "<div class='form-row'>";
                    echo "<input type='text' name='names[]' placeholder='Student $i Name' required>";
                    echo "<input type='number' name='marks[]' placeholder='Marks' min='0' max='100' required>";
                    echo "</div>";
                }
                ?>
                <button type="submit">Find Highest Scorer</button>
            </form>

            <?php
            if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['names']) && isset($_POST['marks'])) {
                $names = $_POST['names'];
                $marks = $_POST['marks'];
                
                if (count($names) == 10 && count($marks) == 10) {
                    $customStudents = [];
                    $highestMarks = 0;
                    $topStudent = '';
                    
                    for ($i = 0; $i < 10; $i++) {
                        $customStudents[] = [
                            'name' => $names[$i],
                            'marks' => (int)$marks[$i]
                        ];
                        
                        if ((int)$marks[$i] > $highestMarks) {
                            $highestMarks = (int)$marks[$i];
                            $topStudent = $names[$i];
                        }
                    }
                    
                    echo "<div class='result'>";
                    echo "<h3>Your Student Data Results:</h3>";
                    
                    // Display custom student table
                    echo "<table class='student-table'>";
                    echo "<tr><th>Student Name</th><th>Marks</th></tr>";
                    
                    foreach ($customStudents as $student) {
                        $rowClass = ($student['name'] === $topStudent) ? 'style="background-color: #d4edda; font-weight: bold;"' : '';
                        echo "<tr $rowClass>";
                        echo "<td>" . htmlspecialchars($student['name']) . "</td>";
                        echo "<td>" . $student['marks'] . "</td>";
                        echo "</tr>";
                    }
                    echo "</table>";
                    
                    // Display winner
                    echo "<div class='winner'>";
                    echo "🏆 <strong>" . htmlspecialchars($topStudent) . "</strong> has the highest marks: <strong>$highestMarks</strong> 🏆";
                    echo "</div>";
                    echo "</div>";
                } else {
                    echo "<div class='result'>Please enter data for all 10 students!</div>";
                }
            }
            ?>
        </div>
    </div>
</body>
</html>
