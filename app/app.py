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

        self.universe = UniverseView(
            viewport_size=(self.width, self.height),
            configuration=configuration
        )
        self.ticking = False

        self.fps = pyglet.window.FPSDisplay(self)

    def on_draw(self):
        self.clear()
        self.universe.draw()

        self.fps.draw()

    def on_mouse_press(self, x, y, key, modifiers):
        if key == pyglet.window.mouse.LEFT:
            self.universe.set_alive(x, y)
        if key == pyglet.window.mouse.RIGHT:
            self.universe.set_dead(x, y)

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.SPACE:
            if not self.ticking:
                pyglet.clock.schedule_interval(self.universe.tick, 0.1)
            elif self.ticking:
                pyglet.clock.unschedule(self.universe.tick)
            self.ticking = not self.ticking

        if key == pyglet.window.key.W:
            pyglet.clock.schedule_interval(
                self.universe.scroll, 1/60.0, direction=(0, 1)
            )
        if key == pyglet.window.key.A:
            pyglet.clock.schedule_interval(
                self.universe.scroll, 1/60.0, direction=(-1, 0)
            )
        if key == pyglet.window.key.S:
            pyglet.clock.schedule_interval(
                self.universe.scroll, 1/60.0, direction=(0, -1)
            )
        if key == pyglet.window.key.D:
            pyglet.clock.schedule_interval(
                self.universe.scroll, 1/60.0, direction=(1, 0)
            )

    def on_key_release(self, key, modifiers):
        if key in (
                pyglet.window.key.W,
                pyglet.window.key.A,
                pyglet.window.key.S,
                pyglet.window.key.D
        ):
            pyglet.clock.unschedule(self.universe.scroll)
