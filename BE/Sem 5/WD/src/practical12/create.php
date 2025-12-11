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
<<<<<<< HEAD
    // On duplicate email, just redirect back for simplicity
=======
    
>>>>>>> f7ea692be64aab11baa01cb5e55267ad5982c00a
    header('Location: /practical12/register.php');
    exit;
}

header('Location: /practical12/list.php');
exit;


