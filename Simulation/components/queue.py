from typing import List

from ..enums.entity_type import EntityType
from ..enums.entity_stat import EntityStatus
from .entity import Entity

class Queue:

    def __init__(self):

        self._entities: List[Entity] = list()
    
    def append(self, entity: Entity, t_now: float):
        insert_ix: int = 0
        if entity.type == EntityType.TYPE1:
            for e in self._entities:
                if e.type == EntityType.TYPE2:
                    insert_ix += 1
        entity.t_start_in_queue = t_now
        self._entities.insert(insert_ix, entity)
    
    def pop(self, t_now):
        try:
            entity: Entity = self._entities.pop()
            entity.t_in_queue += (t_now - entity.t_start_in_queue)
            entity.t_start_in_queue = None
            return entity
        except:
            return None
    
    def check_work_deadline(self, t_now: float):
        entities: List[Entity] = list()

        idx = 0
        while idx < len(self._entities):
            if self._entities[idx].t_arrival + self._entities[idx].t_work_deadline <= t_now:
                entity: Entity = self._entities.pop(idx)
                entity.stat = EntityStatus.QUIT
                entity.t_in_system = t_now - entity.t_arrival
            else:
                idx += 1
        
        return entities

        
    def is_empty(self):
        return len(self._entities) == 0