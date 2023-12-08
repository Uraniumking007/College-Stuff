<?php
$db_server  = "localhost";
$db_user = "root";
$db_password = "";
$db_name = "studentportal";

$connect = mysqli_connect($db_server, $db_user, $db_password, $db_name);

if (!$connect) {
    die("Connection failed: " . mysqli_connect_error());
}
// echo "Connected successfully";
