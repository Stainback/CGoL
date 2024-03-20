import os
import pyglet


pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

# PATHS
PATH_SAVES = "saves"
PATH_FONTS = os.path.join("resources", "fonts")

# IMAGES
IMG_CELL = pyglet.resource.image("images/cell.png")

# COLORS SHORTCUTS
COLOR_DEFAULT = (0, 0, 0, 255)
COLOR_BACKGROUND = (255, 255, 255, 255)
COLOR_CORRECT = (0, 255, 0, 255)
COLOR_INCORRECT = (255, 0, 0, 255)

# FONTS
FONT_DEFAULT = "Cutive Mono"

pyglet.font.add_directory(PATH_FONTS)

# MESSAGES
MESSAGE_ON_OVERWRITE = {
    "message": "Do you want to overwrite this save?",
    "color": COLOR_DEFAULT
}
MESSAGE_ON_SAVE_FILENAME_VALIDATION_ERROR = {
    "message": "Incorrect filename.",
    "color": COLOR_INCORRECT
}
MESSAGE_ON_SAVE_SUCCESS = {
    "message": "Saved successfully as",
    "color": COLOR_CORRECT
}
MESSAGE_ON_LOAD_SUCCESS = {
    "message": "successfully loaded.",
    "color": COLOR_CORRECT
}
MESSAGE_ON_SAVE_FAILURE = {
    "message": "During saving process, some errors occurred.",
    "color": COLOR_INCORRECT
}
MESSAGE_ON_LOAD_FAILURE = {
    "message": "During loading process, some errors occurred.",
    "color": COLOR_INCORRECT
}
