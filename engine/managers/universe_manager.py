import pyglet


class UniverseManager:
    def __init__(self, parent, model, view):
        self.parent = parent
        self.model = model
        self.view = view

        self.parent.register_component(self)

    def _loop_model(self):
        def tick_command(dt):
            if not self._ticking or not self.app.enabled:
                pyglet.clock.unschedule(tick_command)
                return
            parent.set_command(TickCommand(self.universe))

        self._ticking = not self._ticking
        if self._ticking:
            pyglet.clock.schedule_interval(
                tick_command,
                0.1,
            )

    def _scroll(self, dt=None, direction_x: int = 0, direction_y: int = 0):
        self.view.origin = (
            self.view.origin[0] + direction_x * self.view.cell_size[0],
            self.view.origin[1] + direction_y * self.view.cell_size[1]
        )

    def _save_model(self):
        sm = SaveManager(self.app)
        sm.scenario = sm.save_scenario()
        sm.run()

    def _load_model(self):
        sm = SaveManager(self.app)
        sm.scenario = sm.load_scenario()
        sm.run()
