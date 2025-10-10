<?php
declare(strict_types=1);
require __DIR__ . '/db.php';

$pdo = getPdo();
$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
if ($id <= 0) {
    header('Location: /practical12/list.php');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    if ($name !== '' && $email !== '') {
        $stmt = $pdo->prepare('UPDATE pr12_users SET name = ?, email = ? WHERE id = ?');
        try {
            $stmt->execute([$name, $email, $id]);
        } catch (PDOException $e) {
            
        }
        header('Location: /practical12/list.php');
        exit;
    }
}

$stmt = $pdo->prepare('SELECT id, name, email FROM pr12_users WHERE id = ?');
$stmt->execute([$id]);
$user = $stmt->fetch();
if (!$user) {
    header('Location: /practical12/list.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Edit User</title>
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
    <h1>Edit User #<?php echo (int)$user['id']; ?></h1>
    <form method="post">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" required value="<?php echo htmlspecialchars($user['name']); ?>" />

        <label for="email">Email</label>
        <input type="email" id="email" name="email" required value="<?php echo htmlspecialchars($user['email']); ?>" />

        <button type="submit">Save</button>
    </form>
</body>
</html>


