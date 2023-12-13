<?php


try {
    $con = new mysqli("localhost","root","jod","test",3306);
    //code...
    echo $con;
} catch (\Throwable $th) {
    throw $th;
}
    // $con = mysqli_connect("localhost","root","",null,3306);




?>