import pyglet

from app import App


if __name__ == "__main__":
    pyglet.resource.path = ["resources"]
    pyglet.resource.reindex()

    config = {
        (5, 15), (6, 15), (7, 15), (7, 16), (6, 17)
    }

    app = App(1020, 1020, configuration=config)
    pyglet.app.run()
