import pyglet

from app.app_component import AppComponent
from app.gui import TextFormWidget, OptionsListWidget, Text


class SaveManagerView(AppComponent):
    def __init__(self, controller):
        self._controller = controller
        self._app = self._controller.app
        self._batch = pyglet.graphics.Batch()

        self._templates = {
            "text_form": {
                "type": TextFormWidget,
                "kwargs": {
                    "x": 20,
                    "y": self._app.height - 40,
                    "text": "Enter name for new savefile"
                }
            },
            "button_overwrite_true": {
                "type": pyglet.gui.PushButton,
                "kwargs": {

                }
            },
            "button_overwrite_false": {
                "type": pyglet.gui.PushButton,
                "kwargs": {}
            },
            "info_label_overwrite": {
                "type": Text,
                "kwargs": {
                    "x": 20,
                    "y": self._app.height - 80,
                    "text": MESSAGE_ON_OVERWRITE
                }
            },
            "info_label_filename_validation_error": {
                "type": Text,
                "kwargs": {
                    "x": 20,
                    "y": self._app.height - 80,
                    "text": MESSAGE_ON_SAVE_FILENAME_VALIDATION_ERROR
                }
            },
            "info_label_save_success": {
                "type": Text,
                "kwargs": {
                    "x": 20,
                    "y": self._app.height - 80,
                    "text": MESSAGE_ON_SAVE_SUCCESS
                }
            },
            "info_label_load_success": {
                "type": Text,
                "kwargs": {
                    "x": 20,
                    "y": self._app.height - 80,
                    "text": MESSAGE_ON_LOAD_SUCCESS
                }
            },
            "info_label_save_failure": {
                "type": Text,
                "kwargs": {
                    "x": 20,
                    "y": self._app.height - 80,
                    "text": MESSAGE_ON_SAVE_FAILURE
                }
            },
            "info_label_load_failure": {
                "type": Text,
                "kwargs": {
                    "x": 20,
                    "y": self._app.height - 80,
                    "text": MESSAGE_ON_LOAD_FAILURE
                }
            },
            "file_list": {
                "type": OptionsListWidget,
                "kwargs": {
                    "x": 20,
                    "y": 20,
                    "options_list": options_list
                }
            }
        }
        self._gui = {}

    def draw(self):
        self._batch.draw()

    def create_gui_element(self, element_name: str):
        template = self._templates.get(element_name)
        if template:
            element = template["type"](
                batch=self._batch,
                **template["kwargs"]
            )
            if issubclass(element.__class__, pyglet.gui.WidgetBase):
                self._app.frame.add_widget(element)
            self._gui[element_name] = element
            return element
        else:
            raise ValueError(f"No {element_name} GUI template exists.")

    def delete_gui_element(self, element_name: str):
        element = self._gui.pop(element_name)
        self._app.frame.remove_widget(element)
