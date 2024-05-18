from node_config import *
import simulation
import board
import digitalio 
from board import *
import pwmio
from adafruit_motor import servo

#------------Damper control-----------#
# Parallax Standard Servo (https://www.parallax.com/product/parallax-standard-servo/)
SERVO_ACTUATION_RANGE = 180  #degrees
SERVO_MIN_PULSE = 750 #us, for PWM control
SERVO_MAX_PULSE = 2250 #us, for PWM control

if node_type != NODE_TYPE_SIMULATED or node_type != NODE_TYPE_SECONDARY:
    # Damper initialization - use pins A0, A1, and A2 for zones 1, 2, and 3 respectively
    d0 = servo.Servo(pwmio.PWMOut(board.A0, duty_cycle=2 ** 15, frequency=50))
    d1 = servo.Servo(pwmio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50))
    d2 = servo.Servo(pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50))
    pass

# Set the damper for the given zone to the given percent (0 means closed, 100 means fully open)
def set_damper(zone, percent):
    if percent >= 0 or percent <= 100:
        if zone == 0:
            d0.angle = 135 - (90*(percent/100))
        elif zone == 1:
            d1.angle = 135 - (90*(percent/100))   
        else:
            d2.angle = 135 - (90*(percent/100))
    else:
        print("Error: Invalid Percent Value")
    if node_type == NODE_TYPE_SIMULATED:
        simulation.get_instance().set_damper(zone,percent)
    pass

#------------End damper control-----------#

#------------Heat/cool control-----------#
heatPin = None
coolPin = None
if node_type == NODE_TYPE_SIMULATED and 0:
    pass
elif board.board_id == 'unexpectedmaker_feathers2':
    # Initialize digital outputs for heating, cooling, and the circulation fan
    # Use pins D13 for heat, D9 and D6 for cooling, and D12 for the fan
    heatPin = digitalio.DigitalInOut(D13)
    heatPin.direction = digitalio.Direction.OUTPUT
    coolPin = digitalio.DigitalInOut(D9)
    coolPin.direction = digitalio.Direction.OUTPUT
    fanPin = digitalio.DigitalInOut(D12)
    fanPin.direction = digitalio.Direction.OUTPUT
else:
    pass

# Control the heater (turn on by passing in True, off by passing in False)
def set_heating(value):
    if node_type == NODE_TYPE_SIMULATED:
        simulation.get_instance().zones[0]['heating'] = value
        simulation.get_instance().zones[1]['heating'] = value
        simulation.get_instance().zones[2]['heating'] = value   
    heatPin.value = value
    pass

# Control the cooler (turn on by passing in True, off by passing in False)
def set_cooling(value):
    if node_type == NODE_TYPE_SIMULATED:
        simulation.get_instance().zones[0]['cooling'] = value
        simulation.get_instance().zones[1]['cooling'] = value
        simulation.get_instance().zones[2]['cooling'] = value
    coolPin.value = value
    pass

# Control the circulation fan (turn on by passing in True, off by passing in False)
def set_circulating(value):
    fanPin.value = value
    pass
#------------End heat/cool control-----------#