from __future__ import annotations
from inspect import isclass

import pyglet

from engine.command import Command, Invoker, TickCommand, SetCellCommand
from engine.save_manager import SaveManager


class UniverseController(Invoker):
    def __init__(
            self,
            app
    ):
        self.app = app
        self.universe = app.model
        self.view = app.model_view

        self.key_map = {
            "on_key_press": {
                pyglet.window.key.BACKSPACE: {
                    0: {
                        "type": pyglet.clock.schedule_interval,
                        "args": (self._revoke, 0.05)
                    }
                },
                pyglet.window.key.SPACE: {
                    0: {
                        "type": TickCommand,
                        "args": (self.universe,)
                    },
                },
                pyglet.window.key.ENTER: {
                    0: {
                        "type": self._loop_model
                    }
                },
                pyglet.window.key.W: {
                    0: {
                        "type": pyglet.clock.schedule_interval,
                        "args": (self._scroll, 1/60),
                        "kwargs": {"direction_y": 1}
                    }
                },
                pyglet.window.key.A: {
                    0: {
                        "type": pyglet.clock.schedule_interval,
                        "args": (self._scroll, 1/60),
                        "kwargs": {"direction_x": -1}
                    }
                },
                pyglet.window.key.S: {
                    0: {
                        "type": pyglet.clock.schedule_interval,
                        "args": (self._scroll, 1/60),
                        "kwargs": {"direction_y": -1}
                    },
                    pyglet.window.key.MOD_CTRL: {
                        "type": self._save_model
                    }
                },
                pyglet.window.key.D: {
                    0: {
                        "type": pyglet.clock.schedule_interval,
                        "args": (self._scroll, 1/60, ),
                        "kwargs": {"direction_x": 1}
                    }
                },
                pyglet.window.key.L: {
                    pyglet.window.key.MOD_CTRL: {
                        "type": self._load_model
                    }
                }
            },
            "on_key_release": {
                pyglet.window.key.BACKSPACE: {
                    0: {
                        "type": pyglet.clock.unschedule,
                        "args": (self._revoke, )
                    }
                },
                pyglet.window.key.W: {
                    0: {
                        "type": pyglet.clock.unschedule,
                        "args": (self._scroll, )
                    }
                },
                pyglet.window.key.A: {
                    0: {
                        "type": pyglet.clock.unschedule,
                        "args": (self._scroll, )
                    }
                },
                pyglet.window.key.S: {
                    0: {
                        "type": pyglet.clock.unschedule,
                        "args": (self._scroll, )
                    }
                },
                pyglet.window.key.D: {
                    0: {
                        "type": pyglet.clock.unschedule,
                        "args": (self._scroll, )
                    }
                },
            },
            "on_mouse_press": {
                pyglet.window.mouse.LEFT: {
                    0: {
                        "type": SetCellCommand,
                        "args": (self.universe, self.view),
                        "kwargs": {"value": True}
                    }
                },
                pyglet.window.mouse.RIGHT: {
                    0: {
                        "type": SetCellCommand,
                        "args": (self.universe, self.view),
                        "kwargs": {"value": False}
                    }
                }
            }
        }

        self._ticking = False

    def create_command(
            self,
            event: str,
            key: pyglet.window.key,
            modifier: pyglet.window.key,
            *args, **kwargs
    ):
        command_event = self.key_map.get(event)
        # In pyglet, when no modifier is pressed, the variable has the value of 16
        # Thus, the modifier is corrected, so I can use 0 in key_map, which is more
        # understandable for me.
        modifier = modifier - 16
        if command_event:
            command_info = command_event.get(key, {}).get(modifier)
            if command_info:
                args = (*command_info.get("args", ()), *args)
                kwargs = {**kwargs, **command_info.get("kwargs", {})}
                command = command_info["type"]

                if isclass(command) and issubclass(command, Command):
                    self.set_command(command(*args, **kwargs))
                else:
                    command(*args, **kwargs)

    def _loop_model(self):
        def tick_command(dt):
            if not self._ticking or not self.app.enabled:
                pyglet.clock.unschedule(tick_command)
                return
            self.set_command(TickCommand(self.universe))

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
