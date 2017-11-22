import re
from flask import jsonify, request, Blueprint
from flask.views import MethodView
from flask_bcrypt import Bcrypt

from app.models import User, BlacklistToken
from app.endpoints import parse_auth_header

auth = Blueprint("auth", __name__, url_prefix='/api/v1')


def is_valid_email(email):
    """ helper function for validating an email address format"""
    # ne touche pas ici
    exp = r"^([\w\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-z]{2,4}|[0-9]{1,3})(\]?)$"
    return re.match(exp, email)


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

            if len(password) < 6:  # 6 is the minimum expected password length
                return jsonify({
                    "status": "failure",
                    "message": "password must have a minimum of 6 characters"
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
            }), 200


class ResetPassword(MethodView):
    @staticmethod
    def post():
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm password")
        if email and password and confirm_password:
            if len(password) < 6:  # 6 is the minimum expected password length
                return jsonify({
                    "status": "failure",
                    "message": "password must have a minimum of 6 characters"
                }), 400

            password_hash = Bcrypt().generate_password_hash(password).decode('utf-8')

            # if the passwords are similar...
            if Bcrypt().check_password_hash(password_hash, confirm_password):
                user = User.query.filter_by(email=email.lower()).first()
                if user:
                    user.password = password_hash
                    user.save()
                    return jsonify({
                        "status": "success",
                        "message": f"password reset successful for '{user.email}'"
                    }), 200

                return jsonify({
                    "status": "failure",
                    "message": f"user with email `{email}` not found!"
                }), 403
            return jsonify({
                "status": "failure",
                "message": "the given passwords don't match"
            }), 403

        return jsonify({
            "status": "failure",
            "message": "the fields: email, password, and 'confirm password' are required"
        }), 400


register_user = RegisterUser.as_view("register_user")
login = Login.as_view("login")
logout = Logout.as_view("logout")
reset_password = ResetPassword.as_view("reset_password")

auth.add_url_rule("/auth/register", view_func=register_user, methods=['POST'])
auth.add_url_rule("/auth/login", view_func=login, methods=['POST'])
auth.add_url_rule("/auth/logout", view_func=logout, methods=['POST'])
auth.add_url_rule("/auth/reset-password",
                  view_func=reset_password, methods=['POST'])
