import os
import json
import datetime

import tkinter as tk
from tkinter import filedialog

from engine.universe import Universe


class SaveManager:
    _path = "saves"

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller
        self.controller.push_handlers(self)

    def on_save(self):
        data = {
            "timestamp": datetime.datetime.now().timestamp(),
            "configuration": list(self.model.alive),
            "origin": self.controller.view.origin
        }

        with open(
            os.path.join(self._path, "test.json"),
            "w"
        ) as save_file:
            json.dump(data, save_file, indent=4)
            print("saved")

    def on_load(self):
        pass
