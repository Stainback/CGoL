from __future__ import annotations

import pyglet

from app_config import IMG_CELL
from app.app_component import AppComponent
from engine.models.universe_model import Universe


class UniverseView(AppComponent):
    grid_gap = 2

    def __init__(
            self,
            model: Universe,
            viewport_width: int, viewport_height: int,
            viewport_origin: tuple[int, int] = (0, 0),
    ):
        self.model = model

        self._view_batch = pyglet.graphics.Batch()
        self._cell_image = IMG_CELL
        self._cell_size = (
            (self._cell_image.width + self.grid_gap),
            (self._cell_image.height + self.grid_gap)
        )

        self._sprite_field = {
            (i, j): pyglet.sprite.Sprite(
                x=i,
                y=j,
                img=self._cell_image,
                batch=self._view_batch,
            )
            for j in range(0, viewport_height, self.cell_size[1])
            for i in range(0, viewport_width, self.cell_size[0])
        }
        self.origin = viewport_origin

    @property
    def cell_size(self):
        return self._cell_size

    @property
    def sprite_field(self):
        return self._sprite_field

    @property
    def origin(self):
        return self._viewport_origin

    @origin.setter
    def origin(self, point: tuple[int, int]):
        self._viewport_origin = point
        self.on_update()

    def draw(self):
        self._view_batch.draw()

    def on_update(self):
        for sprite in self._sprite_field.values():
            sprite.visible = False

        for cell in self.model.alive:
            sprite = self._sprite_field.get(
                (
                    cell[0] * self.cell_size[0] - self._viewport_origin[0],
                    cell[1] * self.cell_size[1] - self._viewport_origin[1]
                )
            )

            if sprite:
                sprite.visible = True
