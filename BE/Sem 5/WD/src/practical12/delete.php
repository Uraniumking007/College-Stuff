<?php
declare(strict_types=1);
require __DIR__ . '/db.php';

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
if ($id > 0) {
    $pdo = getPdo();
    $stmt = $pdo->prepare('DELETE FROM pr12_users WHERE id = ?');
    $stmt->execute([$id]);
}
header('Location: /practical12/list.php');
<<<<<<< HEAD
exit;


=======
exit;
>>>>>>> f7ea692be64aab11baa01cb5e55267ad5982c00a
