<?php
    $arr = array(10,5,2,6,4,1,3,7,9);
    echo "Unsorted Array = ";
    for ($i=0; $i < count($arr) ; $i++) { 
        echo $arr[$i];
        if($i != count($arr)-1){
            echo ",";
        }
    }
    
    echo "<br>";
     sort($arr);
     echo "Sorted Array = ";   
    for ($i=0; $i < count($arr) ; $i++) { 
        echo $arr[$i];
        if($i != count($arr)-1){
            echo ",";
        }
    }
?>
