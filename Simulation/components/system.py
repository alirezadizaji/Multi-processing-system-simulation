from typing import Dict, List

import numpy as np

from .clock import Clock
from .entity import Entity
from ..enums.entity_type import EntityType
from ..enums.entity_stat import EntityStatus
from .scheduler import Scheduler
from .server import Server

class System:
    """ the system simulates the project and it possesses several servers and an scheduler 
    
    Args:
        entities (List[Entity]): total entities generated by the environment
        scheduler (Scheduler): time scheduler of system
        servers (List[Server]): servers of the system possessing several cores for processing
    """


    def __init__(self,
            entities: List[Entity],
            scheduler: Scheduler,
            servers: List[Server]):

        super(System, self).__init__()

        self.tot_entities = entities
        """ total entities generated by the environment """

        self._total_num_entities: int = len(entities)
        """ total number of entities to be examined """

        self._done_entities: List[Entity] = list()
        """ a list of entities completely DONE or EXPIRED """

        self._scheduler: Scheduler = Scheduler(rate=0.4)
        """ time scheduler of system """
        
        self._servers: List[Server] = [Server() for i in range(5)]
        """ servers of the system possessing several cores for processing """


    def choose_server(self):
        """ choose a server to assign an entity for it """

        servers_queue_len = np.asarray([s.queue.queue_len() for s in self._servers])
        
        # pick the server with minimum queue length
        idx = np.argmin(servers_queue_len)

        candidate_servers = np.where(servers_queue_len == servers_queue_len[idx])

        # if one server remains select it O.W. randomly choose among them
        idx = np.random.choice(candidate_servers)
        
        return idx

    def simulate(self):
        """ run simulation """

        while len(self._done_entities) < self._total_num_entities:
            
            self._test()

            expired_entities: List[Entity] = list()
            
            # add entities into the system if their arrival time has come
            while self.tot_entities and self.tot_entities[0].t_arrival <= Clock().t:
                entity = self.tot_entities.pop(0)
                self._scheduler.enter(entity)            
            
            # examine entity in service and expired entities of the scheduler
            self._scheduler.set_entity_in_serv()
            expired_entities = expired_entities + self._scheduler.check_working_deadline(self.t)
            entity = self._scheduler.check_entity_in_serv_done()

            # if scheduler returns a processed entity, then assigns it to a server
            if entity is not None:
                idx = self.choose_server()
                self._servers[idx].enter_entity(entity)
            
            # check expired entities and entities in service of cores for each server
            for s in self._servers:

                expired_entities = expired_entities + s.check_working_deadline()
                
                for done_entity in s.check_cores():
                    self._done_entities.append(done_entity)

            for e in expired_entities:
                self._done_entities.append(e)
                

            num_entities = len(self._scheduler.queue.entities) + len(self._scheduler.entity_in_serv)
            num_entities += len(self.tot_entities) + len(self._done_entities)
            for s in self._servers:
                num_entities += len(s.queue.entities)
                for c in s.cores:
                    num_entities += len(c.entity_in_serv)
    
    def _test(self):
        """ it tests whether the number of entities currently in system and 
        should be in system are equivalent or not """

        num_entities_in_scheduler = self._scheduler.queue.queue_len() + len(self._scheduler.entity_in_serv)
        num_entities_not_entered_yet = len(self.tot_entities)
        num_entities_done = len(self._done_entities)
        
        num_entities_in_servers = 0
        for s in self._servers:
            num_entities_in_servers += len(s.queue.entities)
            for c in s.cores:
                num_entities_in_servers += len(c.entity_in_serv)

        num_entities_in_system = num_entities_in_scheduler + num_entities_not_entered_yet \
                                    + num_entities_done + num_entities_in_servers
        
        assert num_entities_in_system == self._total_num_entities, \
                f"expected {self._total_num_entities}; got {num_entities_in_system} instead."

    def report(self):
        """ reports the simulation results """

        expired = [0, 0]
        in_system = [0, 0]
        t_in_queue = [0, 0]
        
        for e in self._done_entities:

            idx = 0 if e.type == EntityType.TYPE1 else 1
            
            in_system[idx] += e.t_in_system
            
            if e.stat == EntityStatus.EXPIRED:
                expired[idx] += 1
            
            t_in_queue[idx] += e.t_in_queue
        
        print(expired)
        print(in_system)
        print(t_in_queue)
