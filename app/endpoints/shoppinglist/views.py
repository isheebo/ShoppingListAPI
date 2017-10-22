from flask import Blueprint, request, jsonify
from flask.views import MethodView

from app.endpoints import parse_auth_header
from app.models import ShoppingList

list_blueprint = Blueprint("list_blueprint", __name__, url_prefix="/api/v1")


class ShoppingListAPI(MethodView):
    @staticmethod
    def post():
        """Adds a new shoppinglist to the currently logged in user account"""
        user_id, message, status, status_code, _ = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": message
            }), status_code

        name = request.form.get("name")
        if name:
            name = name.strip().lower()
            name_already_exists = ShoppingList.query.filter(
                ShoppingList.user_id == user_id).filter(ShoppingList.name == name).all()
            if name_already_exists:
                return jsonify({
                    "status": "failure",
                    "message": f"a shopping list with name '{name}' already exists"
                }), 409

            shoppinglist = ShoppingList(user_id, name)
            shoppinglist.save()
            return jsonify({
                "status": "success",
                "message": f"'{shoppinglist.name}' successfully created"
            }), 201
        return jsonify({
            "status": "failure",
            "message": "'name' of the shoppinglist is a required field"
        }), 400


shopping_api = ShoppingListAPI.as_view("shopping_api")
list_blueprint.add_url_rule(
    "/shoppinglists", view_func=shopping_api, methods=['POST'])
