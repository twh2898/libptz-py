
from collections import namedtuple


class PTZError(Exception):
    pass


class PTZOptionError(PTZError):
    def __init__(self, options):
        msg = '{} must be one of {}'.format(
            options.name, ','.join(options.options))
        PTZError.__init__(self, msg)


class PTZRangeError(PTZError):
    def __init__(self, speed_range):
        msg = '{} must be in the range [{}, {}]'.format(
            speed_range.name, speed_range.min, speed_range.max)
        PTZError.__init__(self, msg)


def ensure_options(value, options):
    if not value in options.options:
        raise PTZOptionError(options)


def ensure_range(value, range):
    if not range.min <= value <= range.max:
        raise PTZRangeError(range)


Options = namedtuple('Options', ['name', 'options'])
Range = namedtuple('SpeedRange', ['name', 'min', 'max'])
