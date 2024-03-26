import os
import json
import pyglet

from app_config import PATH_SAVES
from app.app_block import AppBlock
from app.views.save_view import SaveManagerView
from engine.managers.app_manager import AppManager
from engine.managers.universe_manager import UniverseManager


class SaveManager:
    _path = PATH_SAVES

    def __init__(
            self,
            app_manager: AppManager,
            model_manager: UniverseManager,
    ):
        self._app = app_manager
        self._model = model_manager.model
        self._model_view = model_manager.view
        self._save_list = [
            os.path.splitext(path)[0] for path in os.listdir(path=self._path)
        ]
        self._view = SaveManagerView(self)
        self._scenario = None
        self._filename = None

        self._app.view.push_handlers(self)
        self._app.view.register_component(self._view)

    def on_key_press(self, key, modifiers):
        if (key == pyglet.window.key.S
                and modifiers & pyglet.window.key.MOD_CTRL):
            self._scenario = self.save_scenario()
        elif (key == pyglet.window.key.L
              and modifiers & pyglet.window.key.MOD_CTRL):
            self._scenario = self.load_scenario()

        if self._scenario:
            self.run()

    def on_text_commit(self, filename):
        if self._is_valid(filename):
            self._filename = filename
            self.run()

    def _save(self, filename: str):
        data = {
            "configuration": list(self._model.alive),
            "origin": self._model_view.origin
        }

        with open(
            os.path.join(self._path, filename + ".json"),
            "w"
        ) as save_file:
            json.dump(data, save_file, indent=4)
            print(f"{self} - Universe has been saved as {filename}.")

    def _load(self, filename: str):
        with open(
                os.path.join(self._path, filename + ".json"),
                "r"
        ) as save_file:
            data = json.load(save_file)
            self._model.alive = {
                tuple(item) for item in data["configuration"]
            }
            self._model_view.origin = tuple(data["origin"])
            print(f"{self} - {filename} has been loaded.")

    def _is_valid(self, filename):
        return True

    def _is_exists(self, filename):
        return filename in self._save_list

    def run(self):
        if self._scenario:
            try:
                self._scenario.__next__()
            except StopIteration:
                self._scenario = None

    def save_scenario(self):
        with AppBlock(self._app, self._view) as block:
            text_form = self._view.enable_gui_element("savefile_form")
            text_form.push_handlers(self)

            while True:
                yield
                if not self._is_exists(self._filename):
                    self._save(self._filename)
                    self._view.disable_gui_element("savefile_form")
                    break

    def load_scenario(self):
        with AppBlock(self._app, self._view) as block:
            file_list = self._view.enable_gui_element("savefile_list")
            file_list.push_handlers(self)

            while True:
                yield
                if self._is_exists(self._filename):
                    self._load(self._filename)
                    self._view.disable_gui_element("savefile_list")
                    break


