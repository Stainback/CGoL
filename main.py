import pyglet

import app_config
from app import App


WINDOW_WIDTH, WINDOW_HEIGHT = 900, 594


def benchmark():
    return {
        (i, j)
        for i in range(WINDOW_WIDTH // 18)
        for j in range(WINDOW_HEIGHT // 18)
    }


if __name__ == "__main__":
    # config = benchmark()
    config = {(0, 0), (49, 32), (0, 32), (49, 0)}

    app = App(
        viewport_size=(WINDOW_WIDTH, WINDOW_HEIGHT),
        configuration=config,
        caption="CONWAY'S GAME OF LIFE"
    )
    pyglet.app.run()
