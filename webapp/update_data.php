<?php
    // save data from HA by http request
    //ini_set('display_errors', 5);
    if($_POST){

        $type = $_POST['type'];
        $field = $_POST['field'];
        $sv = $_POST['sv'];
        $data = $_POST['val'];

        // generate ts for mysql timerstamp field
        $mysql_ts = date("Y-m-d H:i:s", time()); 

        include 'config.php';
        try
        {
            $bdd = new PDO("mysql:host=$host;dbname=$bdd;charset=utf8", $user, $pass);
            $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        }
        catch(Exception $e)
        {
            die('Erreur : '.$e->getMessage());
        }
        if ($type = "switch"){
            if ($data="on"){$val=1;}else{$val=0;}
            $qry = $bdd->prepare('update Zone set :field=:data where sv=:sv');
            $qry->execute(array('data' => $val,  'sv' => $sv, 'field'=> $field));  
        }
        if ($type = "value"){
            $qry = $bdd->prepare('update Zone set :field=:data where sv=:sv');
            $qry->execute(array('data' => $data,  'sv' => $sv, 'field'=> $field));  
        }
        
        $qry = null;
        $bdd = null;
      
    }
?>
