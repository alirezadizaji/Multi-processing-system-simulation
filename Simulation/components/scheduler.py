from typing import List

import numpy as np

from .clock import Clock
from .queue import Queue
from .entity import Entity
from ..enums.entity_stat import EntityStatus

class Scheduler:
    """ time scheduler whose main purpose is to assign an entity into a server within the system
    
    Args:
        serv_rate (float): service rate (poi)
        num_entities_to_come (int): number of entities to come into the scheduler
    """

    def __init__(self, 
            serv_rate: float,
            num_entities_to_come: int):

        self.queue: Queue = Queue()
        """ queue of scheduler """

        self.entity_in_serv: List[Entity] = list()
        """ entity currently taking service from scheduler """

        self._ts_service = np.random.exponential(1.0 / serv_rate, size=num_entities_to_come).tolist()
        """ time service being pre-generated for entities """

    def _is_busy(self):
        """ returns whether scheduler is busy or not """

        return len(self.entity_in_serv) == 1

    def enter(self, entity: Entity):
        """ enters an entity into the scheduler; at first indeed it directly enters into the queue """

        self.queue.add(entity)
        
    def set_entity_in_serv(self):
        """ set an entity for taking the service """

        if not self.queue.is_empty() and not self._is_busy():
            entity = self.queue.pop()

            # set attributes related to starting a service from scheduler
            entity.t_start_service_in_scheduler = Clock().t
            entity.t_service_in_scheduler = self._ts_service.pop(0)

            self.entity_in_serv = [entity]
    
    def check_entity_in_serv_done(self):
        """ check whether processing of an entity of a core is done or not
        
        Returns:
            (Optional[Entity]): return an entity if its service time is passed 
        """

        if self._is_busy() and self.entity_in_serv[0].t_start_service_in_scheduler + \
                self.entity_in_serv[0].t_service_in_scheduler <= Clock().t:

            entity = self.entity_in_serv.pop(0)

            # set attributes related to completing a service by scheduler
            entity.t_start_service_in_scheduler = None

            return entity

        else:
            return None
    
    def check_working_deadline(self):
        """ returns a list of entities whose work deadline time comes and they will leave 
        the system without being processed by cores """

        expired_entities: List[Entity] = list()

        # first; check entity in service
        if self._is_busy() and self.entity_in_serv[0].t_arrival + \
                self.entity_in_serv[0].t_work_deadline <= Clock().t:
            
            entity = self.entity_in_serv.pop(0)
            
            # set attributes related to an expired entity
            entity.stat = EntityStatus.EXPIRED
            entity.t_in_system = Clock().t - entity.t_arrival
            
            expired_entities.append(entity)

        # second; check entities in queue
        expired_entities = expired_entities + self.queue.check_work_deadline()

        return expired_entities
