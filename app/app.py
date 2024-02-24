import pyglet

from engine.universe import Universe
from .universe_controller import UniverseController


class App:
    def __init__(
            self,
            width: int,
            height: int,
            configuration: set[tuple] = None
    ):
        self.universe = Universe(configuration)
        self.controller = UniverseController(
            universe=self.universe,
            viewport_size=(width, height)
        )
