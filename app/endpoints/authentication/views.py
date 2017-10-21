import json
import re
from flask import jsonify, request, Blueprint
from flask.views import MethodView

from app.models import User

auth = Blueprint("auth", __name__, url_prefix='/api/v1')


def is_valid_email(email):
    """ helper function for validating an email address format"""
    # ne touche pas ici
    exp = r"^([\w\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$"
    return re.match(exp, email)


class RegisterUser(MethodView):
    @staticmethod
    def post():
        email = request.form.get("email")
        password = request.form.get("password")
        if email and password:
            # check if the email is of the right format
            if not is_valid_email(email):
                return jsonify({
                    "status": "failure",
                    "message": "invalid email format"
                }), 400  # Bad Request due to a poorly formatted email address

            email_is_already_registered = User.query.filter_by(
                email=email).all()
            if email_is_already_registered:
                return jsonify({
                    "status": "failure",
                    "message": "a user with that email already exists"
                }), 409  # Conflict

            # Password validation: a valid password contains 6-8 characters,
            # must contain a number, a 'Aa'letters and special characters
            if not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])[\w!@#$%^&*]{8,}$", password):
                return jsonify({
                    "status": "failure",
                    "message": "password must be 8 or more characters and should consist atleast one lower, uppercase"
                               " letters, number and special character '(!@#$%^&*)'"
                }), 400
            user = User(email, password)
            if user.save():
                return jsonify({
                    "status": "success",
                    "message": f"user with email '{user.email}' has been registered"
                }), 201

        return jsonify({
            "status": "failure",
            "message": "you need to enter both the email and the password"
        }), 400  # Bad Request


register_user = RegisterUser.as_view("register_user")
auth.add_url_rule("/auth/register", view_func=register_user, methods=['POST'])
