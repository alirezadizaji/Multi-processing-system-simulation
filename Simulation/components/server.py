from typing import List

import numpy as np

from .core import Core
from .entity import Entity
from .queue import Queue

class Server:
    def __init__(self, core_rates=[0.1, 0.2, 0.3]):
        self._cores: List[Core] = [Core(rate) for rate in core_rates]
        self._queue: Queue = Queue()
    
    def add_entity(self, entity, t_now):
        self._queue.append(entity, t_now)
    
    def check_cores(self, t_now):
        entities: List[Entity] = list()
        for core in self._cores:
            if not core.is_busy():
                if not self._queue.is_empty():
                    entity = self._queue.pop(t_now)
                    core.assign_entity(entity, t_now)
            else:
                entity = core.check_entity_done(t_now)
                if entity is not None:
                    entities.append(entity)

        return entities
    
    def check_working_deadline(self, t_now: float):
        return self._queue.check_work_deadline()

    def queue_len(self):
        return len(self._queue)