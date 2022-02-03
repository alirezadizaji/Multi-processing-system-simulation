from typing import Optional, List

import numpy as np

from .clock import Clock
from .entity import Entity
from ..enums.entity_stat import EntityStatus

class Core:
    """ the object giving final stage of services for entities
    
    Args:
        serv_rate (float): service rate (exponential distribution)
        max_num_entities_to_come (int): maximum number of entities to come for taking services from this core
            this indeed is identical with total number of entities coming to the system.
    """
    def __init__(self,
        serv_rate: float,
        max_num_entities_to_come: int):


        self._ts_service = np.random.exponential(scale=serv_rate, size=max_num_entities_to_come).tolist()
        """ service time pre-generated for entities """

        self.entity_in_serv: List[Entity] = list()
        """ an entity currently taking service from core (this is list to more easily keep track of entity)"""

    def set_entity_in_serv(self, entity: Entity):
        """ set a new entity for taking the service 
        
        Args:
            entity (Entity): entity for taking service
        """

        # set related attributes after an entity taking a core for being processed
        entity.t_service_in_core = self._ts_service.pop(0)
        entity.t_start_service_in_core = Clock().t

        self.entity_in_serv = [entity]


    def is_busy(self):
        """ returns whether the core is currently busy or not """
        
        return len(self.entity_in_serv) == 1  

    
    def check_entity_in_serv_done(self) -> Optional[Entity]:
        """ check whether processing of an entity of a core is done or not
        
        Returns:
            (Optional[Entity]): return an entity if its service time is passed 
        """

        if self.is_busy() and self.entity_in_serv[0].t_start_service_in_core + \
                self.entity_in_serv[0].t_service_in_core <= Clock().t:
            
            entity = self.entity_in_serv.pop()
            
            # set related attributes to when status becomes DONE
            entity.t_in_system = Clock().t - entity.t_arrival
            entity.stat = EntityStatus.DONE

            return entity
        
        else:
            return None
