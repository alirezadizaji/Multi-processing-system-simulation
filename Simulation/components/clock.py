from ..utils import singleton_creator

@singleton_creator
class Clock:
    """ the system clock """

    def __init__(self):
        super(Clock, self).__init__()

        self.t: float = 0.0
        """ current time in system """

        self._t_scale: float = 0.1
        """ time scale in system """

    def pass_time(self):
        """ time passes in system """

        self.t += self._t_scale