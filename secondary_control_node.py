import command
from sensing import *
from actuation import *
import time
import actuation
import networking
from networking import mqtt_connect

# TODO: probably want some global variables here...
autoMode = False
heating = False
cooling = False
actuation.set_circulating(True)
#networking.mqtt_publish_message(networking.FAN_FEED[0], "True")
actuation.set_heating(heating)
actuation.set_cooling(cooling)

#networking.mqtt_connect(networking.TEMP_FEEDS,message_received)

def message_received(client, topic, message):
    global heating, cooling, autoMode
    print(f"New message on topic {topic}: {message}")

    if topic in networking.AUTOMATIC_FEED:
        if message == "true":
            autoMode = True
        if message == "false":
            autoMode = False

    if (autoMode == False) and (topic in networking.COOLING_SECONDARY_FEED):
        if message == "true":
            cooling = True
        elif message == "false":
            cooling = False
        actuation.set_cooling(cooling)

    if (autoMode == False) and (topic in networking.HEATING_SECONDARY_FEED):
        if message == "true":
            heating = True
        elif message == "false":
            heating = False
        actuation.set_heating(heating)
        #if node_type == NODE_TYPE_SIMULATED:

    if (autoMode == True) and (topic in networking.COOLING_PRIMARY_FEED):
        if message == "true":
            cooling = True
        elif message == "false":
            cooling = False
        actuation.set_cooling(cooling)

    if (autoMode == True) and (topic in networking.HEATING_PRIMARY_FEED):
        if message == "true":
            heating = True
        elif message == "false":
            heating = False
        actuation.set_heating(heating)

    if topic in networking.FAN_FEED:
        if message == "true":
            actuation.set_circulating(True)
        elif message == "false":
            actuation.set_circulating(False)
        

    
# TODO: Set up networking etc.
networking.connect_to_network()
networking.mqtt_initialize()
networking.mqtt_connect((networking.FAN_FEED + networking.AUTOMATIC_FEED + networking.HEATING_PRIMARY_FEED + networking.COOLING_PRIMARY_FEED + networking.COOLING_SECONDARY_FEED + networking.HEATING_SECONDARY_FEED),message_received)
#networking.socket_listen(socket_message_received)
# Perform regular secondary node control tasks
def loop():
    # TODO: throttle this loop? (i.e. don't run it every time)
    time.sleep(0.3)
    print("Executing secondary control node loop")

    # TODO: maybe? anything to do here?
    #if autoMode == True:
    if heating == True or cooling == True:
        actuation.set_circulating(True)
        networking.mqtt_publish_message(networking.FAN_FEED[0], "True")
    elif heating == False and cooling == False:
        actuation.set_circulating(False)
        networking.mqtt_publish_message(networking.FAN_FEED[0], "False")

    pass