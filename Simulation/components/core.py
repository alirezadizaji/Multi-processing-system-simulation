from typing import List

import numpy as np

from .entity import Entity
from ..enums.entity_stat import EntityStatus

class Core:

    def __init__(self, exp_rate: float):
        self._t_services = np.random.exponential(scale=exp_rate, size=10000).tolist()
        self._entity: List[Entity] = list()

    def assign_entity(self, entity: Entity, t_now: float):
        entity.t_service = self._t_services.pop[0]
        entity.t_start_service = t_now
        self._entity = [entity]
        self.busy = True

    def is_busy(self):
        return len(self._entity) > 0    
    
    def check_entity_done(self, t_now):
        if self._entity[0].t_start_service + self._entity[0].t_service <= t_now:
            entity = self._entity.pop()
            entity.stat = EntityStatus.DONE
            return entity
        else:
            return None
