import os
import json

from app_config import (PATH_SAVES,
                        MESSAGE_ON_OVERWRITE,
                        MESSAGE_ON_SAVE_SUCCESS,
                        MESSAGE_ON_LOAD_SUCCESS,
                        MESSAGE_ON_LOAD_FAILURE,
                        MESSAGE_ON_SAVE_FILENAME_VALIDATION_ERROR)
from app.app_block import AppBlock
from app.save_manager_gui import SaveManagerGUI


class SaveManager:
    _path = PATH_SAVES

    def __init__(self, app):
        self.app = app
        self.model = app.model
        self.model_view = app.model_view
        self.save_list = [
            os.path.splitext(path)[0] for path in os.listdir(path=self._path)
        ]
        self.view = SaveManagerGUI(self.app, self.save_list)
        self.data = {
            "configuration": list(self.model.alive),
            "origin": self.model_view.origin
        }
        self.scenario = None
        self.filename = None

    def save(self, filename: str):
        with open(
            os.path.join(self._path, filename + ".json"),
            "w"
        ) as save_file:
            json.dump(self.data, save_file, indent=4)
            print(f"{self} - Universe has been saved as {filename}.")

    def load(self, filename: str):
        with open(
                os.path.join(self._path, filename + ".json"),
                "r"
        ) as save_file:
            self.data = json.load(save_file)
            self.model.alive = {
                tuple(item) for item in self.data["configuration"]
            }
            self.model_view.origin = tuple(self.data["origin"])
            print(f"{self} - {filename} has been loaded.")

    def is_valid(self, filename):
        return True

    def is_exists(self, filename):
        return filename in self.save_list

    def run(self):
        try:
            self.scenario.__next__()
        except StopIteration:
            self.scenario = None

    def save_scenario(self):
        with AppBlock(self.app, self.view) as block:
            text_form = self.view.create_gui_element("text_form")
            text_form.push_handlers(self)

            while True:
                yield
                if not self.is_exists(self.filename):
                    self.save(self.filename)
                    self.view.delete_gui_element("text_form")
                    break

    def load_scenario(self):
        with AppBlock(self.app, self.view) as block:
            file_list = self.view.create_gui_element("file_list")
            file_list.push_handlers(self)

            while True:
                yield
                if self.is_exists(self.filename):
                    self.load(self.filename)
                    self.view.delete_gui_element("file_list")
                    break

    def on_text_commit(self, filename):
        if self.is_valid(filename):
            self.filename = filename
            self.run()
