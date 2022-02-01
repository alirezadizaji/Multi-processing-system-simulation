from ..enums.entity_stat import EntityStatus
from ..enums.entity_type import EntityType

class Entity:
    """ entity object of the simulation; they are going to be processed by server cores
    
    Args:
        t_arrival (float): time arrival into the system
        t_work_deadline (float): working deadline time (it won't tolerate further being in a queue)
        ent_type (EntityType): type of entity (1 or 2)
    """
    def __init__(self,
            t_arrival: float,
            t_work_deadline: float,
            ent_type: EntityType,
            name: str):

        super(Entity, self).__init__()

        self.t_arrival: float = t_arrival
        """ time arrival into the system """

        self.t_work_deadline: float = t_work_deadline
        """ working deadline time (it won't tolerate further being in a queue """

        self.type: EntityType = ent_type
        """ type of entity (1 or 2) """

        self.t_in_system: float = 0

        self.t_in_queue: float = 0

        self.t_start_in_queue: float = None

        self.t_service_in_core: float = 0

        self.t_start_service_in_core: float = None

        self.t_service_in_scheduler: float = 0

        self.t_start_service_in_scheduler: float = 0

        self.stat: EntityStatus = EntityStatus.IN_PROG

        self._name = name
        