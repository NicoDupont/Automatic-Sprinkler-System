<?php
ini_set('display_errors', 5);
    require_once('vendor/autoload.php');

    use \PhpMqtt\Client\MqttClient;
    use \PhpMqtt\Client\ConnectionSettings;

    include 'config.php';


    $connectionSettings = new ConnectionSettings();
    $connectionSettings = $connectionSettings
        ->setUsername($usermqtt)
        ->setPassword($passmqtt);
    $mqtt = new MqttClient($servermqtt, $portmqtt, 'test-publisher');
    $mqtt->connect($connectionSettings);
    $mqtt->publish('ha/arrosage/parametre/mode','Stop',1,true);
    $mqtt->disconnect();
    echo "ok";

?>    