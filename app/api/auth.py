from flask import Blueprint

from app.models.user import User

auth = Blueprint('/auth', __name__)


# @auth.route('/regist')
# def regist():
#     return False

# @auth.route('/login')
# def login():
#     return False
    