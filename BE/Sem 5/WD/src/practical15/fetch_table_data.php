<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

$host = 'db';
$username = 'root';
$password = '';
$database = 'ajax_demo_db';

$response = [
    'success' => false,
    'message' => '',
    'data' => [],
    'total_records' => 0,
    'table_info' => []
];

try {
    $pdo = new PDO("mysql:host=$host;dbname=$database;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $tableName = isset($_GET['table']) ? trim($_GET['table']) : '';
    $page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
    $limit = isset($_GET['limit']) ? max(1, min(100, intval($_GET['limit']))) : 10;
    $search = isset($_GET['search']) ? trim($_GET['search']) : '';
    $sortColumn = isset($_GET['sort']) ? trim($_GET['sort']) : '';
    $sortOrder = isset($_GET['order']) && strtoupper($_GET['order']) === 'DESC' ? 'DESC' : 'ASC';
    
    $allowedTables = ['users', 'products', 'orders', 'departments'];
    if (!in_array($tableName, $allowedTables)) {
        $response['message'] = 'Invalid table name. Allowed tables: ' . implode(', ', $allowedTables);
        echo json_encode($response);
        exit;
    }
    
    $tableInfo = [];
    $stmt = $pdo->prepare("DESCRIBE $tableName");
    $stmt->execute();
    $columns = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    foreach ($columns as $column) {
        $tableInfo[] = [
            'name' => $column['Field'],
            'type' => $column['Type'],
            'null' => $column['Null'],
            'key' => $column['Key'],
            'default' => $column['Default']
        ];
    }
    
    $whereClause = '';
    $params = [];
    
    if (!empty($search)) {
        $searchConditions = [];
        foreach ($columns as $column) {
            $fieldName = $column['Field'];
            $searchConditions[] = "$fieldName LIKE :search_$fieldName";
            $params["search_$fieldName"] = "%$search%";
        }
        $whereClause = 'WHERE ' . implode(' OR ', $searchConditions);
    }
    
    $orderClause = '';
    if (!empty($sortColumn)) {
        $columnExists = false;
        foreach ($columns as $column) {
            if ($column['Field'] === $sortColumn) {
                $columnExists = true;
                break;
            }
        }
        
        if ($columnExists) {
            $orderClause = "ORDER BY $sortColumn $sortOrder";
        }
    }
    
    $countSql = "SELECT COUNT(*) as total FROM $tableName $whereClause";
    $countStmt = $pdo->prepare($countSql);
    $countStmt->execute($params);
    $totalRecords = $countStmt->fetch(PDO::FETCH_ASSOC)['total'];
    
    $offset = ($page - 1) * $limit;
    $totalPages = ceil($totalRecords / $limit);
    
    $sql = "SELECT * FROM $tableName $whereClause $orderClause LIMIT :limit OFFSET :offset";
    $stmt = $pdo->prepare($sql);
    
    foreach ($params as $key => $value) {
        $stmt->bindValue(":$key", $value);
    }
    $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
    $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
    
    $stmt->execute();
    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    $formattedData = [];
    foreach ($data as $row) {
        $formattedRow = [];
        foreach ($row as $key => $value) {
            if (strpos($key, 'date') !== false || strpos($key, 'created_at') !== false) {
                $formattedRow[$key] = $value ? date('Y-m-d H:i:s', strtotime($value)) : '';
            } elseif (strpos($key, 'price') !== false || strpos($key, 'salary') !== false || strpos($key, 'budget') !== false || strpos($key, 'amount') !== false) {
                $formattedRow[$key] = $value ? '$' . number_format($value, 2) : '$0.00';
            } else {
                $formattedRow[$key] = $value;
            }
        }
        $formattedData[] = $formattedRow;
    }
    
    $response['success'] = true;
    $response['message'] = "Data retrieved successfully";
    $response['data'] = $formattedData;
    $response['total_records'] = $totalRecords;
    $response['table_info'] = $tableInfo;
    $response['pagination'] = [
        'current_page' => $page,
        'total_pages' => $totalPages,
        'per_page' => $limit,
        'has_next' => $page < $totalPages,
        'has_prev' => $page > 1
    ];
    $response['search'] = $search;
    $response['sort'] = [
        'column' => $sortColumn,
        'order' => $sortOrder
    ];
    
} catch (PDOException $e) {
    $response['message'] = 'Database error: ' . $e->getMessage();
    error_log("Database error in fetch_table_data.php: " . $e->getMessage());
} catch (Exception $e) {
    $response['message'] = 'Unexpected error: ' . $e->getMessage();
    error_log("Unexpected error in fetch_table_data.php: " . $e->getMessage());
}

echo json_encode($response, JSON_PRETTY_PRINT);
?>