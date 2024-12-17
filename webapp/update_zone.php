<?php
  //ini_set('display_errors', 5);
  if($_POST){

    include 'config.php';
    date_default_timezone_set("Europe/Paris");
    
    $idsv = $_POST['idsv'];
    $typesv = $_POST['typesv'];
    $code = $_POST['code'];
    $nom = $_POST['nom'];
    $order = $_POST['numero'];
    $gpio = $_POST['gpio'];
    $seq = $_POST['sequence'];
    $dur = $_POST['duree'];
    $coef = $_POST['coef'];
    
    if (isset($_POST['active']) && $_POST['active'] == 'yes'){ $act = 1; } else{ $act = 0; }
    if (isset($_POST['open']) && $_POST['open'] == 'yes'){ $opn = 1; } else{ $opn = 0; }
    if (isset($_POST['lundi']) && $_POST['lundi'] == 'yes'){ $mon = 1;} else{ $mon = 0; }
    if (isset($_POST['mardi']) && $_POST['mardi'] == 'yes'){ $tue = 1;} else{ $tue = 0; }
    if (isset($_POST['mercredi']) && $_POST['mercredi'] == 'yes'){ $wed = 1;} else{ $wed = 0; }
    if (isset($_POST['jeudi']) && $_POST['jeudi'] == 'yes'){ $thu = 1;} else{ $thu = 0; }
    if (isset($_POST['vendredi']) && $_POST['vendredi'] == 'yes'){ $fri = 1;} else{ $fri = 0; }
    if (isset($_POST['samedi']) && $_POST['samedi'] == 'yes'){ $sat = 1;} else{ $sat = 0; }
    if (isset($_POST['dimanche']) && $_POST['dimanche'] == 'yes'){ $sun = 1;} else{ $sun = 0; }
    if (isset($_POST['touslesjours']) && $_POST['touslesjours'] == 'yes'){ $tlj = 1;} else{ $tlj = 0; }
    if (isset($_POST['even']) && $_POST['even'] == 'yes'){ $even = 1;} else{ $even = 0; }
    if (isset($_POST['odd']) && $_POST['odd'] == 'yes'){ $odd = 1;} else{ $odd = 0; }
    
    if ($even == 1 || $odd == 1){
      $mon = 0;
      $tue = 0;
      $wed = 0;
      $thu = 0;
      $fri = 0;
      $sun = 0;
      $sat = 0;
    }

    if ($even == 0 && $odd == 0 && $tlj == 1){
      $mon = 1;
      $tue = 1;
      $wed = 1;
      $thu = 1;
      $fri = 1;
      $sun = 1;
      $sat = 1;
    }

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
    $qry = $bdd->prepare("select sv,open,active,duration,sequence,`order`,gpio,even,odd,coef from Zone where id_sv='".$idsv."' limit 1;");
    $qry->execute();
    $data = $qry->fetchAll(PDO::FETCH_ASSOC);
    $row = $data[0];

    //mqtt
    if ($row["open"] != $opn or $row["duration"] != $dur or $row["active"] != $act or $row["sequence"] != $seq 
        or $row["order" ] != $act or $row["gpio"] != $gpio or $row["even"] != $even  or $row["coef"] != $coef) {
      
      $mqttsession = ConnectMqtt($usermqtt,$passmqtt,$servermqtt,$portmqtt);

      if ($row["open"] != $opn)     {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["sv"]."/etat".$suffix_mqtt,$opn,1,true);}
      if ($row["active"] != $act)   {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["sv"]."/active".$suffix_mqtt,$act,1,true);}
      if ($row["duration"] != $dur) {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["sv"]."/duree".$suffix_mqtt,$dur,1,true);}
      if ($row["sequence"] != $seq) {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["sv"]."/sequence".$suffix_mqtt,$seq,1,true);}
      if ($row["order"] != $order)  {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["sv"]."/ordre".$suffix_mqtt,$order,1,true);}
      if ($row["gpio"] != $gpio)    {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["sv"]."/gpio".$suffix_mqtt,$gpio,1,true);}
      if ($row["even"] != $even)    {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["sv"]."/even".$suffix_mqtt,$even,1,true);}
      if ($row["odd"] != $odd)      {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["sv"]."/odd".$suffix_mqtt,$odd,1,true);}
      if ($row["coef"] != $coef)    {PublishMqtt ($mqttsession,$prefix_mqtt."/".$device_mqtt."/".$row["sv"]."/coef".$suffix_mqtt,$coef,1,true);}
      
      DisconnectMqtt($mqttsession);
    }

    // update parameters for single zone
    $sql = "UPDATE Zone SET `order` = '".$order."' , duration = '".$dur."', sv = '".$code."' , name = '".$nom."' 
          , sequence = '".$seq."' , gpio = '".$gpio."' , active = '".$act."' , open = '".$opn."' , even = '".$even."' 
          , odd = '".$odd."' , coef = '".$coef."', monday='".$mon."', tuesday='".$tue."', wednesday='".$wed."'
          , thursday='".$thu."', friday='".$fri."', saturday='".$sat."', sunday='".$sun."' where id_sv='".$idsv."';";
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
