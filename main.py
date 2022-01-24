from Simulation.components.world import World
from Simulation.components.environment import Environment

if __name__ == "__main__":
    environment = Environment(10000, 5)
    world = World(environment)
    world.run()