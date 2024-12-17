<?php

	header('Content-type: application/json');
    ini_set('display_errors', 5);
    include 'config.php';
    
    try
    {$bdd = new PDO("mysql:host=$host;dbname=$bdd;charset=utf8", $user, $pass);
     $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);}
    catch(Exception $e)
    {die('Erreur : '.$e->getMessage());}
    
    $qry = $bdd->prepare("select * from Parameter limit 1;");
    $qry->execute();
    $data = $qry->fetchAll(PDO::FETCH_ASSOC);
    $jsondata = json_encode($data);
    echo $jsondata;
    
    $data = null;
    $qry = null;
    $bdd = null;

?>
