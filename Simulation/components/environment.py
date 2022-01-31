from typing import List, Tuple

import numpy as np

from ..enums.entity_type import EntityType
from .entity import Entity

class Environment:
    """ the outer space of system from where the entities come
    
    Args:
        total_num_entities (int): total number of entities to be generated for a simulation
        entity_generation_rate (float): the entity generation rate (entities per second; poission distribution)
        entity_working_deadline_mean (float): the entity working deadline mean (second; exponential distribution)
        ent_type1_ratio (float): the ratio of entity type1 numbers
    """

    def __init__(self,
            total_num_entities: int,
            entity_generation_rate: float,
            entity_working_deadline_mean: float,
            ent_type1_ratio: float = 1 / 10):

        self._total_num_entities: int = total_num_entities
        """ total number of entities to be generated for a simulation """

        self._ent_gen_rate: float = entity_generation_rate
        """ the generation rate for entities """

        self._ent_work_dead_mean: float = entity_working_deadline_mean
        """ the entity working deadline mean (second; exponential distribution) """

        self._ent_type1_ratio: float = ent_type1_ratio
        """ the entity number ratio between type1 and type2 """
    
    
    def create_entites(self) -> List[Entity]:
        """ it creates entites and initiates their type, arrival and working deadline time;
        
        Returns:
            (List[Entity]): a list of all entities should be processed for simulation
        """

        ts_interval = np.random.exponential(1.0 / self._ent_gen_rate, size=self._total_num_entities)
        ts_arrival = np.cumsum(ts_interval)
        ts_work_deadline = np.random.exponential(self._ent_work_dead_mean, size=self._total_num_entities)
        chances = np.random.uniform(size=self._total_num_entities)

        def _init_entity(t_arrival, t_work_deadline, chance):
            e_type = EntityType.TYPE1 if chance < 0.1 else EntityType.TYPE2
            return Entity(t_arrival, t_work_deadline, e_type)

        entities = np.vectorize(_init_entity)(ts_arrival, ts_work_deadline, chances)
        
        return entities.tolist()