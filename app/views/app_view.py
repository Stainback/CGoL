from __future__ import annotations

import pyglet

from engine.models.universe_model import Universe
from engine.managers.universe_manager import UniverseController
from app.views.universe_view import View
from app.app_component import AppComponent


class View(pyglet.window.Window):
    def __init__(
            self,
            viewport_size: tuple[int, int],
            configuration: set[tuple] = None,
            caption: str = "caption"
    ):
        super().__init__(*viewport_size)
        self.set_location(40, 40)
        self.set_caption(caption)

        self._frame = pyglet.gui.Frame(self)
        self._components = []

    @property
    def frame(self):
        return self._frame

    def register_component(self, component: list | AppComponent):
        if isinstance(component, list):
            self._components += component
        elif isinstance(component, AppComponent):
            self._components.append(component)

    def withdraw_component(self, component: list | AppComponent):
        if isinstance(component, list):
            for item in component:
                self._components.remove(item)
        elif isinstance(component, AppComponent):
            self._components.remove(component)

    def on_draw(self):
        self.clear()
        for component in self._components:
            component.draw()
