import pyglet

from .universe_view import UniverseView
from engine.universe import Universe


class UniverseController:
    def __init__(self, universe: Universe, view: UniverseView):
        self.universe = universe
        self.view = view
        self.ticking = False

    def on_mouse_press(self, x, y, key, modifiers):
        if key == pyglet.window.mouse.LEFT:
            # self.universe.set_alive(
            #     (
            #         x // self.view._grid_cell[0],
            #         y // self.view._grid_cell[1]
            #     )
            # )
            print((
                    x // self.view._grid_cell[0],
                    y // self.view._grid_cell[1]
                ))
        if key == pyglet.window.mouse.RIGHT:
            self.universe.set_dead(
                (
                    x // self.view._grid_cell[0],
                    y // self.view._grid_cell[1]
                )
            )

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.SPACE:
            if not self.ticking:
                pyglet.clock.schedule_interval(self.universe.tick, 0.1)
            elif self.ticking:
                pyglet.clock.unschedule(self.universe.tick)
            self.ticking = not self.ticking

        if key == pyglet.window.key.W:
            pyglet.clock.schedule_interval(
                self.view.scroll, 1/60.0, direction=(0, 1)
            )
        if key == pyglet.window.key.A:
            pyglet.clock.schedule_interval(
                self.view.scroll, 1/60.0, direction=(-1, 0)
            )
        if key == pyglet.window.key.S:
            pyglet.clock.schedule_interval(
                self.view.scroll, 1/60.0, direction=(0, -1)
            )
        if key == pyglet.window.key.D:
            pyglet.clock.schedule_interval(
                self.view.scroll, 1/60.0, direction=(1, 0)
            )

    def on_key_release(self, key, modifiers):
        if key in (
                pyglet.window.key.W,
                pyglet.window.key.A,
                pyglet.window.key.S,
                pyglet.window.key.D
        ):
            pyglet.clock.unschedule(self.view.scroll)
