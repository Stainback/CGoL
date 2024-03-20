from __future__ import annotations

import pyglet

from app.views.app_view import AppView
from engine.command import Invoker


class AppManager(Invoker):
    def __init__(
            self,
            viewport_size: tuple[int, int],
            caption: str
    ):
        self._view = AppView(
            viewport_size=viewport_size, caption=caption
        )

        self._view.push_handlers(self)

    @property
    def view(self) -> AppView:
        return self._view

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.BACKSPACE:
            pyglet.clock.schedule_interval(self._revoke, 0.05)

    def on_key_release(self, key, modifiers):
        if key == pyglet.window.key.BACKSPACE:
            pyglet.clock.unschedule(self._revoke)
