<?php
$host = 'db';
$username = 'root';
$password = '';
$database = 'ajax_demo_db';

try {
    $pdo = new PDO("mysql:host=$host", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $pdo->exec("CREATE DATABASE IF NOT EXISTS `$database`");
    $pdo->exec("USE `$database`");
    
    echo "<h2>Database Setup for Practical 15</h2>";
    echo "<p>Database '$database' created successfully!</p>";
    
    $tables = [
        'users' => "
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                age INT,
                city VARCHAR(50),
                department VARCHAR(50),
                salary DECIMAL(10,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ",
        'products' => "
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                price DECIMAL(10,2),
                stock_quantity INT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ",
        'orders' => "
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                product_id INT,
                quantity INT,
                total_amount DECIMAL(10,2),
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ",
        'departments' => "
            CREATE TABLE IF NOT EXISTS departments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                manager VARCHAR(100),
                budget DECIMAL(12,2),
                location VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        "
    ];
    
    foreach ($tables as $tableName => $sql) {
        $pdo->exec($sql);
        echo "<p>Table '$tableName' created successfully!</p>";
    }
    
    $sampleData = [
        'users' => [
            ['John Doe', 'john.doe@email.com', 28, 'New York', 'IT', 75000.00],
            ['Jane Smith', 'jane.smith@email.com', 32, 'Los Angeles', 'Marketing', 65000.00],
            ['Mike Johnson', 'mike.johnson@email.com', 25, 'Chicago', 'IT', 70000.00],
            ['Sarah Wilson', 'sarah.wilson@email.com', 29, 'Houston', 'HR', 60000.00],
            ['David Brown', 'david.brown@email.com', 35, 'Phoenix', 'Finance', 80000.00],
            ['Lisa Davis', 'lisa.davis@email.com', 27, 'Philadelphia', 'Marketing', 62000.00],
            ['Tom Miller', 'tom.miller@email.com', 31, 'San Antonio', 'IT', 72000.00],
            ['Emma Garcia', 'emma.garcia@email.com', 26, 'San Diego', 'HR', 58000.00]
        ],
        'products' => [
            ['Laptop Pro 15"', 'Electronics', 1299.99, 50, 'High-performance laptop for professionals'],
            ['Wireless Mouse', 'Electronics', 29.99, 200, 'Ergonomic wireless mouse with long battery life'],
            ['Office Chair', 'Furniture', 199.99, 75, 'Comfortable ergonomic office chair'],
            ['Coffee Maker', 'Appliances', 89.99, 30, 'Automatic drip coffee maker'],
            ['Notebook Set', 'Stationery', 15.99, 100, 'Set of 5 premium notebooks'],
            ['Desk Lamp', 'Furniture', 45.99, 60, 'LED desk lamp with adjustable brightness'],
            ['Bluetooth Speaker', 'Electronics', 79.99, 40, 'Portable wireless speaker with great sound'],
            ['Water Bottle', 'Accessories', 12.99, 150, 'Insulated stainless steel water bottle']
        ],
        'departments' => [
            ['Information Technology', 'John Manager', 500000.00, 'Building A, Floor 3'],
            ['Marketing', 'Jane Manager', 300000.00, 'Building B, Floor 2'],
            ['Human Resources', 'Sarah Manager', 200000.00, 'Building A, Floor 1'],
            ['Finance', 'David Manager', 400000.00, 'Building C, Floor 2'],
            ['Operations', 'Mike Manager', 350000.00, 'Building B, Floor 1']
        ]
    ];
    
    foreach ($sampleData as $tableName => $data) {
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM $tableName");
        $stmt->execute();
        $count = $stmt->fetchColumn();
        
        if ($count == 0) {
            if ($tableName === 'users') {
                $insertStmt = $pdo->prepare("INSERT INTO users (name, email, age, city, department, salary) VALUES (?, ?, ?, ?, ?, ?)");
            } elseif ($tableName === 'products') {
                $insertStmt = $pdo->prepare("INSERT INTO products (name, category, price, stock_quantity, description) VALUES (?, ?, ?, ?, ?)");
            } elseif ($tableName === 'departments') {
                $insertStmt = $pdo->prepare("INSERT INTO departments (name, manager, budget, location) VALUES (?, ?, ?, ?)");
            }
            
            foreach ($data as $row) {
                $insertStmt->execute($row);
            }
            echo "<p>Sample data inserted into '$tableName' table!</p>";
        } else {
            echo "<p>Table '$tableName' already contains data.</p>";
        }
    }
    
    $orderStmt = $pdo->prepare("SELECT COUNT(*) FROM orders");
    $orderStmt->execute();
    $orderCount = $orderStmt->fetchColumn();
    
    if ($orderCount == 0) {
        $orders = [
            [1, 1, 1, 1299.99, 'delivered'],
            [2, 2, 2, 59.98, 'shipped'],
            [3, 3, 1, 199.99, 'processing'],
            [1, 4, 1, 89.99, 'pending'],
            [4, 5, 3, 47.97, 'delivered'],
            [5, 6, 1, 45.99, 'shipped']
        ];
        
        $insertOrderStmt = $pdo->prepare("INSERT INTO orders (user_id, product_id, quantity, total_amount, status) VALUES (?, ?, ?, ?, ?)");
        foreach ($orders as $order) {
            $insertOrderStmt->execute($order);
        }
        echo "<p>Sample orders inserted!</p>";
    }
    
    echo "<h3>Setup Complete!</h3>";
    echo "<p>Database '$database' is ready with sample data.</p>";
    echo "<p><a href='table_viewer.html'>Go to Table Viewer</a></p>";
    
} catch (PDOException $e) {
    echo "<h2>Database Setup Error</h2>";
    echo "<p>Error: " . $e->getMessage() . "</p>";
    echo "<p>Please make sure MySQL is running and the credentials are correct.</p>";
}
?>