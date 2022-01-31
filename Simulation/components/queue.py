from typing import List

from ..enums.entity_type import EntityType
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
    
    def is_empty(self):
        return len(self._entities) == 0