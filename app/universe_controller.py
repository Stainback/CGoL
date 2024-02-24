from __future__ import annotations

import pyglet
from pyglet.event import EventDispatcher

from .universe_view import View
from engine.universe import Universe
from .save_manager import SaveManager


class UniverseController(EventDispatcher):
    def __init__(
            self,
            universe: Universe,
            viewport_size: tuple[int, int]
    ):
        self.universe = universe
        self.view = View(
            model=self.universe,
            controller=self,
            viewport_size=viewport_size,
            caption="CONWAY'S GAME OF LIFE"
        )
        self.manager = SaveManager(
            model=self.universe,
            controller=self
        )
        self._ticking = False

    def loop_model(self):
        if not self._ticking:
            pyglet.clock.schedule_interval(self.universe.tick, 0.1)
        elif self._ticking:
            pyglet.clock.unschedule(self.universe.tick)
        self._ticking = not self._ticking

    def save_model(self):
        self.dispatch_event("on_save")

    def set_cells(self, x: float, y: float, value: bool = True):
        self.universe.set_cells(
            self.abs_to_grid((x, y)),
            value=value
        )

    def abs_to_grid(self, coord: tuple | int):
        if isinstance(coord, tuple):
            return (coord[0] // self.view.cell_size[0],
                    coord[1] // self.view.cell_size[1])
        if isinstance(coord, int):
            return coord // self.view.cell_size[0]


UniverseController.register_event_type("on_save")
