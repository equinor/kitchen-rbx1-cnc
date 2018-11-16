import importlib.util
from .Server import Server
try:
    importlib.util.find_spec('RPi.GPIO')
    from .Robot import Robot
except ImportError:
    from .MockRobot import MockRobot as Robot