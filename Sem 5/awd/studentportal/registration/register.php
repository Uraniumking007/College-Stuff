<?php
include '../db.php';

if (isset($_POST)) {
    $name = $_POST['name'];
    $department = $_POST['department'];
    $gender = $_POST['gender'];

    $registerQuery = "insert into students(name,department,gender) values('$name','$department','$gender')";
    $result = mysqli_query($connect, $registerQuery);

    if ($result) {
        header("Location: ../index.php");
    } else {
        echo "Error: " . $registerQuery . "<br>" . mysqli_error($connect);
    }
}
