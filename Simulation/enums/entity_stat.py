class EntityStatus:

    IN_PROG = "IN_PROGRESS"
    """ neither expired nor taking service from a core """

    EXPIRED = "EXPIRED"
    """ the work deadline time has come then the entity will leave the system without being processed by cores"""

    DONE = "DONE"
    """ after taking service from a core """