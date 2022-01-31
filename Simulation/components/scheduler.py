from .queue import Queue
from .entity import Entity
class Scheduler:

    def __init__(self):
        self._queue: Queue = Queue()


    def enter(self, entity: Entity, t_now: float):
        self._queue.append(entity, t_now)
    
    def exit(self, t_now: float):
        return self._queue.pop(t_now)