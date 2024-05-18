from node_config import *
import networking
import time
from sensing import *
import adafruit_dotstar
import board, analogio, digitalio

# Set up networking.
networking.connect_to_network()
networking.mqtt_initialize()
networking.mqtt_connect()

# The previously reported temperature values.
prev_temps = [None] * num_zones

# Timing variables.
LOOP_INTERVAL_NS = 1000000000
_prev_time = time.monotonic_ns()

# Init LDO2 Pin
ldo2 = digitalio.DigitalInOut(board.LDO2)
ldo2.direction = digitalio.Direction.OUTPUT

def enable_LDO2(state):
    # If Temp measurement nodes don't work try to comment this out
    """Set the power for the second on-board LDO to allow no current draw when not needed."""
    ldo2.value = state
    # A small delay to let the IO change state
    time.sleep(0.035)

enable_LDO2(True)

# Runs periodic node tasks.
def loop():
    # Only run this code if LOOP_INTERVAL_NS have elapsed.
    global _prev_time
    curr_time = time.monotonic_ns()
    if curr_time - _prev_time < LOOP_INTERVAL_NS:
        return

    _prev_time = curr_time


    # Make a list of zones that we're reporting temperature for. This allows us to report all
    # zones for a simulated node.
    zones = [zone_id]
    if node_type == NODE_TYPE_SIMULATED:
        zones = [i for i in range(num_zones)]

    for zone in zones:
        
        current_temp = get_current_temperature_f(zone)

        print(f'Zone {zone} temp: {current_temp}')

        # TODO: do we need to report the temperature EVERY time? Report only if the new reading is
        # significantly different from the old one!
        networking.mqtt_publish_message(networking.TEMP_FEEDS[zone], round(current_temp,2))