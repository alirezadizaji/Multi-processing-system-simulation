import time
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

        self._scheduler: Scheduler = scheduler
        """ time scheduler of system """
        
        self._servers: List[Server] = servers
        """ servers of the system possessing several cores for processing """

        self._iteration: int = 0
        """ number of iterations during simulation """


    def choose_server(self):
        """ choose a server to assign an entity for it """

        servers_queue_len = np.asarray([s.queue.queue_len() for s in self._servers])
        
        # pick the server with minimum queue length
        idx = np.argmin(servers_queue_len)

        candidate_servers = np.argwhere(servers_queue_len == servers_queue_len[idx]).ravel()

        # if one server remains select it O.W. randomly choose among them
        idx = np.random.choice(candidate_servers)
        
        return idx

    def simulate(self):
        """ run simulation """

        while len(self._done_entities) < self._total_num_entities:
            
            expired_entities: List[Entity] = list()
            
            # add entities into the system if their arrival time has come
            while self.tot_entities and self.tot_entities[0].t_arrival <= Clock().t:
                entity = self.tot_entities.pop(0)
                self._scheduler.enter(entity)
            
            # examine entity in service and expired entities of the scheduler
            self._scheduler.set_entity_in_serv()
            expired_entities = expired_entities + self._scheduler.check_working_deadline()
            entity = self._scheduler.check_entity_in_serv_done()

            self._scheduler.queue.record_length()

            # if scheduler returns a processed entity, then assigns it to a server
            if entity is not None:
                idx = self.choose_server()
                self._servers[idx].enter_entity(entity)
            
            # check expired entities and entities in service of cores for each server
            for s in self._servers:

                expired_entities = expired_entities + s.check_working_deadline()
                
                for done_entity in s.check_cores():
                    self._done_entities.append(done_entity)

                s.queue.record_length()

            for e in expired_entities:
                self._done_entities.append(e)

            self._log()
            self._iteration += 1

            Clock().pass_time()

    def _log(self):
        """ it prints current status of simulation """

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
        
        print(f"time: {Clock().t: .2f}, num not entered: {num_entities_not_entered_yet}, num in scheduler: {num_entities_in_scheduler}, num done or expired: {num_entities_done}, total num: {num_entities_in_system}", flush=True)
    
    
    def report(self):
        """ reports the simulation results """

        num_expired = np.zeros(2, dtype=int)
        num_ent_type = np.zeros(2, dtype=int)
        time_in_system = np.zeros((2, self._total_num_entities))
        time_in_queue = np.zeros_like(time_in_system)

        for i, e in enumerate(self._done_entities):

            e_type = 0 if e.type == EntityType.TYPE1 else 1
            num_ent_type[e_type] += 1
            time_in_system[e_type][i] = e.t_in_system
            
            if e.stat == EntityStatus.EXPIRED:
                num_expired[e_type] += 1
            
            time_in_queue[e_type][i] = e.t_in_queue
        

        print("\n***")
        print(f"percentage of expired entities per type (%): {num_expired * 100 / num_ent_type}, per case (%): {num_expired.sum() * 100 / self._total_num_entities}", flush=True)
        print(f"Avg time being in system per type (sec): {time_in_system.sum(1) / num_ent_type}, per case (sec): {time_in_system.sum() / self._total_num_entities}", flush=True)
        print(f"Avg time being in queue per type (sec): {time_in_queue.sum(1) / num_ent_type}, per case (sec): {time_in_queue.sum() / self._total_num_entities}", flush=True)
        print(f"Avg queue length in scheduler: {self._scheduler.queue.total_length / self._iteration}")
        
        for i, s in enumerate(self._servers):
            print(f"Avg queue length in server{i+1}: {s.queue.total_length / self._iteration}")

        print("***")