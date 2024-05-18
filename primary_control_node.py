from actuation import *
import time
import actuation
import networking
from networking import mqtt_connect

# TODO: probably want some global variables here...
setPoints = [79,77,60]
currTemp = [70,85,70]
prevTime = 0
damperPercent = [50,50,50]
autoMode = True # 0 = manual , 1 = Automatic
heating = False
cooling = False
# actuation.set_heating(heating)
# actuation.set_cooling(cooling)




# mqtt_connect(feeds=[networking.TEMP_FEEDS,networking.COOLING_FEED,networking.HEATING_FEED,networking.SETPOINT_FEEDS,networking.DAMPER_FEEDS])

# Called when an MQTT message is received.
# topic is the feed name the message was published on.
# message is the contents of the message.
def message_received(client, topic, message):
    global heating, cooling, autoMode, setPoints
    print(f"New message on topic {topic}: {message}")
    
    if topic in networking.SETPOINT_FEEDS:
        if topic == networking.SETPOINT_FEEDS[0]:
            setPoints[0] = float(message)
        if topic == networking.SETPOINT_FEEDS[1]:
            setPoints[1] = float(message)
        if topic == networking.SETPOINT_FEEDS[2]:
            setPoints[2] = float(message)

    if topic in networking.DAMPER_FEEDS:
        if topic == networking.DAMPER_FEEDS[0]:
            actuation.set_damper(0, float(message))
        if topic == networking.DAMPER_FEEDS[1]:
            actuation.set_damper(1, float(message))
        if topic == networking.DAMPER_FEEDS[2]:
            actuation.set_damper(2, float(message))

    if topic in networking.TEMP_FEEDS:
        if topic == networking.TEMP_FEEDS[0]:
            currTemp[0] = float(message)
        if topic == networking.TEMP_FEEDS[1]:
            currTemp[1] = float(message)
        if topic == networking.TEMP_FEEDS[2]:
            currTemp[2] = float(message)

    if topic in networking.AUTOMATIC_FEED:
        if message == "true":   
            autoMode = True
        if message == "false":
            autoMode = False

    if (topic in networking.COOLING_SECONDARY_FEED):
        if message == "true":
            cooling = True
        elif message == "false":
            cooling = False
        actuation.set_cooling(cooling)

    if (topic in networking.HEATING_SECONDARY_FEED):
        if message == "true":
            heating = True
        elif message == "false":
            heating = False
        actuation.set_heating(heating)
        #if node_type == NODE_TYPE_SIMULATED:

    if (topic in networking.COOLING_PRIMARY_FEED):
        if message == "true":
            cooling = True
        elif message == "false":
            cooling = False
        actuation.set_cooling(cooling)

    if (topic in networking.HEATING_PRIMARY_FEED):
        if message == "true":
            heating = True
        elif message == "false":
            heating = False
        actuation.set_heating(heating)


networking.connect_to_network()
networking.mqtt_initialize()
networking.mqtt_connect((networking.TEMP_FEEDS + networking.SETPOINT_FEEDS + networking.DAMPER_FEEDS + networking.AUTOMATIC_FEED + networking.COOLING_SECONDARY_FEED + networking.HEATING_SECONDARY_FEED + networking.COOLING_PRIMARY_FEED + networking.HEATING_PRIMARY_FEED),message_received)

# Send initial values to MQTT
for zone in range(num_zones):
    networking.mqtt_publish_message(networking.SETPOINT_FEEDS[zone], str(setPoints[zone]))
    networking.mqtt_publish_message(networking.DAMPER_FEEDS[zone], str(damperPercent[zone]))
if node_type != NODE_TYPE_SIMULATED:
    networking.mqtt_publish_message(networking.AUTOMATIC_FEED[0], "true")
networking.mqtt_publish_message(networking.HEATING_PRIMARY_FEED[0], str(heating))
networking.mqtt_publish_message(networking.COOLING_PRIMARY_FEED[0], str(cooling))

# Run the regular primary control node tasks
def loop():
    # TODO: throttle this loop? (i.e. don't run it every time)
    global heating, cooling, autoMode, damperPercent, setPoints
    currTime = time.monotonic_ns()
    global prevTime
    print("Executing primary control node loop")

    # Main temperature control logic
    if autoMode == True:
        for zone in range(num_zones):
            
            if (currTime - prevTime)/1000000000 >= 20:
                if (sum(currTemp) - sum(setPoints)) / len(currTemp) > 0:
                    heating = False
                    cooling = True
                elif (sum(currTemp) - sum(setPoints)) / len(currTemp) < 0:
                    heating = True
                    cooling = False
                elif (currTemp[0] - setPoints[0]) and (currTemp[1] - setPoints[1]) and (currTemp[2] - setPoints[2]) == 0:
                    heating = False
                    cooling = False
                prevTime = currTime

            if (currTime - prevTime)/1000000000 >= 3:
                if heating and currTemp[zone] >= setPoints[zone]:
                    actuation.set_damper(zone, 0)
                    damperPercent[zone] = 0
                elif cooling and currTemp[zone] <= setPoints[zone]:
                    actuation.set_damper(zone, 0)
                    damperPercent[zone] = 0
                elif heating and (currTemp[zone] < setPoints[zone]):
                    actuation.set_damper(zone, min(100,((abs(currTemp[zone]-setPoints[zone]))*10)))
                    damperPercent[zone] = min(100,((abs(currTemp[zone]-setPoints[zone]))*10))
                elif cooling and (currTemp[zone] > setPoints[zone]):
                    actuation.set_damper(zone, min(100,((abs(currTemp[zone]-setPoints[zone]))*10)))
                    damperPercent[zone] = min(100,((abs(currTemp[zone]-setPoints[zone]))*10))
                networking.mqtt_publish_message(networking.DAMPER_FEEDS[zone], str(damperPercent[zone]))  

        # Update values in MQTT
        networking.mqtt_publish_message(networking.HEATING_PRIMARY_FEED[0], str(heating))
        networking.mqtt_publish_message(networking.COOLING_PRIMARY_FEED[0], str(cooling))
        actuation.set_heating(heating)
        actuation.set_cooling(cooling)



    elif autoMode == False:
        # input(" enter input ")
        pass
