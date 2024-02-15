import pyglet

from app import App


WINDOW_WIDTH, WINDOW_HEIGHT = 900, 900


def benchmark():
    return {
        (i, j) for i in range(50) for j in range(50)
    }


if __name__ == "__main__":
    pyglet.resource.path = ["resources"]
    pyglet.resource.reindex()

    config = benchmark()

    app = App(WINDOW_WIDTH, WINDOW_HEIGHT, configuration=config)
    pyglet.app.run()
