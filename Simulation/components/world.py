import numpy as np

from ..enums import EntityType
from .environment import Environment

class World:
    """ it contains all the components within the simulation, e.g. environment (outer space), system """
    
    def __init__(self,
            environment: Environment):
        
        np.random.seed(12345)
        self._environment: Environment = environment

    def run(self):
        """ run simulation """

        entity_type_time = self._environment.schedule_entry_interval_time_into_system()

