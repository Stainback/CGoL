import pyglet

from app.app_component import AppComponent
import app.gui as gui


class TextFormWidget:
    pass


class OptionsListWidget(pyglet.gui.WidgetBase):
    _page_capacity = 5

    def __init__(
            self,
            batch,
            x: int,
            y: int,
            options_list: list[str] = None,
    ):
        self._group = pyglet.graphics.Group()
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
            item = self._options_list[
                int(
                    (self._options.y - y) //
                    (self._options.height / len(self._options_list))
                )
            ]
            print(item)
            self.dispatch_event("on_text_commit", item)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def show(self):
        self._group.visible = True

    def hide(self):
        self._group.visible = False


# TextFormWidget.register_event_type("on_text_commit")
OptionsListWidget.register_event_type("on_text_commit")


class SaveManagerView(AppComponent):
    def __init__(self, manager):
        self._manager = manager
        self._batch = pyglet.graphics.Batch()

        self._gui = {
            "savefile_list": OptionsListWidget(
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
