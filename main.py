import pyglet

from app import App


WINDOW_WIDTH, WINDOW_HEIGHT = 1620, 810


def benchmark():
    return {
        (i, j)
        for i in range(WINDOW_WIDTH // 18)
        for j in range(WINDOW_HEIGHT // 18)
    }


if __name__ == "__main__":
    pyglet.resource.path = ["resources"]
    pyglet.resource.reindex()

    # config = benchmark()
    config = {(0, 0), (49, 32), (0, 32), (49, 0)}
    # config = None

    app = App(WINDOW_WIDTH, WINDOW_HEIGHT, configuration=config)
    pyglet.app.run()
