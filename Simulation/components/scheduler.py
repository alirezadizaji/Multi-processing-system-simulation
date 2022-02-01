from typing import List

import numpy as np

from .queue import Queue
from .entity import Entity
from ..enums.entity_stat import EntityStatus

class Scheduler:

    def __init__(self, rate):
        self._queue: Queue = Queue()
        self._entity: List[Entity] = None
        self._ts_service = np.random.exponential(1.0 / rate, size=10000).tolist()

    def enter(self, entity: Entity, t_now: float):
        self._queue.append(entity, t_now)
    
    def assign_entity(self, t_now: float):
        if len(self._queue) > 0:
            entity = self._queue.pop(t_now)
            entity.t_start_service_in_scheduler = t_now
            entity.t_service_in_scheduler = self._ts_service.pop(0)
            self._entity = [entity]
    
    def check_entity_in_service(self, t_now: float):
        if self._entity and self._entity[0].t_start_service_in_scheduler + \
                self._entity[0].t_service_in_scheduler <= t_now:
            entity = self._entity.pop(0)
            return entity
        else:
            return None
    
    def check_working_deadline(self, t_now: float):
        entities: List[Entity] = list()

        if self._entity and self._entity[0].t_arrival + \
                self._entity[0].t_work_deadline <= t_now:
            entity = self._entity.pop(0)
            entity.stat = EntityStatus.QUIT
            entity.t_in_system = t_now - entity.t_arrival
            entities.append(entity)

        entities = entities + self._queue.check_work_deadline()
        return entities