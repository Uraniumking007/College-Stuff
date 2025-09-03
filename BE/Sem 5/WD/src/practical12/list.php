<?php
declare(strict_types=1);
require __DIR__ . '/db.php';

$pdo = getPdo();
$users = $pdo->query('SELECT id, name, email, created_at FROM pr12_users ORDER BY id DESC')->fetchAll();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Users</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: .5rem; }
        th { background: #f2f2f2; }
        .nav { margin-bottom: 1rem; }
        .nav a { margin-right: 1rem; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/practical12/register.php">Register</a>
        <a href="/practical12/list.php">Users</a>
    </div>
    <h1>Users</h1>
    <?php if (empty($users)): ?>
        <p>No users yet.</p>
    <?php else: ?>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Created</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($users as $u): ?>
                <tr>
                    <td><?php echo (int)$u['id']; ?></td>
                    <td><?php echo htmlspecialchars($u['name']); ?></td>
                    <td><?php echo htmlspecialchars($u['email']); ?></td>
                    <td><?php echo htmlspecialchars($u['created_at']); ?></td>
                    <td>
                        <a href="/practical12/update.php?id=<?php echo (int)$u['id']; ?>">Edit</a>
                        |
                        <a href="/practical12/delete.php?id=<?php echo (int)$u['id']; ?>" onclick="return confirm('Delete this user?');">Delete</a>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    <?php endif; ?>
</body>
</html>


