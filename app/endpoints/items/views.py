from datetime import datetime
from flask.views import MethodView
from flask import Blueprint, request, jsonify

from app.models import Item
from app.endpoints import parse_auth_header, get_shoppinglist

items = Blueprint("items", __name__, url_prefix="/api/v1")


class ItemsAPI(MethodView):
    @staticmethod
    def post(list_id):
        """Adds an item to a shoppinglist"""

        user_id, message, status, status_code, _ = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": message
            }), status_code
        shoppinglist, message, status, status_code = get_shoppinglist(
            user_id, list_id)
        if shoppinglist:
            # form fields
            name = request.form.get("name")
            price = request.form.get("price")
            quantity = request.form.get("quantity")
            status = request.form.get("status")

            has_been_bought = True if status and status.title() == "True" else False
            if name and price and quantity:
                name = name.strip().lower()

                name_already_exists = Item.query.filter(
                    Item.shoppinglist_id == list_id).filter(Item.name == name).all()

                if name_already_exists:
                    return jsonify({
                        "status": "failure",
                        "message": f"an item with name '{name}' already exists"
                    }), 409

                item = Item(list_id, name, quantity,
                            price, status=has_been_bought)
                item.save()
                return jsonify({
                    "status": "success",
                    "message": f"'{item.name}' has been added"
                }), 201
            return jsonify({
                "status": "failure",
                "message": "'name', 'price' and 'quantity' of an item must be specified whereas 'status' is optional"
            }), 400
        return jsonify({
            "status": status,
            "message": message
        }), status_code

    @staticmethod
    def get(list_id):
        user_id, message, status, status_code, _ = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": message
            }), status_code
        shoppinglist, message, status, status_code = get_shoppinglist(
            user_id, list_id)
        if shoppinglist:
            # the query parameters for items
            q = request.args.get('q', None, type=str)
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('limit', 10, type=int)
            if per_page and per_page > 20:
                per_page = 20
            if not per_page or per_page < 1:
                per_page = 20
            if not page or page < 1:
                page = 1

            query_object = Item.query.filter(Item.shoppinglist_id == list_id)
            if q is not None:
                query_object = query_object.filter(
                    Item.name.like('%' + q.strip().lower() + '%'))

            pagination_object = query_object.paginate(
                page=page, per_page=per_page, error_out=False)

            list_items = []
            for item in pagination_object.items:
                list_items.append({
                    "id": item.id,
                    "name": item.name,
                    "date modified": item.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
                    "current page": page,
                    "total number of pages": pagination_object.pages
                })
            if list_items:
                if q is not None:
                    return jsonify({
                        "status": "success",
                        "matched items": list_items
                    }), 200
                return jsonify({
                    "status": "success",
                    "items": list_items
                }), 200
            if q is not None:
                return jsonify({
                    "status": "success",
                    "message": "your query did not match any items"
                }), 200
            return jsonify({
                "status": 'success',
                "message": 'no items on this list'
            }), 200
        return jsonify({
            "status": status,
            "message": message
        }), status_code


items_api = ItemsAPI.as_view("items_api")

items.add_url_rule("/shoppinglists/<list_id>/items",
                   view_func=items_api, methods=['POST', 'GET'])
