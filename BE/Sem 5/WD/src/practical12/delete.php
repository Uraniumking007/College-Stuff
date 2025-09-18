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
exit;