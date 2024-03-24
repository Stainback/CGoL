import pyglet

from app.app_component import AppComponent
from app.gui import TextFormWidget, OptionsListWidget


class SaveManagerView(AppComponent):
    def __init__(self, manager):
        self._manager = manager
        self._batch = pyglet.graphics.Batch()

        self._gui = {
            "savefile_list": OptionsListWidget(
                batch=self._batch,
                x=32, y=32,
                options_list=self._manager._save_list,
            ),
        }

        for element in self._gui.values():
            element.hide()

    def draw(self):
        self._batch.draw()

    def enable_gui_element(self, element_name: str, *args, **kwargs):
        element = self._gui.get(element_name)
        if element:
            element.show()
            self._manager._app._view.frame.add_widget(element)
            return element
        else:
            raise ValueError(f"No {element_name} GUI template exists.")

    def disable_gui_element(self, element_name: str):
        element = self._gui.get(element_name)
        if element:
            self._manager._app._view.remove_widget(element)
        else:
            raise ValueError(f"No {element_name} GUI template exists.")
