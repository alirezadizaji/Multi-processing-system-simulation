from typing import List

import numpy as np

from .core import Core
from .entity import Entity
from .queue import Queue

class Server:
    """ server contains several cores for processing and a queue for waiting list 
    
    Args:
        cores (List[Core]): list of cores
    """
    def __init__(self, cores: List[Core]):

        self.cores: List[Core] = cores
        """ list of cores within the server """

        self.queue: Queue = Queue()
        """ the queue within the server """


    def enter_entity(self, entity: Entity):
        """ enters an entity into the server; indeed at first it directly enters into the queue """

        self.queue.add(entity)

    
    def check_cores(self):
        """ check the current status of cores; whether they are busy or not and if not,
        assign a new entity for them (if queue is not empty). also if any entity has been processed 
        then return it
        
        Returns:
            done_entities (List[Entity]): a list of processed entities by cores
        """
        
        done_entities: List[Entity] = list()
        
        for core in self.cores:
            
            if not core.is_busy():

                # assign a new entity to the core if queue is not empty
                if not self.queue.is_empty():
                    entity = self.queue.pop()
                    core.set_entity_in_serv(entity)

            else:
                
                # check whether the entity in service is done with processing or not
                entity = core.check_entity_in_serv_done()

                if entity is not None:
                    done_entities.append(entity)

        return done_entities

    
    def check_working_deadline(self):
        """ returns a list of entities whose work deadline time comes and they will leave 
        the system without being processed by cores """

        return self.queue.check_work_deadline()