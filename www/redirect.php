<?php
$ref = $_SERVER['HTTP_HOST'];
if ($ref == "www.school.com")   { header('Location: school.html'); }
require('peets.html');
?>
