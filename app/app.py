import pyglet


class App(pyglet.window.Window):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
