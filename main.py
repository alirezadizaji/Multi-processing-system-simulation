from typing import List

import numpy as np

from Simulation.components import  Core, Environment, Server, System
    
if __name__ == "__main__":
    np.random.seed(12345)

    num_cores = 3
    num_servers = 5
    total_num_entities = 1000000

    # entity generation rate (poi), work deadline mean (exp), service rate at scheduler (poi)
    lamda, alpha, mu = map(float, input().split())
    
    servers: List[Server] = list()

    for i in range(num_servers):

        # service rate (exp) for each core
        core_serv_rates = map(float, input().split())

        cores: List[Core] = list()
        for rate in core_serv_rates:
            cores.append(
                    Core(rate, max_num_entities_to_come=total_num_entities)
            )

        servers.append(Server(cores))
    
    environment = Environment(10000, 5, 0.4)
    entites = environment.create_entites()
    system = System(entites, 0.1)
    system.simulate()
    system.report()