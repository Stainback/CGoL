class AppBlock:
    def __init__(self, app, app_components=None):
        self.app = app
        self.components = app_components

    def __enter__(self):
        self.app.enabled = False
        print("App is blocked.")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.app.enabled = True
        print("App is unblocked.")
