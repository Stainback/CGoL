from __future__ import annotations

import pyglet

from engine import Universe


class UniverseView:
    def __init__(
            self,
            visible_universe_abs: dict,
            configuration: set[tuple] = None,
    ):
        self._universe = Universe(configuration)

        self._cell_image = pyglet.resource.image("images/cell.png")

        self._universe_batch = pyglet.graphics.Batch()

        self.visible_universe_abs = visible_universe_abs
        self.visible_universe_grid = {
            "left_x": self.abs_to_grid(self.visible_universe_abs["left_x"]),
            "bottom_y": self.abs_to_grid(self.visible_universe_abs["bottom_y"]),
            "right_x": self.abs_to_grid(self.visible_universe_abs["right_x"]),
            "top_y": self.abs_to_grid(self.visible_universe_abs["top_y"])
        }
        self.grid_width = (self.visible_universe_grid["right_x"] -
                           self.visible_universe_grid["left_x"])
        self.grid_height = (self.visible_universe_grid["top_y"] -
                            self.visible_universe_grid["bottom_y"])

        self.cell_counter = pyglet.text.Label(
            x=self.visible_universe_abs["right_x"],
            y=self.visible_universe_abs["bottom_y"],
            anchor_x="right",
            anchor_y="bottom",
            color=(0, 255, 0, 255)
        )

        self._cells_sprites = [
            pyglet.sprite.Sprite(
                x=i,
                y=j,
                img=self._cell_image,
                batch=self._universe_batch,
            )
            for j in range(
                self.visible_universe_abs["bottom_y"],
                self.visible_universe_abs["top_y"],
                self._cell_image.height + 2
            )
            for i in range(
                self.visible_universe_abs["left_x"],
                self.visible_universe_abs["right_x"],
                self._cell_image.width + 2
            )
        ]
        self.update_cells_sprites()

    def update_cells_sprites(self):
        for sprite in self._cells_sprites:
            sprite.visible = False

        for cell in self._universe.alive:
            if (
                    self.visible_universe_grid["left_x"] <= cell[0] <
                    self.visible_universe_grid["right_x"] and
                    self.visible_universe_grid["bottom_y"] <= cell[1] <
                    self.visible_universe_grid["top_y"]
            ):
                self._cells_sprites[
                    cell[0] + cell[1] * self.grid_height
                    ].visible = True

    def draw(self):
        self._universe_batch.draw()
        self.cell_counter.draw()

    def set_alive(self, x: int, y: int):
        self._universe.set_alive(
            self.abs_to_grid((x, y))
        )
        self.update_cells_sprites()

    def set_dead(self, x: int, y: int):
        self._universe.set_dead(
            self.abs_to_grid((x, y))
        )
        self.update_cells_sprites()

    def tick(self, dt=None):
        self._universe.tick()
        self.update_cells_sprites()
        self.cell_counter.text = f"C:{len(self._universe.alive)}"

    def abs_to_grid(self, coord: tuple | int):
        if isinstance(coord, tuple):
            return (coord[0] // (self._cell_image.width + 2),
                    coord[1] // (self._cell_image.height + 2))
        if isinstance(coord, int):
            return coord // (self._cell_image.width + 2)
