<?php
require_once 'auth_config.php';

logoutUser();

header("Location: login.php?logout=1");
exit();
?>
