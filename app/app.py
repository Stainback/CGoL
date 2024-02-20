import pyglet

from engine.universe import Universe
from .universe_view import UniverseView
from .universe_controller import UniverseController
from .save_manager import SaveManager


class App(pyglet.window.Window):
    def __init__(
            self,
            width: int,
            height: int,
            configuration: set[tuple] = None
    ):
        super().__init__(width, height)
        self.set_caption("CONWAY'S GAME OF LIFE")

        self.universe = Universe(configuration)
        self.universe_view = UniverseView(
            subject=self.universe,
            viewport_size=(self.width, self.height),
        )
        self.controller = UniverseController(self.universe, self.universe_view)
        self.push_handlers(self.controller)

        self.save_manager = SaveManager()

        self.fps = pyglet.window.FPSDisplay(self)

    def on_draw(self):
        self.clear()
        self.universe_view.draw()

        self.fps.draw()
