<?php

require_once '../html/hello.php';

class HelloWorldTest extends PHPUnit\Framework\TestCase
{
 public function testOutput()
 {
    ob_start();
    include '../html/hello.php';
    $output = ob_get_clean();

    $this->assertEquals("Hello, Docker!", $output);
 }
}
?>
