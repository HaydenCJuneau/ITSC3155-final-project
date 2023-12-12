"""
__init__.py for the routes folder
This file helps to register blueprint objects.
Blueprints are modules that allow flask to register routes over many files. 
Each python file in this folder is a module that defines some routes externally. 
In app.py, we gather all the blueprints defined here and register them with the app.
"""

# src/__init__.py
from flask import Blueprint

# Create a blueprint for route modules to import and use
users_bp = Blueprint('users', __name__)
posts_bp = Blueprint('posts', __name__)


# Import all route modules
from . import users
from . import posts
