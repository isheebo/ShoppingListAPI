import json
import re
from flask import jsonify, request, Blueprint
from flask.views import MethodView

from app.models import User, BlacklistToken
from app.endpoints import parse_auth_header

auth = Blueprint("auth", __name__, url_prefix='/api/v1')


def is_valid_email(email):
    """ helper function for validating an email address format"""
    # ne touche pas ici
    exp = r"^([\w\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-z]{2,4}|[0-9]{1,3})(\]?)$"
    return re.match(exp, email)


# def parse_auth_header():
#     auth_header = request.headers.get("Authorization")
#     if auth_header:
#         # check if we have are using the JWT-Based Aunthentication mechanism
#         if len(auth_header.split()) != 2 or (auth_header.split()[0]).title() != "Bearer":
#             return jsonify({
#                 "status": "failure",
#                 "message": "Authentication Header is poorly formatted. The acceptable format is `Bearer <jwt_token>`"
#             }), 401
#         return auth_header.split()[1]
#     return jsonify({
#         "status": "failure",
#         "message": "Authorization header must be set for a successful request"
#     }), 401


class RegisterUser(MethodView):
    @staticmethod
    def post():
        email = request.form.get("email")
        password = request.form.get("password")
        if email and password:
            email = email.lower()
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
                    "message": f"user with email '{email}' already exists"
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


class Login(MethodView):
    @staticmethod
    def post():
        email = request.form.get("email")
        password = request.form.get("password")
        if email and password:
            email = email.lower()
            if not is_valid_email(email):
                return jsonify({
                    "status": "failure",
                    "message": "invalid email format"
                }), 400

            user = User.query.filter_by(email=email).first()
            if user:
                if user.validate_password(password):
                    return jsonify({
                        "status": "success",
                        "message": f"Login successful for '{user.email}'",
                        "token": User.generate_token(user.id).decode()
                    }), 200
                return jsonify({
                    "status": "failure",
                    "message": "Wrong password for the given email address"
                }), 403
            return jsonify({
                "status": "failure",
                "message": f"user with email '{email}' doesn't exist"
            }), 403
        return jsonify({
            "status": "failure",
            "message": "you need to enter both the email and the password"
        }), 400


class Logout(MethodView):
    @staticmethod
    def post():
        # Logout works only if a user is logged in and has an authentication token
        user_id, msg, status, status_code, token = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": msg
            }), status_code

        user = User.query.filter_by(id=user_id).first()
        blacklist = BlacklistToken(token)
        if blacklist.save():  # blacklist token
            return jsonify({
                "status": "success",
                "message": f"Successfully logged out '{user.email}'"
            }), 400


register_user = RegisterUser.as_view("register_user")
login = Login.as_view("login")
logout = Logout.as_view("logout")

auth.add_url_rule("/auth/register", view_func=register_user, methods=['POST'])
auth.add_url_rule("/auth/login", view_func=login, methods=['POST'])
auth.add_url_rule("/auth/logout", view_func=logout, methods=['POST'])
