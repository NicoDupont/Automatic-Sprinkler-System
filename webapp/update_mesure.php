<?php
    // save data sent by an arduino/esp8266 or a python script on rpi or another device..
    // ini_set('display_errors', 5);
    if($_POST){
        date_default_timezone_set("Europe/Paris");
        include 'config.php';
        $id_sensor = $_POST['id'];
        $mesure = $_POST['data'];

        // generate ts for mysql timerstamp field
        $mysql_ts = date("Y-m-d H:i:s", time()); 

        if(isset($mesure) && isset($id_sensor)  && !empty($mesure) && !empty($id_sensor)) {
            try
            {
                $bdd = new PDO("mysql:host=$host;dbname=$bdd;charset=utf8", $user, $pass);
                $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            }
            catch(Exception $e)
            {
                die('Erreur : '.$e->getMessage());
            }
            
            // add value to mesure table
            $qry = $bdd->prepare('INSERT INTO mesure (id_sensor,  mesure) VALUES ( :id_sensor,  :mesure)');
            $qry->execute(array('id_sensor' => $id_sensor,  'mesure' => $mesure));
            
            
            // add or update value on mesure_last table
            $qry = $bdd->prepare('SELECT * FROM mesure_last WHERE id_sensor=:id_sensor');
            $qry->execute(array('id_sensor' => $id_sensor));
            //$qry->bindParam(1, $id_sensor, PDO::PARAM_INT);
            $exist = $qry->fetchColumn();
            
            if ($exist){
                $qry = $bdd->prepare('UPDATE mesure_last set mesure=:mesure, mesure_tm=:mesure_tm where id_sensor=:id_sensor ');
                $qry->execute(array('id_sensor' => $id_sensor,  'mesure' => $mesure, 'mesure_tm' => $mysql_ts));
                //echo 'case1';
            }else {
                $qry = $bdd->prepare('INSERT INTO mesure_last (id_sensor,  mesure) VALUES ( :id_sensor,  :mesure)');
                $qry->execute(array('id_sensor' => $id_sensor,  'mesure' => $mesure));
                //echo 'case2';
            } 
            $qry = null;
            $bdd = null;
            

        }
    }
?>
