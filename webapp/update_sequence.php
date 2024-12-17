<?php

  if ($_POST){
    ini_set('display_errors', 5);
    include 'config.php';
    date_default_timezone_set("Europe/Paris");
    
    $seq = $_POST['seqid'];
    $heure = $_POST['heure'];
    $minute = $_POST['minute'];
    
    if (isset($_POST['active']) && $_POST['active'] == 'yes'){ $act = 1; } else{ $act = 0; }
    
    try
      {
        $bdd = new PDO("mysql:host=$host;dbname=$bdd;charset=utf8", $user, $pass);
        $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
      }
    catch(Exception $e)
      {
         die('Erreur : '.$e->getMessage());
      }
            
    //bdd ok
    $qry = $bdd->prepare("select * from Sequence where seq='".$seq."' limit 1;");
    $qry->execute();
    $data = $qry->fetchAll(PDO::FETCH_ASSOC);
    $row = $data[0];

    //mqtt
    if ($row["active"] != $act or $row["heure"] != $heure or $row["minute"] != $minute ) {
      $mqttsession = ConnectMqtt($usermqtt,$passmqtt,$servermqtt,$portmqtt);
      
      if ($row["active"] != $act)     {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["seq"]."/active".$suffix_mqtt,$act,1,true);}
      if ($row["heure"] != $heure)      {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["seq"]."/heure".$suffix_mqtt,$heure,1,true);}
      if ($row["minute"] != $minute)     {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["seq"]."/minute".$suffix_mqtt,$minute,1,true);}
  
      DisconnectMqtt($mqttsession);
    }

    $sql = "UPDATE Sequence SET 
    heure = '".$heure."' ,
    minute = '".$minute."' ,
    active = '".$act."' 
    where seq='".$seq."';";
    $qry = $bdd->prepare(  $sql);
    $qry->execute();

    $qry = null;
    $bdd = null;
    echo "ok";
      //echo $sql;
  
}else {  //post ko
    echo "ko post";
}

?>
