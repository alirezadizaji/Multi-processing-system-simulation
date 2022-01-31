from typing import List

import numpy as np

from ..entity import Entity
from .scheduler import Scheduler
from .server import Server

class System:

    def __init__(self, entities, t_scale):
        super(System, self).__init__()

        self.t: float = 0
        self._t_scale: float = t_scale
        self._entities = entities
        
        self._total_num_entities: int = len(entities)
        self._done_entities = list()

        self._scheduler: Scheduler = Scheduler()
        self._servers: List[Server] = [Server() for i in range(5)]

    def choose_server(self):
        servers_len = np.asarray([s.queue_len() for s in self._servers])
        idx = np.argmin(servers_len)
        if np.sum(servers_len == servers_len[idx]) > 1:
            idx = np.random.uniform(servers_len.size)
        
        return idx

    def simulate(self):

        while len(self._done_entities) < self._total_num_entities:

            while self._entities[0].t_arrival <= self.t:
                entity = self._entities.pop[0]
                self._scheduler.enter(entity, self.t)            
            
            entity = self._scheduler.exit(self.t)
            if entity is not None:
                idx = self.choose_server()
                self._servers[idx].add_entity(entity)
            
            for s in self._servers:
                s.check_cores(self.t)

            self.t += self._t_scale
