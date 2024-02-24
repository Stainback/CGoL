from __future__ import annotations

import pyglet

from engine import Universe
# from .universe_controller import UniverseController


class View(pyglet.window.Window):
    grid_gap = 2

    def __init__(
            self,
            model: Universe,
            controller,
            viewport_size: tuple[int, int],
            viewport_origin: tuple[int, int] = (0, 0),
            caption: str = "View"
    ):
        super().__init__(*viewport_size)
        self.set_location(40, 40)
        self.set_caption(caption)

        self.model = model
        self.controller = controller
        self.model.push_handlers(self)
        self.controller.push_handlers(self)

        self._viewport_origin = viewport_origin
        self._view_batch = pyglet.graphics.Batch()
        self._cell_image = pyglet.resource.image("images/cell.png")
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
            for j in range(0, self.height, self.cell_size[1])
            for i in range(0, self.width, self.cell_size[0])
        }
        self.on_update()

        self._scroll_direction = [0, 0]

    @property
    def cell_size(self):
        return self._cell_size

    @property
    def sprite_field(self):
        return self._sprite_field

    @property
    def origin(self):
        return self._viewport_origin

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

    def on_draw(self):
        self.clear()
        self._view_batch.draw()

    def on_mouse_press(self, x, y, key, modifiers):
        if key in (pyglet.window.mouse.LEFT, pyglet.window.mouse.RIGHT):
            self.controller.set_cells(
                x + self._viewport_origin[0],
                y + self._viewport_origin[1],
                key == pyglet.window.mouse.LEFT
            )

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.SPACE:
            self.controller.loop_model()
        if key == pyglet.window.key.LSHIFT:
            self.controller.save_model()

        if key in (
                pyglet.window.key.W,
                pyglet.window.key.A,
                pyglet.window.key.S,
                pyglet.window.key.D
        ):
            if key == pyglet.window.key.W:
                self._scroll_direction[1] = 1
            if key == pyglet.window.key.A:
                self._scroll_direction[0] = -1
            if key == pyglet.window.key.S:
                self._scroll_direction[1] = -1
            if key == pyglet.window.key.D:
                self._scroll_direction[0] = 1

            pyglet.clock.unschedule(self._scroll)
            if self._scroll_direction != [0, 0]:
                pyglet.clock.schedule_interval(
                    self._scroll, 1/60.0, direction=self._scroll_direction
                )

    def on_key_release(self, key, modifiers):
        if key in (
                pyglet.window.key.W,
                pyglet.window.key.A,
                pyglet.window.key.S,
                pyglet.window.key.D
        ):
            if key in (pyglet.window.key.W, pyglet.window.key.S):
                self._scroll_direction[1] = 0
            if key in (pyglet.window.key.A, pyglet.window.key.D):
                self._scroll_direction[0] = 0
            pyglet.clock.unschedule(self._scroll)
            if self._scroll_direction != [0, 0]:
                pyglet.clock.schedule_interval(
                    self._scroll, 1/60.0, direction=self._scroll_direction
                )

    def _scroll(self, dt, direction: list[int, int]):
        self._viewport_origin = (
            self._viewport_origin[0] + direction[0] * self.cell_size[0],
            self._viewport_origin[1] + direction[1] * self.cell_size[1],
        )
        self.on_update()
