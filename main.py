import numpy as np

from Simulation.components.environment import Environment
from Simulation.components.system import System

def run_simulation():
    environment = Environment(10000, 5, 0.4)
    entites = environment.create_entites()
    system = System(entites, 0.1)
    system.simulate()
    
if __name__ == "__main__":
    np.random.seed(12345)

    run_simulation()