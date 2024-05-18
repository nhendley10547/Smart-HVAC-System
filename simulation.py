from node_config import num_zones
import time
import math
import actuation

# TODO: define some values?
ambientTemp = 50

# The Simulation(R)
_sim = None

# We only want ONE Simulation object, and we want to share it between all of the modules. We can accomplish this
# using the singleton design pattern. This function is a key part of that pattern. It returns the singleton instance.
# Call "simulation.get_instance()" to get a Simulation, instead of instantiating a Simulation directly.
def get_instance():
    global _sim
    if _sim is None:
        _sim = Simulation(num_zones)
    return _sim

# A class that simulates the physical environment for the system.
class Simulation:
    # Initializes the simulation.
    def __init__(self, num_zones):
       self.prevTime = time.monotonic_ns()
       self.zones = [
           {
               'temp': 70.0,
               'damper': 50,
               'heating': False,
               'cooling': False,
           },
            {
               'temp': 85.0,
               'damper': 50,
               'heating': False,
               'cooling': False,
           },
           {
               'temp': 70.0,
               'damper': 50,
               'heating': False,
               'cooling': False,
           }
       ]

    # Returns the current temperature in the zone specified by zone_id
    def get_temperature_f(self, zone_id):
        return self.zones[zone_id]['temp']

    # Sets the damper(s) for the zone specified by zone_id to the percentage
    # specified by percent. 0 is closed, 1 is fully open.
    def set_damper(self, zone_id, percent):
        self.zones[zone_id]['damper'] = percent
        return


    # Update the temperatures of the zones, given that elapsed_time_ms milliseconds
    # have elapsed since this was previously called.
    def _update_temps(self, elapsed_time_ms):
        for zone in range(num_zones):
            self.zones[zone]['temp'] =  self.zones[zone]['temp'] - ((math.sqrt(abs(self.zones[zone]['temp']-ambientTemp))/100)*(elapsed_time_ms/1000))

            if self.zones[zone]['heating']:
                self.zones[zone]['temp'] = self.zones[zone]['temp'] + ((self.zones[zone]['damper']/100)*elapsed_time_ms/1000)
            elif self.zones[zone]['cooling']:
                self.zones[zone]['temp'] =  self.zones[zone]['temp'] - ((self.zones[zone]['damper']/100)*elapsed_time_ms/1000)

    
    # Runs periodic simulation actions.
    def loop(self):
        currTime = time.monotonic_ns()
        elapsed_time_ms = (currTime-self.prevTime)/1000000
        self.prevTime = currTime
        
        self._update_temps(elapsed_time_ms)
        

# Used for testing the simulation.
if __name__ == '__main__':
    sim = get_instance()
    

    while True:
        sim.loop()
        time.sleep(1)

        for zone in range(num_zones):
            temp = sim.get_temperature_f(zone)
            print(f'Zone {zone} temp: {temp}')
            

        # TODO: add additional testing code, e.g. what happens if you turn on heating/cooling?
        
        