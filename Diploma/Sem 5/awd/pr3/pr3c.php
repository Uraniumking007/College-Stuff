<?php

$num1 = 25;
$num2 = 35;

function Add($a,$b){
    return $a + $b ;
}
function Sub($a,$b){
    return $a - $b ;
}
function Mul($a,$b){
    return $a * $b ;
}
function Div($a,$b){
    return $a / $b ;
}
echo "Addition of ".$num1." and ". $num2." is ".Add($num1,$num2).".";
echo "<br>";
echo "Subtraction of ".$num1." and ". $num2." is ".Sub($num1,$num2).".";
echo "<br>";
echo "Product of ".$num1." and ". $num2." is ".Mul($num1,$num2).".";
echo "<br>";
echo "Division of ".$num1." and ". $num2." is ".Div($num1,$num2).".";


?>