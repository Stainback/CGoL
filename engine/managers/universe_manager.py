import pyglet

from app.views.universe_view import UniverseView
from engine import Universe
from engine.command import TickCommand, SetCellCommand
from engine.managers.app_manager import AppManager


class UniverseManager:
    def __init__(
            self,
            app_manager: AppManager,
            model: Universe,
    ):
        self._invoker = app_manager
        self._model = model
        self._view = UniverseView(
            self._model,
            viewport_width=app_manager.view.width,
            viewport_height=app_manager.view.height
        )

        self._model.push_handlers(self._view)
        app_manager.view.push_handlers(self)
        app_manager.view.register_component(self._view)

        self._ticking = False

    @property
    def model(self):
        return self._model

    @property
    def view(self):
        return self._view

    def on_mouse_press(self, x, y, button, modifiers):
        value = None

        if button == pyglet.window.mouse.LEFT:
            value = True
        elif button == pyglet.window.mouse.RIGHT:
            value = False

        if value is not None:
            self._invoker.set_command(
                SetCellCommand(
                    self._model,
                    self._view,
                    x, y,
                    value
                )
            )

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.SPACE and not self._ticking:
            self._invoker.set_command(
                TickCommand(
                    self._model
                )
            )
        elif key == pyglet.window.key.ENTER:
            self._loop_model()
        elif key == pyglet.window.key.W:
            pyglet.clock.schedule_interval(
                self._scroll, 1/60, direction_y=1
            )
        elif key == pyglet.window.key.A:
            pyglet.clock.schedule_interval(
                self._scroll, 1/60, direction_x=-1
            )
        elif key == pyglet.window.key.S:
            pyglet.clock.schedule_interval(
                self._scroll, 1/60, direction_y=-1
            )
        elif key == pyglet.window.key.D:
            pyglet.clock.schedule_interval(
                self._scroll, 1/60, direction_x=1
            )

    def on_key_release(self, key, modifiers):
        if key in (
                pyglet.window.key.W,
                pyglet.window.key.A,
                pyglet.window.key.S,
                pyglet.window.key.D
        ):
            pyglet.clock.unschedule(self._scroll)

    def _loop_model(self):
        def tick_command(dt):
            if not self._ticking:
                pyglet.clock.unschedule(tick_command)
            self._invoker.set_command(TickCommand(self._model))

        self._ticking = not self._ticking
        if self._ticking:
            pyglet.clock.schedule_interval(
                tick_command,
                0.1,
            )

    def _scroll(self, dt=None, direction_x: int = 0, direction_y: int = 0):
        self._view.origin = (
            self._view.origin[0] + direction_x * self._view.cell_size[0],
            self._view.origin[1] + direction_y * self._view.cell_size[1]
        )
