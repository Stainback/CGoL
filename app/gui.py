from __future__ import annotations

import pyglet

from app_config import FONT_DEFAULT, COLOR_DEFAULT, COLOR_BACKGROUND


class WidgetTextComponent:
    def __init__(
            self,
            batch: pyglet.graphics.Batch,
            widget_group: pyglet.graphics.Group,
            x: int, y: int,
            text: str = "",
            font_name: str = FONT_DEFAULT,
            font_size: int = 16,
            text_color: tuple[int, int, int, int] = COLOR_DEFAULT
    ):
        self._batch = batch
        self._group = pyglet.graphics.Group(order=1, parent=widget_group)

        self._doc = pyglet.text.document.FormattedDocument()
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        self.text = text

        self._layout = pyglet.text.layout.TextLayout(
            document=self._doc, width=self._width, height=None,
            x=x, y=y,
            multiline=True, batch=batch,
            group=self._group
        )

    @property
    def x(self) -> int:
        return self._layout.x

    @property
    def y(self) -> int:
        return self._layout.y

    @property
    def width(self) -> int | float:
        return self._layout.content_width

    @property
    def height(self) -> int | float:
        return self._layout.content_height

    @property
    def text(self) -> str:
        return self._doc.text

    @text.setter
    def text(self, text: str):
        self._doc.text = text

        lines = text.splitlines()
        self._width = self.font_size / 1.25 * len(max(lines, key=len))                 # pt to px

        self._doc.set_style(
            start=0,
            end=len(self._doc.text),
            attributes={
                "font_name": self.font_name,
                "font_size": self.font_size,
                "color": self.text_color,
            }
        )


class WidgetBackgroundComponent:
    _padding = 2

    def __init__(
            self,
            batch: pyglet.graphics.Batch,
            widget_group: pyglet.graphics.Group,
            content,
            color: tuple[int] = COLOR_BACKGROUND
    ):
        self._group = pyglet.graphics.Group(order=0, parent=widget_group)
        self._outline = pyglet.shapes.Rectangle(
            content.x - self._padding, content.y - self._padding,
            content.width + (2 * self._padding),
            content.height + (2 * self._padding), color[:3],
            batch, self._group
        )
        self._outline.opacity = color[3]

    @property
    def x(self):
        return self._outline.x

    @property
    def y(self):
        return self._outline.y

    @property
    def width(self):
        return self._outline.width

    @property
    def height(self):
        return self._outline.height


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

        self._options = WidgetTextComponent(
            batch=batch,
            widget_group=self._group,
            x=x, y=y,
            text="\n".join([option.upper() for option in self._options_list]),
            text_color=(0, 0, 0, 255)
        )

        self._background = WidgetBackgroundComponent(
            batch=batch,
            widget_group=self._group,
            content=self._options
        )

        self._info = WidgetTextComponent(
            batch=batch,
            widget_group=self._group,
            x=x, y=self._background.y + self._background.height + 20,
            text="Pick a savefile to continue loading...",
            text_color=(0, 255, 0, 255)
        )

        super().__init__(
            x=x, y=y,
            width=max(self._info.width, self._background.width),
            height=self._background.height + self._info.height + 20
        )
        self._item_height = self._options.height / len(self._options_list)

    def _check_hit(self, x, y):
        return (
            self._options.x < x < self._options.x + self._options.width and
            self._options.y < y < self._options.y + self._options.height
        )

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            item = self._options_list[
                int(
                    (self._options.y + self._options.height - y) //
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
