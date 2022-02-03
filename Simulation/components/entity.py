from ..enums.entity_stat import EntityStatus
from ..enums.entity_type import EntityType

class Entity:
    """ entity object of the simulation; they are going to be processed by server cores
    
    Args:
        t_arrival (float): time arrival into the system
        t_work_deadline (float): working deadline time (time to tolerate being in a queue)
        ent_type (EntityType): type of entity; type1 is always preferred at the top of a queue
    """
    def __init__(self,
            t_arrival: float,
            t_work_deadline: float,
            ent_type: EntityType):

        super(Entity, self).__init__()

        self.t_arrival: float = t_arrival
        """ time arrival into the system """

        self.t_work_deadline: float = t_work_deadline
        """ working deadline time (time to tolerate being in a queue) """

        self.type: EntityType = ent_type
        """type of entity; type1 is always preferred at the top of a queue """

        self.t_in_system: float = 0
        """ total time being in system """

        self.t_in_queue: float = 0
        """ total time being in queues """

        self.t_start_in_queue: float = None
        """ record the time whenever it enters within a queue """

        self.t_service_in_core: float = 0
        """ service time assigned by a core """

        self.t_start_service_in_core: float = None
        """ record the time when entity starts a service from a core """

        self.t_service_in_scheduler: float = 0
        """ service time assigned by scheduler """

        self.t_start_service_in_scheduler: float = 0
        """ time starting service within scheduler """

        self.stat: EntityStatus = EntityStatus.IN_PROG
        """ the current status of entity """