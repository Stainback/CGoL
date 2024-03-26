import pyglet

from app.app_component import AppComponent
import app.gui as gui


class SaveWidget(pyglet.gui.WidgetBase):
    def __init__(
            self,
            batch: pyglet.graphics.Batch,
            x: int, y: int,
    ):
        self._group = pyglet.graphics.Group(order=0)

        self._info = gui.WidgetTextComponent(
            batch=batch,
            widget_group=self._group,
            x=x, y=y,
            anchor_y="top",
            text_color=(0, 255, 0, 255)
        )

        self._form = gui.WidgetTextFormComponent(
            batch=batch,
            widget_group=self._group,
            x=x, y=y,
            anchor_y="top"
        )

        self._background = gui.WidgetBackgroundComponent(
            batch=batch,
            widget_group=self._group,
            content=self._form
        )

        super().__init__(
            x=0, y=0,
            width=0,
            height=0
        )

    def _check_hit(self, x, y):
        return (
            self._form.x < x < self._form.x + self._form.width and
            self._form.y - self._form.height < y < self._form.y
        )

    def on_mouse_press(self, x, y, button, modifiers):
        print(x,y)
        if self._check_hit(x, y):
            print(1)
            self._form.enable(x, y, button, modifiers)
        else:
            self._form.disable()

    def on_text(self, text_input: str):
        filename = self._form.process_text_input(text_input)
        if filename:
            self.dispatch_event("on_text_commit", filename)
            self._form.disable()
            self._form.hide()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self._form.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text_motion(self, motion):
        self._form.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        self._form.on_text_motion_select(motion)

    def show(self):
        self._group.visible = True

    def hide(self):
        self._group.visible = False


class LoadWidget(pyglet.gui.WidgetBase):
    _page_capacity = 5

    def __init__(
            self,
            batch,
            x: int,
            y: int,
            options_list: list[str] = None,
    ):
        self._group = pyglet.graphics.Group(order=1)
        self._options_list = options_list

        self._info = gui.WidgetTextComponent(
            batch=batch,
            widget_group=self._group,
            x=x, y=y,
            anchor_y="top",
            text="Pick a savefile to continue loading...",
            text_color=(0, 255, 0, 255)
        )

        self._options = gui.WidgetTextComponent(
            batch=batch,
            widget_group=self._group,
            x=x, y=y - self._info.height - 20,
            anchor_y="top",
            text="\n".join(
                [option.upper()
                 for option in self._options_list[:min(
                    self._page_capacity, len(self._options_list)
                )]]
            ),
            text_color=(0, 0, 0, 255)
        )

        self._background = gui.WidgetBackgroundComponent(
            batch=batch,
            widget_group=self._group,
            content=self._options
        )

        total_height = self._options.height + self._info.height + 20

        super().__init__(
            x=x, y=y - total_height,
            width=max(self._info.width, self._background.width),
            height=total_height
        )
        self._item_height = self._options.height / len(self._options_list)

    def _check_hit(self, x, y):
        return (
            self._options.x < x < self._options.x + self._options.width and
            self._options.y - self._options.height < y < self._options.y
        )

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            filename = self._options_list[
                int(
                    (self._options.y - y) //
                    (self._options.height / len(self._options_list))
                )
            ]
            print(filename)
            self.dispatch_event("on_text_commit", filename)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def show(self):
        self._group.visible = True

    def hide(self):
        self._group.visible = False


SaveWidget.register_event_type("on_text_commit")
LoadWidget.register_event_type("on_text_commit")


class SaveManagerView(AppComponent):
    def __init__(self, manager):
        self._manager = manager
        self._batch = pyglet.graphics.Batch()

        self._gui = {
            "savefile_form": SaveWidget(
                batch=self._batch,
                x=32, y=self._manager._app._view.height - 32,
            ),
            "savefile_list": LoadWidget(
                batch=self._batch,
                x=32, y=self._manager._app._view.height,
                options_list=self._manager._save_list,
            ),
        }

        for element in self._gui.values():
            element.hide()

    def draw(self):
        self._batch.draw()

    def enable_gui_element(self, element_name: str, *args, **kwargs):
        element = self._gui.get(element_name)
        if element:
            element.show()
            self._manager._app._view.frame.add_widget(element)
            return element
        else:
            raise ValueError(f"No {element_name} GUI template exists.")

    def disable_gui_element(self, element_name: str):
        element = self._gui.get(element_name)
        if element:
            element.hide()
            self._manager._app._view.frame.remove_widget(element)
        else:
            raise ValueError(f"No {element_name} GUI template exists.")
