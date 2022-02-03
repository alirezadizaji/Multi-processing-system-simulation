from typing import List

import numpy as np

from Simulation.components import  Core, Environment, Scheduler, Server, System
    
if __name__ == "__main__":
    np.random.seed(12345)

    num_cores = 3
    num_servers = 5
    total_num_entities = 10000

    # entity generation rate (poi), work deadline mean (exp), service rate at scheduler (poi)
    lamda, alpha, mu = map(float, input().split())
    
    environment = Environment(total_num_entities, lamda, alpha)
    entites = environment.create_entites()

    scheduler = Scheduler(mu, total_num_entities)

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

    system = System(entites, scheduler, servers)
    system.simulate()
    system.report()