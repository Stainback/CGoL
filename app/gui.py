from __future__ import annotations
from abc import abstractmethod

import pyglet

from app_config import FONT_DEFAULT, COLOR_DEFAULT, COLOR_BACKGROUND


class WidgetComponent:
    def __init__(
            self,
            batch: pyglet.graphics.Batch = None,
            order: int = 0,
            parent: pyglet.graphics.Group = None
    ):
        self._batch = batch if batch else pyglet.graphics.Batch()
        self._group = pyglet.graphics.Group(order=order, parent=parent)

    #region Abstract Methods
    @abstractmethod
    def x(self):
        pass

    @abstractmethod
    def y(self):
        pass

    @abstractmethod
    def width(self):
        pass

    @abstractmethod
    def height(self):
        pass
    #endregion

    def show(self) -> None:
        self._group.visible = True

    def hide(self) -> None:
        self._group.visible = False


class WidgetTextComponent(WidgetComponent):
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

        super().__init__(batch=batch, order=1, parent=widget_group)

        self._doc = pyglet.text.document.UnformattedDocument(text)
        self._doc.set_style(
            start=0, end=len(self._doc.text),
            attributes={
                "font_name": font_name,
                "font_size": font_size,
                "color": text_color,
            }
        )

        self._layout = pyglet.text.layout.TextLayout(
            document=self._doc,
            width=(self._doc.get_style("font_size") / 1.25 * len(max(self._doc.text.splitlines()))
                   if self._doc.text != "" else 1),
            height=None,
            x=x, y=y,
            anchor_x=anchor_x, anchor_y=anchor_y,
            multiline=True,
            batch=batch,
            group=self._group
        )

    #region Properties
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
    # endregion


class WidgetTextFormComponent(WidgetComponent):
    def __init__(
            self,
            batch: pyglet.graphics.Batch,
            widget_group: pyglet.graphics.Group,
            x: int, y: int,
            anchor_x: str = "left", anchor_y: str = "bottom",
            text: str = "",
            char_limit: int = 20,
            font_name: str = FONT_DEFAULT,
            font_size: int = 16,
            text_color: tuple[int, int, int, int] = COLOR_DEFAULT
    ):
        super().__init__(batch, order=1, parent=widget_group)

        self._doc = pyglet.text.document.UnformattedDocument(text)
        self._char_limit = char_limit
        self._doc.set_style(
            start=0,
            end=len(self._doc.text),
            attributes={
                "font_name": font_name,
                "font_size": font_size,
                "color": text_color,
            }
        )

        self._layout = pyglet.text.layout.IncrementalTextLayout(
            document=self._doc,
            width=self._doc.get_style("font_size") / 1.25 * self._char_limit,
            height=self._doc.get_style("font_size") * 1.33,
            x=x, y=y,
            anchor_x=anchor_x, anchor_y=anchor_y,
            batch=batch,
            group=self._group
        )

        self._caret = pyglet.text.caret.Caret(self._layout, self._batch)
        self._caret.visible = False
        self._focus = False

    #region Properties
    @property
    def x(self) -> int:
        return self._layout.x

    @property
    def y(self) -> int:
        return self._layout.y

    @property
    def width(self) -> int | float:
        return self._layout.width

    @property
    def height(self) -> int | float:
        return self._layout.height

    @property
    def anchor(self) -> tuple[str, str]:
        return self._layout.anchor_x, self._layout.anchor_y

    @property
    def text(self) -> str:
        return self._doc.text

    @text.setter
    def text(self, text: str) -> None:
        self._doc.text = text if len(text) <= self._char_limit else text[:self._char_limit]
    #endregion

    def enable(self, x, y, button, modifiers):
        self._focus = True
        self._caret.on_mouse_press(x, y, button, modifiers)

    def disable(self):
        self._focus = False

    def show(self):
        self._group.visible = True

    def hide(self):
        self._group.visible = False

    def process_text_input(self, text_input: str):
        if self._focus:
            # Commit on Enter/Return:
            if text_input in ('\r', '\n'):
                self.disable()
                return self.text
            self._caret.on_text(text_input)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._focus:
            self._caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text_motion(self, motion):
        if self._focus:
            self._caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self._focus:
            self._caret.on_text_motion_select(motion)


class WidgetBackgroundComponent(WidgetComponent):
    _padding = 2

    def __init__(
            self,
            batch: pyglet.graphics.Batch,
            widget_group: pyglet.graphics.Group,
            content,
            color: tuple[int] = COLOR_BACKGROUND
    ):
        super().__init__(batch, order=0, parent=widget_group)

        anchor_x_values = ["left", "center", "right"]
        anchor_y_values = ["bottom", "center", "top"]
        self._anchor_padding_x = 0.5 * anchor_x_values.index(content.anchor[0]) * content.width
        self._anchor_padding_y = 0.5 * anchor_y_values.index(content.anchor[1]) * content.height

        self._background = pyglet.shapes.Rectangle(
            x=content.x - self._padding - self._anchor_padding_x,
            y=content.y - self._padding - self._anchor_padding_y,
            width=content.width + (2 * self._padding),
            height=content.height + (2 * self._padding),
            color=color[:3],
            batch=self._batch,
            group=self._group
        )
        self._background.opacity = color[3]

    #region Properties
    @property
    def x(self):
        return self._background.x

    @property
    def y(self):
        return self._background.y

    @property
    def width(self):
        return self._background.width

    @property
    def height(self):
        return self._background.height
    #endregion


class WidgetButtonComponent:
    pass


class WidgetSliderComponent:
    pass
