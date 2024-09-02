<?php

    $products = array("Pencil"=>array(25,6),"Pen"=>array(25,4),"Books"=>array(25,2));
    $billAmount = 0;
    count($products);
    $i=0;
    foreach($products as $name=>$info){
        if ($info[1] < 5) {
            echo "Order Placed of 500 $name.<br>";
            $billAmount+= $info[0]* 500;
        }
        $i++;
        if($i == count($products)){
            echo "<br>Total Price: ".$billAmount;
        }

    }

?>