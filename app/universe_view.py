from __future__ import annotations

import pyglet

from engine import Universe


class UniverseView:
    grid_gap = 2

    def __init__(
            self,
            viewport_size: tuple[int, int],
            viewport_origin: tuple[int, int] = (0, 0),
            configuration: set[tuple] = None,
    ):
        self._universe = Universe(configuration)

        self._cell_image = pyglet.resource.image("images/cell.png")
        self._universe_batch = pyglet.graphics.Batch()

        self._grid_cell = (
            (self._cell_image.width + self.grid_gap),
            (self._cell_image.height + self.grid_gap)
        )
        self._grid_origin = (self.abs_to_grid(viewport_origin[0]),
                             self.abs_to_grid(viewport_origin[1]))
        self._grid_width = (self.abs_to_grid(viewport_size[0]) -
                            self._grid_origin[0])
        self._grid_height = (self.abs_to_grid(viewport_size[1]) -
                             self._grid_origin[1])

        self._cells_sprites = [
            pyglet.sprite.Sprite(
                x=i * self._grid_cell[0],
                y=j * self._grid_cell[1],
                img=self._cell_image,
                batch=self._universe_batch,
            )
            for j in range(self._grid_height)
            for i in range(self._grid_width)
        ]
        self.update()

    def update(self):
        for sprite in self._cells_sprites:
            sprite.visible = False

        for cell in self._universe.alive:
            if (
                    self._grid_origin[0] <= cell[0] <
                    self._grid_origin[0] + self._grid_width and
                    self._grid_origin[1] <= cell[1] <
                    self._grid_origin[1] + self._grid_height
            ):
                self._cells_sprites[
                    (cell[1] - self._grid_origin[1]) * self._grid_width +
                    (cell[0] - self._grid_origin[0])
                    ].visible = True

    def draw(self):
        self._universe_batch.draw()

    def set_alive(self, x: int, y: int):
        target = self.abs_to_grid((x, y))
        self._universe.set_alive(
            (target[0] + self._grid_origin[0], target[1] + self._grid_origin[1])
        )
        self.update()

    def set_dead(self, x: int, y: int):
        target = self.abs_to_grid((x, y))
        self._universe.set_dead(
            (target[0] + self._grid_origin[0], target[1] + self._grid_origin[1])
        )
        self.update()

    def scroll(self, dt, direction: tuple[int, int]):
        self._grid_origin = (self._grid_origin[0] + direction[0],
                             self._grid_origin[1] + direction[1])
        self.update()

    def tick(self, dt=None):
        self._universe.tick()
        self.update()

    def abs_to_grid(self, coord: tuple | int):
        if isinstance(coord, tuple):
            return (coord[0] // self._grid_cell[0],
                    coord[1] // self._grid_cell[1])
        if isinstance(coord, int):
            return coord // self._grid_cell[0]
