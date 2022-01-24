from typing import List, Tuple

import numpy as np

from ...enums.entity_type import EntityType

class Environment:
    """ the outer space of system from where the entities come
    
    Args:
        total_num_entities (int): total number of entities to be generated for a simulation
        entity_gen_rate (float): the entity generation rate (poisson lambda rate) in general.
        ent_type1_ratio (float): the ratio of entity type1 numbers
    """

    def __init__(self,
            total_num_entities: int,
            entity_gen_rate: float,
            ent_type1_ratio: float = 1 / 10):

        self._total_num_entities: int = total_num_entities
        """ total number of entities to be generated for a simulation """

        self._ent_gen_rate = entity_gen_rate
        """ the generation rate for entities """
        
        self._ent_type1_ratio: float = ent_type1_ratio
        """ the entity number ratio between type1 and type2 """
    
    
    def schedule_entry_interval_time_into_system(self) -> List[Tuple[float, EntityType]]:
        """ it schedules the entry interval time of entities into the system; also their types are determined """

        times = np.random.exponential(self._ent_gen_rate, size=self._total_num_entities)
        chances = np.random.uniform(size=self._total_num_entities)

        entity_type_time = np.vectorize(lambda ch, t: (EntityType.TYPE1, t) if ch < 0.1 else (EntityType.TYPE2, t))(chances, times)
        return zip(*entity_type_time)