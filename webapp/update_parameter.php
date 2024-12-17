<?php
ini_set('display_errors', 5);
if($_POST){
    include 'config.php';
    date_default_timezone_set("Europe/Paris");
    
    $mo = $_POST['mode'];
    $so = $_POST['source'];
    $shd = $_POST['heuredemande'];
    $mid = $_POST['minutedemande'];
    $seq = $_POST['sequencedemande'];
    $td = $_POST['testduration'];
    $minp = $_POST['minpressure'];
    $maxp = $_POST['maxpressure'];
    $dp = $_POST['deltapressure'];
    $coef = $_POST['coef'];
    $nc = $_POST['nbcuve'];
    $nblc = $_POST['nblitrecuve'];
    $mic = $_POST['seuilminicuve'];
    $mac = $_POST['seuilmaxcuve'];
    $tt = $_POST['seuilautocuve'];
    $kpiautocoef = $_POST['kpiautocoef'];
    $nbmaxsv = $_POST['nbmaxsv'];
    $nbjourprecipitation = $_POST['nbjourprecipitation'];
    $seuilprecipitation = $_POST['seuilprecipitation'];
    
    if (isset($_POST['verifnbmaxsv']) && $_POST['verifnbmaxsv'] == 'yes'){
        $vnbmaxsv = 1;
    }else{
        $vnbmaxsv = 0;
    }

    if (isset($_POST['autocoef']) && $_POST['autocoef'] == 'yes'){
        $autocoef = 1;
    }else{
        $autocoef = 0;
    }

    if (isset($_POST['overcanalpressure']) && $_POST['overcanalpressure'] == 'yes'){
        $ocp = 1;
    }else{
        $ocp = 0;
    }

    if (isset($_POST['overcitypressure']) && $_POST['overcitypressure'] == 'yes'){
        $ocip = 1;
    }else{
        $ocip = 0;
    }

    if (isset($_POST['overtankpressure']) && $_POST['overtankpressure'] == 'yes'){
        $otp = 1;
    }else{
        $otp = 0;
    }

    if (isset($_POST['activetank']) && $_POST['activetank'] == 'yes'){
        $at = 1;
    }else{
        $at = 0;
    }

    if (isset($_POST['overcapacuve']) && $_POST['overcapacuve'] == 'yes'){
        $oh = 1;
    }else{
        $oh = 0;
    }

    if (isset($_POST['pompecuve']) && $_POST['pompecuve'] == 'yes'){
        $gpcu = 1;
    }else{
        $gpcu = 0;
    }

    if (isset($_POST['pompecanal']) && $_POST['pompecanal'] == 'yes'){
        $gpca = 1;
    }else{
        $gpca = 0;
    }


    if (isset($_POST['verifseqhour']) && $_POST['verifseqhour'] == 'yes'){
        $vseqhour = 1;
    }else{
        $vseqhour = 0;
    }

    if (isset($_POST['precipitation']) && $_POST['precipitation'] == 'yes'){
        $precipitation = 1;
    }else{
        $precipitation = 0;
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
    $qry = $bdd->prepare("select * from Parameter limit 1;");
    $qry->execute();
    $data = $qry->fetchAll(PDO::FETCH_ASSOC);
    $row = $data[0];

    if ($row["mode"] != $mo or 
        $row["source"] != $so or 
        $row["heure_demande"] != $shd or 
        $row["minute_demande"] != $mid or 
        $row["sequence_demande"] != $seq or 
        $row["duree_test"] != $td or 
        $row["coef"] != $coef or 
        $row["pression_seuil_bas"] != $minp or 
        $row["pression_seuil_haut"] != $maxp or
        $row["delta_pression_filtre_max"] != $dp or
        $row["test_pression_cuve"] != $otp or
        $row["test_pression_canal"] != $ocp or
        $row["test_pression_ville"] != $ocip or
        $row["nb_cuve_ibc"] != $nc or
        $row["nb_litre_cuve_ibc"] != $nblc or
        $row["seuil_min_capacite_cuve"] != $mic or
        $row["seuil_max_capacite_cuve"] != $mac or
        $row["seuil_capacite_remplissage_auto_cuve"] != $tt or
        $row["gestion_cuve"] != $at or
        $row["test_hauteur_eau_cuve"] != $oh or
        $row["gestion_pompe_cuve"] != $gpcu or
        $row["gestion_pompe_canal"] != $gpca or
        $row["kpi_auto_coef"] != $kpiautocoef or
        $row["auto_coef"] != $autocoef or
        $row["nb_max_sv"] != $nbmaxsv or
        $row["verif_nb_max_sv"] != $vnbmaxsv or
        $row["precipitation"] != $precipitation or
        $row["seuil_precipitation"] != $seuilprecipitation or
        $row["nb_jour_precipitation"] != $nbjourprecipitation or
        $row["verif_seq_hour"] != $vseqhour) {
            
        $mqttsession = ConnectMqtt($usermqtt,$passmqtt,$servermqtt,$portmqtt);
        
        if ($row["mode"] != $mo)                        {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/mode'.$suffix_mqtt,$mo,1,true);}
        if ($row["source"] != $so)                      {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/source'.$suffix_mqtt,$so,1,true);}
        if ($row["heure_demande"] != $shd)              {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/heure_demande'.$suffix_mqtt,$shd,1,true);}
        if ($row["minute_demande"] != $mid)             {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/minute_demande'.$suffix_mqtt,$mid,1,true);}
        if ($row["sequence_demande"] != $seq)           {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/sequence_demande'.$suffix_mqtt,$seq,1,true);}
        if ($row["duree_test"] != $td)                  {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/duree_test'.$suffix_mqtt,$td,1,true);}
        if ($row["coef"] != $coef)                      {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/coef'.$suffix_mqtt,$coef,1,true);}
        if ($row["pression_seuil_bas"] != $minp)        {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/pression_seuil_bas'.$suffix_mqtt,$minp,1,true);}
        if ($row["pression_seuil_haut"] != $maxp)       {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/pression_seuil_haut'.$suffix_mqtt,$maxp,1,true);}
        if ($row["delta_pression_filtre_max"] != $dp)   {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/delta_pression_filtre_max'.$suffix_mqtt,$dp,1,true);}
        if ($row["test_pression_cuve"] != $otp)         {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/test_pression_cuve'.$suffix_mqtt,$otp,1,true);}
        if ($row["test_pression_canal"] != $ocp)        {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/test_pression_canal'.$suffix_mqtt,$ocp,1,true);}
        if ($row["test_pression_ville"] != $ocip)       {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/test_pression_ville'.$suffix_mqtt,$ocip,1,true);}
        if ($row["nb_cuve_ibc"] != $nc)                 {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/nb_cuve_ibc'.$suffix_mqtt,$nc,1,true);}
        if ($row["nb_litre_cuve_ibc"] != $nblc)         {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/nb_litre_cuve_ibc'.$suffix_mqtt,$nblc,1,true);}
        if ($row["seuil_min_capacite_cuve"] != $mic)    {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/seuil_min_capacite_cuve'.$suffix_mqtt,$mic,1,true);}
        if ($row["seuil_max_capacite_cuve"] != $mac)                {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/seuil_max_capacite_cuve'.$suffix_mqtt,$mac,1,true);}
        if ($row["seuil_capacite_remplissage_auto_cuve"] != $tt)    {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/seuil_capacite_remplissage_auto_cuve'.$suffix_mqtt,$tt,1,true);}
        if ($row["gestion_cuve"] != $at)                {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/gestion_cuve'.$suffix_mqtt,$at,1,true);}
        if ($row["gestion_pompe_cuve"] != $gpcu)        {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/gestion_pompe_cuve'.$suffix_mqtt,$gpcu,1,true);}
        if ($row["gestion_pompe_canal"] != $gpca)       {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/gestion_pompe_canal'.$suffix_mqtt,$gpca,1,true);}
        if ($row["test_hauteur_eau_cuve"] != $oh)       {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/test_hauteur_eau_cuve'.$suffix_mqtt,$oh,1,true);}
        if ($row["auto_coef"] != $autocoef)             {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/auto_coef'.$suffix_mqtt,$autocoef,1,true);}
        if ($row["kpi_auto_coef"] != $kpiautocoef)      {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/kpi_auto_coef'.$suffix_mqtt,$kpiautocoef,1,true);}
        if ($row["nb_max_sv"] != $nbmaxsv)                    {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/nb_max_sv'.$suffix_mqtt,$nbmaxsv,1,true);}
        if ($row["verif_nb_max_sv"] != $vnbmaxsv)      {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/verif_nb_max_sv'.$suffix_mqtt,$vnbmaxsv,1,true);}
        if ($row["verif_seq_hour"] != $vseqhour)      {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/verif_seq_hour'.$suffix_mqtt,$vseqhour,1,true);}
        if ($row["precipitation"] != $precipitation)      {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/precipitation'.$suffix_mqtt,$precipitation,1,true);}
        if ($row["seuil_precipitation"] != $seuilprecipitation)      {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/seuil_precipitation'.$suffix_mqtt,$seuilprecipitation,1,true);}
        if ($row["nb_jour_precipitation"] != $nbjourprecipitation)   {PublishMqtt ($mqttsession,$prefix_mqtt.'/'.$device_mqtt.'/parametre/nb_jour_precipitation'.$suffix_mqtt,$nbjourprecipitation,1,true);}

        DisconnectMqtt($mqttsession);
            
    }

    $qry = $bdd->prepare("UPDATE Parameter set    duree_test =:duree_test
                                                , coef =:coef
                                                , pression_seuil_bas=:pression_seuil_bas
                                                , pression_seuil_haut=:pression_seuil_haut
                                                , delta_pression_filtre_max=:delta_pression_filtre_max
                                                , test_pression_cuve=:test_pression_cuve
                                                , test_pression_canal=:test_pression_canal
                                                , heure_demande=:heure_demande
                                                , sequence_demande=:sequence_demande
                                                , minute_demande=:minute_demande
                                                , mode =:mode
                                                , source =:source
                                                , test_pression_ville =:test_pression_ville
                                                , nb_cuve_ibc =:nb_cuve_ibc
                                                , nb_litre_cuve_ibc =:nb_litre_cuve_ibc
                                                , seuil_min_capacite_cuve =:seuil_min_capacite_cuve
                                                , seuil_max_capacite_cuve =:seuil_max_capacite_cuve
                                                , seuil_capacite_remplissage_auto_cuve =:seuil_capacite_remplissage_auto_cuve
                                                , gestion_cuve =:gestion_cuve
                                                , test_hauteur_eau_cuve =:test_hauteur_eau_cuve
                                                , gestion_pompe_cuve =:gestion_pompe_cuve
                                                , gestion_pompe_canal =:gestion_pompe_canal
                                                , auto_coef =:auto_coef
                                                , kpi_auto_coef =:kpi_auto_coef
                                                , nb_max_sv =:nb_max_sv
                                                , verif_nb_max_sv =:verif_nb_max_sv 
                                                , precipitation =:precipitation
                                                , verif_seq_hour =:verif_seq_hour
                                                , seuil_precipitation =:seuil_precipitation
                                                , nb_jour_precipitation =:nb_jour_precipitation");

    $qry->execute(array(  'duree_test' => $td
                        , 'coef' => $coef
                        , 'pression_seuil_bas' => $minp
                        , 'pression_seuil_haut' => $maxp
                        , 'delta_pression_filtre_max' => $dp
                        , 'test_pression_cuve' => $otp
                        , 'test_pression_canal' => $ocp
                        , 'heure_demande' => $shd
                        , 'minute_demande' => $mid
                        , 'sequence_demande' => $seq
                        , 'mode' => $mo
                        , 'source' => $so
                        , 'test_pression_ville' => $ocip
                        , 'nb_cuve_ibc' => $nc
                        , 'nb_litre_cuve_ibc' => $nblc
                        , 'seuil_min_capacite_cuve' => $mic
                        , 'seuil_max_capacite_cuve' => $mac
                        , 'seuil_capacite_remplissage_auto_cuve' => $tt
                        , 'gestion_cuve' => $at
                        , 'test_hauteur_eau_cuve' => $oh
                        , 'gestion_pompe_cuve' => $gpcu
                        , 'gestion_pompe_canal' => $gpca
                        , 'auto_coef' => $autocoef
                        , 'kpi_auto_coef' => $kpiautocoef
                        , 'nb_max_sv' => $nbmaxsv
                        , 'verif_nb_max_sv' => $vnbmaxsv
                        , 'precipitation' => $precipitation
                        , 'verif_seq_hour' =>$vseqhour
                        , 'seuil_precipitation' => $seuilprecipitation
                        , 'nb_jour_precipitation' => $nbjourprecipitation));

    $qry = null;
    $bdd = null;
    echo "ok";
      
} else { 
     //post ko
    echo "ko post";
}

?>
