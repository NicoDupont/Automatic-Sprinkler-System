<?php

	header('Content-type: application/json');
    #ini_set('display_errors', 5);
    include 'config.php';
    
    try
    {$bdd = new PDO("mysql:host=$host;dbname=$bdd;charset=utf8", $user, $pass);
     $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);}
    catch(Exception $e)
    {die('Erreur : '.$e->getMessage());}
    if (isset($_GET["sequence"]) ){
        $qry = $bdd->prepare("select * from Sequence where seq='".$_GET["sequence"]."';");  
    }else{
        $qry = $bdd->prepare("select a.*,(case when b.seq is null then 0 else 1 end) as open from Sequence as a left join (select distinct sequence as seq from Zone where open=1 and active=1) as b on a.seq=b.seq;");
    }
    $qry->execute();
    $data = $qry->fetchAll(PDO::FETCH_ASSOC);
    $jsondata = json_encode($data);
    echo $jsondata;
    
    $data = null;
    $qry = null;
    $bdd = null;

?>