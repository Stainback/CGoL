from __future__ import annotations

from pyglet.event import EventDispatcher


class Universe(EventDispatcher):
    def __init__(self, configuration: set[tuple] = None):
        self.alive = configuration

    @property
    def alive(self):
        return list(self._alive)

    @alive.setter
    def alive(self, configuration: set[tuple]):
        self._alive = configuration if configuration is not None else set()
        self.dispatch_event("on_update", self.alive)

    @staticmethod
    def _get_region_around(position: tuple[int, int]) -> set[tuple]:
        return {
            (position[0] + i, position[1] + j)
            for i in range(-1, 2)
            for j in range(-1, 2)
        }

    def _get_scope(self) -> set[tuple]:
        scope = set()

        for cell in self._alive:
            scope = scope.union(self._get_region_around(cell))

        return scope

    def set_cells(
            self,
            configuration: set[tuple] | tuple[int, int],
            value: bool
    ):
        if isinstance(configuration, tuple):
            configuration = {configuration}

        if value:
            self.alive = self._alive.union(configuration)
        else:
            self.alive = self._alive.difference(configuration)

    def tick(self, dt):
        scope = self._get_scope()
        generation = {cell for cell in self._alive}

        for cell in scope:
            region_index = len(
                self._alive.intersection(
                    self._get_region_around(cell)
                )
            ) - int(cell in self._alive)

            if cell in self._alive:
                if region_index < 2 or region_index > 3:
                    generation.remove(cell)
            else:
                if region_index == 3:
                    generation.add(cell)

        self.alive = generation


Universe.register_event_type("on_universe_update")
