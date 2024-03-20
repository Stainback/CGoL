import pyglet

from app_config import WINDOW_WIDTH, WINDOW_HEIGHT
from app.views.app_view import View
from engine.managers.app_manager import Manager


def benchmark():
    return {
        (i, j)
        for i in range(WINDOW_WIDTH // 18)
        for j in range(WINDOW_HEIGHT // 18)
    }


if __name__ == "__main__":
    # config = benchmark()
    config = {
        (0, 0),
        (WINDOW_WIDTH // 18 - 1, WINDOW_HEIGHT // 18 - 1),
        (0, WINDOW_HEIGHT // 18 - 1),
        (WINDOW_WIDTH // 18 - 1, 0)
    }

    app_view = View(
        viewport_size=(WINDOW_WIDTH, WINDOW_HEIGHT),
        configuration=config,
        caption="CONWAY'S GAME OF LIFE"
    )
    app_manager = Manager(app_view)
    app_view.push_handlers(app_manager)

    pyglet.app.run()
