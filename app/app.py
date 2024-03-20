from __future__ import annotations

import pyglet

from engine.universe import Universe
from engine.universe_controller import UniverseController
from app.universe_view import View
from app.app_component import AppComponent


class TestFrame(pyglet.gui.Frame):
    def remove_widget(self, widget):
        super().remove_widget(widget)
        print(f"{self} - widget removed")

    def on_mouse_press(self, x, y, buttons, modifiers):
        print(f"{self} - on_mouse_press")
        try:
            super().on_mouse_press(x, y, buttons, modifiers)
        except RuntimeError:
            print(f"{self} - RuntimeError: to be omitted")
        print(f"{self} - finished on_mouse_press")


class App(pyglet.window.Window):
    def __init__(
            self,
            viewport_size: tuple[int, int],
            configuration: set[tuple] = None,
            caption: str = "caption"
    ):
        super().__init__(*viewport_size)
        self.set_location(40, 40)
        self.set_caption(caption)
        self._frame = TestFrame(self)
        self._graphic_components = []

        self._model = Universe(configuration)
        self._model_view = View(self)
        self._controller = UniverseController(self)

        self._model.push_handlers(self._model_view)

        self.register_component(self._model_view)

        self.enabled = True

    @property
    def frame(self):
        return self._frame

    @property
    def model(self):
        return self._model

    @property
    def controller(self):
        return self._controller

    @property
    def model_view(self):
        return self._model_view

    def register_component(self, component: list | AppComponent):
        if isinstance(component, list):
            self._graphic_components += component
        elif isinstance(component, AppComponent):
            self._graphic_components.append(component)

    def withdraw_component(self, component: list | AppComponent):
        if isinstance(component, list):
            for item in component:
                self._graphic_components.remove(item)
        elif isinstance(component, AppComponent):
            self._graphic_components.remove(component)

    def on_draw(self):
        self.clear()
        for component in self._graphic_components:
            component.draw()

    def on_mouse_press(self, x, y, key, modifiers):
        if self.enabled:
            self.controller.create_command(
                "on_mouse_press",
                key,
                modifiers,
                x, y,
            )

    def on_key_press(self, key, modifiers):
        if self.enabled:
            self.controller.create_command(
                event="on_key_press",
                key=key,
                modifier=modifiers
            )

    def on_key_release(self, key, modifiers):
        if self.enabled:
            self.controller.create_command(
                event="on_key_release",
                key=key,
                modifier=modifiers
            )
