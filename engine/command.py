from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class Invoker:
    _history_capacity = 50
    _history = []

    def set_command(
            self,
            command: Command,
            delayed: bool = False
    ):
        if len(self._history) == self._history_capacity:
            self._history.pop(0)
        self._history.append(command)
        if not delayed:
            self._invoke()

    def _invoke(self):
        self._history[-1].execute()

    def _revoke(self, dt=None):
        if self._history:
            self._history[-1].undo()
            self._history.pop(-1)


class TickCommand(Command):
    def __init__(self, universe):
        self.model = universe
        self.state = universe.alive

    def execute(self):
        self.state = self.model.alive
        self.model.tick()

    def undo(self):
        self.model.alive = self.state


class SetCellCommand(Command):
    def __init__(
            self,
            model,
            view,
            abs_x: int,
            abs_y: int,
            value: bool
    ):
        self.model = model
        self.value = value
        self.x = (abs_x + view.origin[0]) // view.cell_size[0]
        self.y = (abs_y + view.origin[1]) // view.cell_size[1]

    def _debug_message(self):
        return (
            f"Cell at ({self.x}, {self.y}) has been "
            f"{'created' if self.value else 'destroyed'}."
        )

    def execute(self):
        print(self._debug_message())
        self.model.set_cells((self.x, self.y), self.value)

    def undo(self):
        print(self._debug_message())
        self.model.set_cells((self.x, self.y), not self.value)
