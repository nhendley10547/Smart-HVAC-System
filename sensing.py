from node_config import *

# Only import hardware modules if we're not simulating
if node_type != NODE_TYPE_SIMULATED:
    import analogio
    import board
    from board import *
import simulation

#---------LM35 code----------#
ADC_MAX_VOLTAGE = 5.0 # Voltage range for the ADC input
ADC_MAX_VALUE = 65535 # Max value coming off the ADC
LM35_MV_PER_C = 10.0  # millivolts per degrees Celsius

# LM35 temperature sensor initialization
# TODO: pin configuration
if node_type == NODE_TYPE_SIMULATED:
    pass
elif board.board_id == 'unexpectedmaker_feathers2':
    # Initialize LM35 input on pin A3
    _lm35_pin = analogio.AnalogIn(A3)
    pass
else:
    pass

# Get a temperature reading from the LM35
def lm35_temperature_c():
    # TODO: read from lm35 and return value in degrees 
    a3tempC = ((_lm35_pin.value * 2.57) / 51000) / 0.001
    return 0
#---------End LM35 code----------#

#---------FunHouse code----------#
# FunHouse initialization
if node_type == NODE_TYPE_SIMULATED:
    _lm35_pin = None
elif board.board_id == 'adafruit_funhouse':
    _lm35_pin = analogio.AnalogIn(board.A0)
else:
    _lm35_pin = None

# Get a temperature reading from the FunHouse internal temperature sensor
def funhouse_temperature_c():
    return lm35_temperature_c()
#---------End FunHouse code----------#

# Convert Celsius to Fahrenheit
def c_to_f(value):
    # TODO: implement
    return 0

# Get a temperature reading using whatever sensor is configured. zone is the zone ID of 
# the zone we're getting the reading for (used when simulating)
def get_current_temperature_f(zone=0):
    if node_type == NODE_TYPE_SIMULATED:
        sim = simulation.get_instance()
        return sim.get_temperature_f(zone)

    if board.board_id == 'unexpectedmaker_feathers2':
        return c_to_f(lm35_temperature_c())

    if board.board_id == 'adafruit_funhouse':
        return c_to_f(funhouse_temperature_c())