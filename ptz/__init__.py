
from collections import namedtuple

class PTZError(Exception):
    pass


class PTZCommandError(PTZError):
    def __init__(self, name, options):
        msg = '{} must be one of {}'.format(name, ','.join(options))
        PTZError.__init__(self, msg)


class PTZSpeedError(PTZError):
    def __init__(self, speed_range):
        msg = '{} must be in the range [{}, {}]'.format(
            speed_range.name, speed_range.min, speed_range.max)
        PTZError.__init__(self, msg)


SpeedRange = namedtuple('SpeedRange', ['name', 'min', 'max'])