from __future__ import annotations

from pyglet.event import EventDispatcher


class Universe(EventDispatcher):
    def __init__(self, configuration: set[tuple] = None) -> None:
        self.alive = configuration

    @property
    def alive(self) -> set:
        return self._alive

    @alive.setter
    def alive(self, configuration: set[tuple]) -> None:
        self._alive = configuration if configuration is not None else set()
        self.dispatch_event("on_update")

    @staticmethod
    def _get_region_around(position: tuple[int, int]) -> set[tuple]:
        return {
            (position[0] + i, position[1] + j)
            for i in range(-1, 2)
            for j in range(-1, 2)
        }

    def _get_scope(self) -> set[tuple]:
        """
            Returns set with all cells around alive cells. It uses as a scope
            of simulation at current step.
        """
        scope = set()

        for cell in self.alive:
            scope = scope.union(self._get_region_around(cell))

        return scope

    def set_cells(
            self,
            configuration: set[tuple] | tuple[int, int],
            value: bool = True
    ) -> None:
        """
            Sets a cell or a group of cells as alive (by default) or dead.
        """
        if isinstance(configuration, tuple):
            configuration = {configuration}

        if value:
            self.alive = self.alive.union(configuration)
        else:
            self.alive = self.alive.difference(configuration)

    def tick(self) -> None:
        """
            Perform a simulation step.
        """
        scope = self._get_scope()
        generation = {cell for cell in self.alive}

        for cell in scope:
            region_index = len(
                self.alive.intersection(
                    self._get_region_around(cell)
                )
            ) - int(cell in self.alive)

            if cell in self.alive:
                if region_index < 2 or region_index > 3:
                    generation.remove(cell)
            else:
                if region_index == 3:
                    generation.add(cell)

        self.alive = generation


Universe.register_event_type("on_update")
