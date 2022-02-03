from typing import List

from ..enums.entity_type import EntityType
from ..enums.entity_stat import EntityStatus
from .entity import Entity
from .clock import Clock

class Queue:
    """ the queue object putting entities in waiting list before taking a service """

    def __init__(self):

        self.entities: List[Entity] = list()
        """ entities in waiting list """

    def add(self, entity: Entity):
        """ add a new entity into queue """

        insert_ix: int = 0
        
        # priority of entity type 1 is always greater than type 2
        if entity.type == EntityType.TYPE1:

            for e in self.entities:
            
                if e.type == EntityType.TYPE2:
                    insert_ix += 1
        
        # set attribute related to entering the queue
        entity.t_start_in_queue = Clock().t

        self.entities.insert(insert_ix, entity)
    
    def pop(self):
        """ it pops and returns an entity from waiting list """

        # EAFP rule
        try:

            entity: Entity = self.entities.pop()

            # set attribute related to exiting the queue
            entity.t_in_queue += (Clock().t - entity.t_start_in_queue)
            entity.t_start_in_queue = None
            
            return entity
        
        except:
            return None
    
    def check_work_deadline(self):
        """ returns a list of entities whose work deadline time comes and they will leave 
        the system without being processed by cores """

        expired_entities: List[Entity] = list()

        idx = 0

        while idx < len(self.entities):
        
            if self.entities[idx].t_arrival + self.entities[idx].t_work_deadline \
                     <= Clock().t:
        
                entity: Entity = self.entities.pop(idx)

                # set attribute related to expiring
                entity.stat = EntityStatus.EXPIRED
                entity.t_in_system = Clock().t - entity.t_arrival

                expired_entities.append(entity)

            else:
                idx += 1
        
        return expired_entities

        
    def is_empty(self):
        """ returns whether the queue is empty or not """

        return len(self.entities) == 0
    
    def queue_len(self):
        """ returns length of queue within the server """

        return len(self.entities)