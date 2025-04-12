"""
Application initialization module.
This module sets up the Flask application and its extensions.
"""

# Import path functionality with alias to avoid naming conflicts
from os import path as PA

# Import required Flask modules and extensions
from flask import Flask
from flask_bootstrap import Bootstrap

# Get the absolute path of the directory containing this file
# This is useful for handling file paths across different operating systems
basedir = PA.abspath(PA.dirname(__file__))

# Initialize Flask application instance
# template_folder='templates' tells Flask where to find the HTML templates
app = Flask(__name__, template_folder='templates')

# Initialize Flask-Bootstrap extension
# This provides Bootstrap integration for the Flask application
Bootstrap(app)

# Import views after app initialization to avoid circular imports
from app import views


# Set the secret key for session management and CSRF protection
# WARNING: In production, this should be loaded from environment variables
app.secret_key = 'AAO$&!|0wkamvVia0?n$NqIRVWOG'
