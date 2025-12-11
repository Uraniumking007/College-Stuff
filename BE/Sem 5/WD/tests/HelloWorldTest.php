<?php

require_once '../html/hello.php';

class HelloWorldTest extends PHPUnit\Framework\TestCase
{
 public function testOutput()
 {
<<<<<<< HEAD
    // Capture the output of hello.php
=======
>>>>>>> f7ea692be64aab11baa01cb5e55267ad5982c00a
    ob_start();
    include '../html/hello.php';
    $output = ob_get_clean();

<<<<<<< HEAD
    // Assert that the output is "Hello, Docker!"
=======
>>>>>>> f7ea692be64aab11baa01cb5e55267ad5982c00a
    $this->assertEquals("Hello, Docker!", $output);
 }
}
?>
