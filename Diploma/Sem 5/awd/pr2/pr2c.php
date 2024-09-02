<?php

    $number = 154;
    $sum = 0;
    for( $i = $number; $i!=0; $i/=10 ) {
        $x = $i % 10;
        $sum += $x*$x*$x;
    }
    if($sum == $number){
        echo "$number is ArmStrong Number";
    }   else {
        echo "$number is not ArmStrong Number";
    }


?>
