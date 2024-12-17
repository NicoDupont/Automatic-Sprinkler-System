<?php
$user='nicolas';
$pass='';
$host='192.168.1.123';
$bdd='ARROSAGE';

$servermqtt   = '192.168.1.125';
$portmqtt    = 1883;
$clientId = rand(5, 15);
$usermqtt = 'nicolas';
$passmqtt = '';
$clean_session = false;
$prefix_mqtt = 'ha';
$device_mqtt = 'arrosage';
$suffix_mqtt = '';
#$suffix_mqtt = '/cmd';

require_once('vendor/autoload.php');
use \PhpMqtt\Client\MqttClient;
use \PhpMqtt\Client\ConnectionSettings;

function ConnectMqtt($user,$pass,$server,$port){
    $connectionSettings = new ConnectionSettings();
    $connectionSettings = $connectionSettings
            ->setUsername($user)
            ->setPassword($pass);
    $mqtt = new MqttClient($server, $port, 'mqttphp');
    $mqtt->connect($connectionSettings);
    return $mqtt;

}

function DisconnectMqtt($session){
    $session->disconnect();
}

function PublishMqtt ($session,$topic,$payload,$qos,$retain){
    $session->publish($topic,$payload,$qos,$retain);

}


?>