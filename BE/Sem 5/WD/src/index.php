<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Web Development Practicals</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 2rem; 
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 2rem;
            border-bottom: 3px solid #3498db;
            padding-bottom: 1rem;
        }
        .practical-section {
            margin-bottom: 2rem;
            padding: 1.5rem;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            background-color: #fafafa;
        }
        .practical-section h2 {
            color: #34495e;
            margin-top: 0;
            border-left: 4px solid #3498db;
            padding-left: 1rem;
        }
        .practical-links {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 1rem;
        }
        .practical-links a {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s, transform 0.2s;
            font-weight: 500;
        }
        .practical-links a:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
        }
        .description {
            color: #666;
            margin-bottom: 1rem;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Web Development Practicals</h1>
        
        <div class="practical-section">
            <h2>Practical 2: Timetable</h2>
            <div class="description">HTML table creation with timetable layout</div>
            <div class="practical-links">
                <a href="/practical2/timetable.html">Timetable</a>
            </div>
        </div>

        <div class="practical-section">
            <h2>Practical 3: Resume</h2>
            <div class="description">HTML resume page with structured content</div>
            <div class="practical-links">
                <a href="/practical3/resume.html">Resume</a>
            </div>
        </div>

        <div class="practical-section">
            <h2>Practical 4: Catalogue & Login</h2>
            <div class="description">HTML catalogue page and login form</div>
            <div class="practical-links">
                <a href="/practical4/catalogue.html">Catalogue</a>
                <a href="/practical4/index.html">Home</a>
                <a href="/practical4/login.html">Login</a>
            </div>
        </div>

        <div class="practical-section">
            <h2>Practical 5: Registration</h2>
            <div class="description">HTML registration form</div>
            <div class="practical-links">
                <a href="/practical5/registration.html">Registration Form</a>
            </div>
        </div>

        <div class="practical-section">
            <h2>Practical 6: Frames</h2>
            <div class="description">HTML frames and iframes demonstration</div>
            <div class="practical-links">
                <a href="/practical6/frames.html">Main Frames Page</a>
                <a href="/practical6/navigationframes.html">Navigation Frames</a>
                <a href="/practical6/floatingframes.html">Floating Frames</a>
            </div>
        </div>

        <div class="practical-section">
            <h2>Practical 11: PHP Programming Scripts</h2>
            <div class="description">PHP scripts for various programming concepts and algorithms</div>
            <div class="practical-links">
                <a href="/practical11/index.php">Main Index</a>
                <a href="/practical11/odd_even.php">Odd/Even Checker</a>
                <a href="/practical11/fibonacci.php">Fibonacci Series</a>
                <a href="/practical11/prime_numbers.php">Prime Numbers</a>
                <a href="/practical11/student_marks.php">Student Marks</a>
                <a href="/practical11/string_converter.php">String Converter</a>
            </div>
        </div>

        <div class="practical-section">
            <h2>Practical 12: PHP Database Operations</h2>
            <div class="description">PHP CRUD operations with MySQL database</div>
            <div class="practical-links">
                <a href="/practical12/register.php">Register</a>
                <a href="/practical12/list.php">Users List</a>
                <a href="/practical12/create.php">Create User</a>
                <a href="/practical12/update.php">Update User</a>
                <a href="/practical12/delete.php">Delete User</a>
            </div>
        </div>
    </div>
</body>
</html>