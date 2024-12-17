<?php
	header('Content-type: application/json');
    #ini_set('display_errors', 5);
    include 'config.php';
    try
    {$bdd = new PDO("mysql:host=$host;dbname=$bdd;charset=utf8", $user, $pass);
     $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);}
    catch(Exception $e)
    {die('Erreur : '.$e->getMessage());}
   
    #$qry = $bdd->prepare("SELECT concat(sequence,' ',sv,' ',DATE_FORMAT(StartingDate, '%d-%m %H:%i'),' => ',DATE_FORMAT(EndDate, '%H:%i'),' ',name) as seq FROM SequenceZone order by 'order',sv;");
    $qry = $bdd->prepare("SELECT concat(a.sequence,' ',a.sv,' ',DATE_FORMAT(a.StartingDate, '%d-%m %H:%i'),' => ',DATE_FORMAT(a.EndDate, '%H:%i')) as seq, b.open, (case WHEN now() BETWEEN a.StartingDate and a.EndDate then TIMESTAMPDIFF(MINUTE,now(),a.EndDate) else (case WHEN now()>a.EndDate then 0 else TIMESTAMPDIFF(MINUTE,a.StartingDate,a.EndDate) end) end) as reste,a.planned FROM SequenceZone as a left join Zone as b on a.sv=b.sv order by a.`order`,a.sv;");
    $qry->execute();
    $data = $qry->fetchAll(PDO::FETCH_ASSOC);
    $jsondata = json_encode($data);
    echo $jsondata;
    
    $data = null;
    $qry = null;
    $bdd = null;
?>