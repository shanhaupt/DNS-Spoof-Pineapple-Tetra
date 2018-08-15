<?php
$ref = $_SERVER['HTTP_HOST'];
if ($ref == "www.school.com")   { header('Location: school.html'); }
if ($ref == "www.pornhub.com")  { header('Location: pornhub.html'); }
require('peets.html');
?>
