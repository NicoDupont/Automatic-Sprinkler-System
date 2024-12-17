<?php
	header('Content-type: application/json');
    ini_set('display_errors', 5);
    include 'config.php';
    try
    {$bdd = new PDO("mysql:host=$host;dbname=$bdd;charset=utf8", $user, $pass);
     $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);}
    catch(Exception $e)
    {die('Erreur : '.$e->getMessage());}

    #$qry = $bdd->prepare("select concat(DATE_FORMAT(eventdate, '%d-%m %H:%i'),' - ',val1,' - ',val3,' - ',left(val4,15)) as zone,val4,val5 as type from Event order by eventdate desc limit 30;");
    if (isset($_GET["type"]) ){
        if ($_GET["type"]=="sv"){
            $sql = "select DATE_FORMAT(eventdate, '%d-%m %H:%i') as dateeve,val1,val2,val3,val4,val5 from Event where val5 = 'sv' order by eventdate desc limit 30;";
        }else{
            $sql = "select DATE_FORMAT(eventdate, '%d-%m %H:%i') as dateeve,val1,val2,val3,val4,val5 from Event where val5 != 'sv' order by eventdate desc limit 20;";
        }
        $qry = $bdd->prepare($sql);
        $qry->execute();
        $data = $qry->fetchAll(PDO::FETCH_ASSOC);
        $jsondata = json_encode($data);
        echo $jsondata;
    }
    $data = null;
    $qry = null;
    $bdd = null;
?>