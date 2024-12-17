
import yaml
import secret as secret

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

LOG_LEVEL_STREAM = config['p_log_level_stream']   # log level to be write like print  NOTSET | DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_LEVEL_FILE = config['p_log_level_file']       # log level to be write in log file  NOTSET | DEBUG | INFO | WARNING | ERROR | CRITICAL
#settings for OpenWeatherMap API
API_KEY = secret.p_api_key_openweatermap
LATITUDE = secret.p_latitude
LONGITUDE = secret.p_longitude

IP_BDD_SERVER = config['p_ip_bdd']
USER_BDD = config['p_user_bdd']
PASSWORD_BDD = secret.p_password_bdd
LOG_DATABASE = config['p_log_bdd']
NAME_DATABASE = config['p_database']

IP_MQTT_BROKER = config['p_ip_mqtt']
USER_MQTT = config['p_user_mqtt']
PASSWORD_MQTT = secret.p_password_mqtt
PORT_MQTT = config['p_port_mqtt']
FILE_TOPIC_MQTT = config['p_topics_mqtt']
PREFIX_MQTT= config['P_prefix_mqtt']    
DEVICE_MQTT= config['p_device_mqtt']    
#SUFFIX_CMD_MQTT = config['p_suffix_cmd_mqtt']   #for 2025
#SUFFIX_STA_MQTT = config['p_suffix_sta_mqtt']   #for 2025

GLOBAL_SETTINGS_FILE =  config['p_gp_file']      # global parameters for irrigation
SEQUENCE_FILE =  config['p_sequence_file']       # calculated sequence for watering
ZONE_SEQUENCE_FILE =  config['p_zone_file']       # calculated sequence for watering
ZONE_PARAMETER_FILE = config['p_zp_file']         # configuration of the solenoid valves (=zone) for watering
GLOBAL_PARAMETER_FILE = config['p_gp_file']      # global parameters for irrigation
ACTIVE_ZONE_FILE = config['p_az_file']            # file of the active zone for lcd
MQTT_BDD_AUTODISCOVERY_FILE = config['p_mqtt_bdd_autodiscovery_file']
PUBLISH_MQTT = config['p_mqtt']

RPI_NUMBER =  config['p_rpi']                     # if I need more than one rpi to manage all solenoid valves
IP_WEB_SERVER =  config['p_ip_web']               # ip of local web server                
IP_MQTT_SERVER =  config['p_ip_mqtt']             # ip of local mqtt server    
IP_HA_SERVER =  config['p_ip_ha']                  # ip of local ha instance   
IP_WEB =  config['p_ip_www']                  # ip for test internet         
DELAY_TIME_SEQUENCE = config['p_delay_sequence']  # time in minutes between two sequences
MIN_TIME_SEQUENCE = config['p_min_runtime']       # minimum run time for watering
MAX_TIME_SEQUENCE = config['p_max_runtime']       # maximum run time for watering
SLEEP_TIME_LOOP = config['p_sleep_loop']          # time in seconds between two main loops
RUN_WATERING= config['p_watering']             # watering management yes or no
DETECT_ANOMALY = config['p_anomaly']    # take care of any anomalies
ACTIVE_LCD = config['p_lcd_screen']               # use or not the lcd
PROJECT_NAME = config['p_name']                   # name of the project
PROJECT_VERSION = config['p_version']             # version number of the project
PROJECT_DATE_VERSION = config['p_date_version']   # date version of the project
WAIT_TIME_LCD = config['p_lcd_sleep_time']        # time in seconds to keep display

MIN_TEMP = config['p_min_coef_temp']
MAX_TEMP = config['p_max_coef_temp']
MIN_COEF = config['p_min_coef']
MAX_COEF = config['p_max_coef']

MAX_ERROR = 20

#---------------------------------------
#initialise gpio => recupération depuis fichier de config ?
#list_gpio = [4,17,27,22,10,9,11,5,6,13,19,26,21,20,16,12,7,8,25,24,23,18]
list_gpio = config['p_gpio']