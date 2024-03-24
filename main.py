import pyglet

from app_config import WINDOW_WIDTH, WINDOW_HEIGHT
from engine import Universe
from engine.managers.app_manager import AppManager
from engine.managers.save_manager import SaveManager
from engine.managers.universe_manager import UniverseManager


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

    app_manager = AppManager(
        viewport_size=(WINDOW_WIDTH, WINDOW_HEIGHT),
        caption="CONWAY'S GAME OF LIFE"
    )

    universe = Universe(config)
    universe_manager = UniverseManager(
        app_manager, universe
    )

    save_manager = SaveManager(
        app_manager, universe_manager
    )

    pyglet.app.run()
