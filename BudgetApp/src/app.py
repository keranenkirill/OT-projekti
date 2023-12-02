from views.app_view import Application  # pylint: disable=import-error

if __name__ == "__main__":

    app = Application("Budget App")
    app.controller.load_login_view()

    app.run()
