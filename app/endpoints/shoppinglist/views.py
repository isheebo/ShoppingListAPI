from datetime import datetime
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

    @staticmethod
    def get():
        """
        Returns the shoppinglists that are owned by the logged in user.
        The lists returned depend on whether there were any specified query parameters.
        """
        user_id, message, status, status_code, _ = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": message
            }), status_code

        # the query parameters
        q = request.args.get('q', None, type=str)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 10, type=int)
        if per_page and per_page > 20:
            per_page = 20
        if not per_page or per_page < 1:
            per_page = 20
        if not page or page < 1:
            page = 1

        query_object = ShoppingList.query.filter(
            ShoppingList.user_id == user_id)
        if q is not None:
            query_object = query_object.filter(ShoppingList.name.like(
                '%' + q.strip().lower() + '%'))

        pagination_object = query_object.paginate(
            page=page, per_page=per_page, error_out=False)

        shoppinglists = []
        for shoppinglist in pagination_object.items:
            shoppinglists.append({
                "id": shoppinglist.id,
                "name": shoppinglist.name,
                "date created": shoppinglist.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "notify date": shoppinglist.notify_date.strftime("%Y-%m-%d"),
                "date modified": shoppinglist.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
                "current page": page,
                "total number of pages": pagination_object.pages
            })
        if shoppinglists:
            if q is not None:
                return jsonify({
                    "status": "success",
                    "matched lists": shoppinglists
                }), 200
            return jsonify({
                "status": "success",
                "lists": shoppinglists
            }), 200
        if q is not None:
            return jsonify({
                "status": "success",
                "message": "your query did not match any shopping lists"
            }), 200
        return jsonify({
            "status": "success",
            "message": "No shoppinglists found!"
        }), 200


shopping_api = ShoppingListAPI.as_view("shopping_api")
list_blueprint.add_url_rule(
    "/shoppinglists", view_func=shopping_api, methods=['POST', 'GET'])
