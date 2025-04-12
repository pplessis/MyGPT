"""
Main application entry point for MyGPT web application.
This file serves as the application runner and imports the Flask application instance.
"""

# Import the Flask application instance from the app package
from app import app

if __name__ == '__main__':
    # Run the application in debug mode when executed directly
    app.run(debug=True)


## Run the app for Python web development
#if __name__ == '__main__':
#
#    # Bootstrap-Flask requires this line
#    bootstrap = Bootstrap5(app)
#    # Flask-WTF requires this line
#    csrf = CSRFProtect(app)
#