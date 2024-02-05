import pyglet

from engine import Universe


class UniverseView:
    CELL_SIZE = 16
    GRID_GAP = 2

    def __init__(self, configuration: set[tuple] = None):
        self._universe = Universe(configuration)
        self._universe_batch = pyglet.graphics.Batch()
        self._cells = []

    def draw(self):
        self._cells = [
            pyglet.shapes.Rectangle(
                x=cell[0] * (self.CELL_SIZE + self.GRID_GAP),
                y=cell[1] * (self.CELL_SIZE + self.GRID_GAP),
                width=self.CELL_SIZE,
                height=self.CELL_SIZE,
                batch=self._universe_batch
            )
            for cell in self._universe.alive
        ]
        self._universe_batch.draw()

    def set_alive(self, x: int, y: int):
        self._universe.set_alive(
            (x // (self.CELL_SIZE + self.GRID_GAP),
             y // (self.CELL_SIZE + self.GRID_GAP))
        )

    def tick(self, dt=None):
        self._universe.tick()
        print(f"Cells alive = {len(self._universe.alive)}")
