import pyglet

from .universe_view import UniverseView


class App(pyglet.window.Window):
    def __init__(
            self,
            width: int,
            height: int,
            configuration: set[tuple] = None
    ):
        super().__init__(width, height)
        self.set_caption("CONWAY'S GAME OF LIFE")

        self.universe = UniverseView(configuration)
        self.ticking = False

    def on_draw(self):
        self.clear()
        self.universe.draw()

    def on_mouse_press(self, x, y, key, modifiers):
        if key == pyglet.window.mouse.RIGHT and not self.ticking:
            self.universe.tick()
        if key == pyglet.window.mouse.LEFT:
            self.universe.set_alive(x, y)

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.SPACE:
            if not self.ticking:
                pyglet.clock.schedule_interval(self.universe.tick, 0.1)
            elif self.ticking:
                pyglet.clock.unschedule(self.universe.tick)
            self.ticking = not self.ticking
