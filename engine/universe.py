class Universe:
    def __init__(self, configuration: set[tuple] = None):
        self._alive = configuration if configuration is not None else set()

    @property
    def alive(self):
        return list(self._alive)

    @staticmethod
    def get_region_around(position: tuple[int, int]) -> set[tuple]:
        return {
            (position[0] + i, position[1] + j)
            for i in range(-1, 2)
            for j in range(-1, 2)
        }

    def get_scope(self) -> set[tuple]:
        scope = set()

        for cell in self._alive:
            scope = scope.union(self.get_region_around(cell))

        return scope

    def set_alive(self, position: tuple[int, int]):
        self._alive.add(position)

    def tick(self):
        scope = self.get_scope()
        generation = {cell for cell in self._alive}

        for cell in scope:
            region_index = len(
                self._alive.intersection(
                    self.get_region_around(cell)
                )
            ) - int(cell in self._alive)

            if cell in self._alive:
                if region_index < 2 or region_index > 3:
                    generation.remove(cell)
            else:
                if region_index == 3:
                    generation.add(cell)

        self._alive = generation


if __name__ == "__main__":
    universe = Universe(
        {(10, 11), (10, 12), (11, 10), (12, 13), (13, 11), (13, 12)}
    )
    universe.tick()
