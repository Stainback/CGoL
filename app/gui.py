from __future__ import annotations

import pyglet

from app_config import FONT_DEFAULT, COLOR_DEFAULT, COLOR_BACKGROUND


class WidgetTextComponent:
    def __init__(
            self,
            batch: pyglet.graphics.Batch,
            widget_group: pyglet.graphics.Group,
            x: int, y: int,
            anchor_x: str = "left", anchor_y: str = "bottom",
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
            anchor_x=anchor_x, anchor_y=anchor_y,
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
    def anchor(self) -> tuple[str, str]:
        return self._layout.anchor_x, self._layout.anchor_y

    @property
    def text(self) -> str:
        return self._doc.text

    @text.setter
    def text(self, text: str):
        self._doc.text = text

        lines = text.splitlines()
        # pt to px
        self._width = self.font_size / 1.25 * len(max(lines, key=len))

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

        self._anchor_padding_x = 0
        self._anchor_padding_y = 0

        if content.anchor[0] == "right":
            self._anchor_padding_x = content.width
        elif content.anchor[0] == "center":
            self._anchor_padding_x = 0.5 * content.width

        if content.anchor[1] == "top":
            self._anchor_padding_y = content.height
        elif content.anchor[1] == "center":
            self._anchor_padding_y = 0.5 * content.height

        self._outline = pyglet.shapes.Rectangle(
            x=content.x - self._padding - self._anchor_padding_x,
            y=content.y - self._padding - self._anchor_padding_y,
            width=content.width + (2 * self._padding),
            height=content.height + (2 * self._padding),
            color=color[:3],
            batch=batch,
            group=self._group
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
