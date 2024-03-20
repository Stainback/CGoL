from __future__ import annotations
from inspect import isclass

import pyglet

from engine.command import Command, Invoker, TickCommand, SetCellCommand


class Manager(Invoker):
    def __init__(
            self,
            app
    ):
        self.app = app
        self._components = []

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

    def register_component(self, component):
        pass

    def withdraw_component(self, component):
        pass


    def on_mouse_press(self, x, y, key, modifiers):
        if self.enabled:
            self.controller.create_command(
                "on_mouse_press",
                key,
                modifiers,
                x, y,
            )

    def on_key_press(self, key, modifiers):
        if self.enabled:
            self.controller.create_command(
                event="on_key_press",
                key=key,
                modifier=modifiers
            )

    def on_key_release(self, key, modifiers):
        if self.enabled:
            self.controller.create_command(
                event="on_key_release",
                key=key,
                modifier=modifiers
            )

