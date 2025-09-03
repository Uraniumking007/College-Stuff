<?php
declare(strict_types=1);
require __DIR__ . '/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /practical12/register.php');
    exit;
}

$name = trim($_POST['name'] ?? '');
$email = trim($_POST['email'] ?? '');

if ($name === '' || $email === '') {
    header('Location: /practical12/register.php');
    exit;
}

$pdo = getPdo();
$stmt = $pdo->prepare('INSERT INTO pr12_users (name, email) VALUES (?, ?)');
try {
    $stmt->execute([$name, $email]);
} catch (PDOException $e) {
    // On duplicate email, just redirect back for simplicity
    header('Location: /practical12/register.php');
    exit;
}

header('Location: /practical12/list.php');
exit;


