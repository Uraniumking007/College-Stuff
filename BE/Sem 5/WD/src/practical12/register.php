<?php
declare(strict_types=1);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Registration</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; }
        form { max-width: 400px; padding: 1rem; border: 1px solid #ddd; border-radius: 8px; }
        label { display: block; margin-top: .5rem; }
        input { width: 100%; padding: .5rem; margin-top: .25rem; }
        button { margin-top: 1rem; padding: .5rem 1rem; }
        .nav { margin-bottom: 1rem; }
        .nav a { margin-right: 1rem; }
    </style>
    
</head>
<body>
    <div class="nav">
        <a href="/practical12/register.php">Register</a>
        <a href="/practical12/list.php">Users</a>
    </div>
    <h1>Register</h1>
    <form method="post" action="/practical12/create.php">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" required />

        <label for="email">Email</label>
        <input type="email" id="email" name="email" required />

        <button type="submit">Submit</button>
    </form>
</body>
</html>


