<?php
    $students = array("Adnan"=>"354","Bhumil"=>"28","Tejash"=>"29","Bhavesh"=>"30");
    asort($students);
    foreach($students as $name => $marks){
        if($marks == max($students)){
            echo "$name has scored a total of ".$marks." marks.<br>";
        }
    }

?>