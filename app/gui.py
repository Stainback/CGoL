import pyglet

from app_config import FONT_DEFAULT, COLOR_DEFAULT, COLOR_BACKGROUND


class TextFormWidget(pyglet.gui.TextEntry):
    def __init__(
            self,
            batch,
            x: int,
            y: int,
            color: tuple[int] = COLOR_BACKGROUND,
            text: str = "",
            text_color: tuple[int] = COLOR_DEFAULT,
            font_name: str = FONT_DEFAULT,
            font_size: int = 16,
            group=None
    ):
        super().__init__(
            text=text,
            x=x,
            y=y,
            width=max(200, len(text) * font_size),
            color=color,
            text_color=text_color,
            batch=batch,
            group=group
        )

        self._doc.set_style(
            start=0,
            end=0,
            attributes={
                "font_name": font_name,
                "font_size": font_size
            }
        )

    def on_commit(self, text):
        super().on_commit(text)
        self.dispatch_event("on_text_commit", text)


class OptionsListWidget(pyglet.gui.WidgetBase):
    _item_gap = 2
    _page_capacity = 5

    def __init__(
            self,
            batch,
            x: int,
            y: int,
            color: tuple[int] = COLOR_BACKGROUND,
            options_list: list[str] = None,
            text_color: tuple[int] = COLOR_DEFAULT,
            font_name: str = FONT_DEFAULT,
            font_size: int = 16,
            group=None
    ):
        self._doc = pyglet.text.document.FormattedDocument(
            "\n".join(options_list)
        )
        self._doc.set_style(
            start=0,
            end=len(self._doc.text),
            attributes={
                "font_name": font_name,
                "font_size": font_size,
                "color": text_color,
            }
        )
        font = self._doc.get_font(0)
        height = ((font.ascent - font.descent + self._item_gap) *
                  min(len(options_list), self._page_capacity))
        width = max(
            200, max(map(lambda item: len(item), options_list)) * font_size
        )

        bg_group = pyglet.graphics.Group(order=0, parent=group)
        fg_group = pyglet.graphics.Group(order=1, parent=group)

        self._outline = pyglet.shapes.Rectangle(
            x - self._item_gap, y - self._item_gap,
            width + (2 * self._item_gap),
            height + (2 * self._item_gap), color[:3],
            batch, bg_group
        )
        self._outline.opacity = color[3]

        self._layout = pyglet.text.layout.TextLayout(
            self._doc, width, height,
            multiline=True, batch=batch,
            group=fg_group
        )
        self._layout.x = x
        self._layout.y = y

        super().__init__(x, y, width, height)

        self.options_list = options_list
        self._item_height = self._height / len(self.options_list)
        self._right_x = self._x + self._width
        self._upper_y = self._y + self._height

    def _check_hit(self, x, y):
        return (self._x < x < self._right_x
                and self._y < y < self._upper_y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            item = self.options_list[
                int((self._upper_y - y) // self._item_height)
            ]
            self.dispatch_event("on_text_commit", item)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass


class Text(pyglet.text.Label):
    _padding = 2

    def __init__(
            self,
            batch,
            x: int, y: int,
            color: tuple[int] = COLOR_BACKGROUND,
            text: str = "TEXT PLACEHOLDER",
            text_color: tuple[int] = COLOR_DEFAULT,
            font_name=FONT_DEFAULT,
            font_size: int = 16,
            group=None
    ):
        super().__init__(
            text=text,
            font_name=font_name,
            font_size=font_size,
            color=text_color,
            x=x, y=y,
            batch=batch,
            group=group
        )

        font = self.document.get_font(0)
        height = font.ascent - font.descent
        width = max(
            200, len(text) * font_size
        )

        bg_group = pyglet.graphics.Group(order=0, parent=group)

        self._outline = pyglet.shapes.Rectangle(
            x - self._padding, y - self._padding,
            width + (2 * self._padding),
            height + (2 * self._padding), color[:3],
            batch, bg_group
        )
        self._outline.opacity = color[3]


TextFormWidget.register_event_type("on_text_commit")
OptionsListWidget.register_event_type("on_text_commit")