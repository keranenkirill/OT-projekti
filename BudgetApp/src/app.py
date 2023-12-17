from views.app_view import Application  # pylint: disable=import-error

if __name__ == "__main__":
    """
    Entry point for the Budget App.

    This script initializes the main application window using the 'Application' class
    from the 'app_view' module. It loads the login view using the controller
    and runs the application.

    Usage:
    - Run this script to launch the Budget App.

    """
    app = Application("Budget App")
    app.controller.load_login_view()

    app.run()
