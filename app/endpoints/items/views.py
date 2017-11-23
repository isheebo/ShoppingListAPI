from datetime import datetime
from flask.views import MethodView
from flask import Blueprint, request, jsonify

from app.models import Item
from app.endpoints import parse_auth_header, get_shoppinglist, get_item

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

            has_been_bought = True if status and status.strip().title() == "True" else False
            name = name.strip() if name else ""
            price = price.strip() if price else ""
            quantity = quantity.strip() if quantity else ""

            if name.strip and price and quantity:
                name = name.lower()

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
            search_query = request.args.get('q', None, type=str)
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('limit', 10, type=int)
            if per_page and per_page > 20:
                per_page = 20
            if not per_page or per_page < 1:
                per_page = 20
            if not page or page < 1:
                page = 1

            query_object = Item.query.filter(Item.shoppinglist_id == list_id)
            if search_query is not None:
                query_object = query_object.filter(
                    Item.name.like('%' + search_query.strip().lower() + '%'))

            # pg_object refers to the pagination object obtained
            pg_object = query_object.paginate(
                page=page, per_page=per_page, error_out=False)

            next_page = None
            if pg_object.has_next:
                next_page = "/api/v1/shoppinglists/{0}/items?page={1}{2}{3}".format(
                    list_id, pg_object.next_num, '' if per_page == 20 else f'&limit={per_page}',
                    '' if search_query is None else f'&q={search_query}')

            previous_page = None
            if pg_object.has_prev:
                previous_page = "/api/v1/shoppinglists/{0}/items?page={1}{2}{3}".format(
                    list_id, pg_object.prev_num, '' if per_page == 20 else f'&limit={per_page}',
                    '' if search_query is None else f'&q={search_query}')

            list_items = []
            for item in pg_object.items:
                list_items.append(
                    {
                        "id": item.id,
                        "name": item.name,
                        "price": item.price,
                        "quantity": item.quantity,
                        "has been bought": item.has_been_bought,
                        "date modified": item.date_modified.strftime("%Y-%m-%d %H:%M:%S")
                    }
                )

            if list_items:
                if search_query is not None:
                    return jsonify({
                        "status": "success",
                        "matched items": list_items,
                        "previous page": previous_page,
                        "next page": next_page
                    }), 200

                return jsonify({
                    "status": "success",
                    "items": list_items,
                    "previous page": previous_page,
                    "next page": next_page
                }), 200

            if search_query is not None:
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


class ItemsAPIByID(MethodView):
    @staticmethod
    def get(list_id, item_id):
        user_id, message, status, status_code, _ = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": message
            }), status_code

        item, message, status, status_code = get_item(
            user_id, list_id, item_id)
        if item is not None:
            return jsonify({
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity,
                "has been bought": item.has_been_bought,
                "date modified": item.date_modified.strftime("%Y-%m-%d %H:%M:%S")
            }), 200
        return jsonify({
            "status": status,
            "message": message
        }), status_code

    @staticmethod
    def delete(list_id, item_id):
        user_id, message, status, status_code, _ = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": message
            }), status_code

        item, message, status, status_code = get_item(
            user_id, list_id, item_id)
        if item is not None and item.delete():
            return jsonify({
                'status': status,
                'message': f'an item with ID {item_id} has been successfully deleted'
            }), status_code
        return jsonify({
            "status": status,
            "message": message
        }), status_code

    @staticmethod
    def put(list_id, item_id):
        user_id, message, status, status_code, _ = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": message
            }), status_code

        item, message, status, status_code = get_item(
            user_id, list_id, item_id)
        if item is not None:
            # query parameters
            name = request.form.get("name")
            price = request.form.get("price")
            quantity = request.form.get("quantity")
            status = request.form.get("status")

            has_been_bought = True if status and status.strip().title() == "True" else False

            name = name.strip() if name else ""
            price = price.strip() if price else ""
            quantity = quantity.strip() if quantity else ""

            if name and price and quantity:
                name = name.lower()
                name_already_exists = Item.query.filter(Item.shoppinglist_id == list_id).filter((
                    (Item.name == name) & (Item.id != item_id))).all()

                if (item.name == name and item.quantity == quantity and  # if no edits were made...
                        item.price == price and item.has_been_bought == has_been_bought):
                    return jsonify({
                        "status": "failure",
                        "message": "no changes were made to the item"
                    }), 200

                if name_already_exists:  # if name exists and it isn't the current name we are editing
                    return jsonify({
                        "status": 'failure',
                        "message": f"an item with name '{name}' already exists"
                    }), 409

                item.name = name
                item.price = price
                item.quantity = quantity
                item.has_been_bought = has_been_bought
                item.date_modified = datetime.now()
                item.save()
                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': item.id,
                        'name': item.name,
                        "price": item.price,
                        "quantity": item.quantity,
                        'date modified': item.date_modified,
                        'has been bought': item.has_been_bought
                    },
                    'message': 'item has been updated successfully'
                }), 200
            return jsonify({
                'status': 'failure',
                'message':  "'name', 'price' and 'quantity' of an item must be specified whereas 'status' is optional"
            }), 400
        return jsonify({
            "status": status,
            "message": message
        }), status_code


items_api = ItemsAPI.as_view("items_api")
items_by_id_api = ItemsAPIByID.as_view("items_by_id_api")

items.add_url_rule("/shoppinglists/<list_id>/items",
                   view_func=items_api, methods=['POST', 'GET'])

items.add_url_rule("/shoppinglists/<list_id>/items/<item_id>",
                   view_func=items_by_id_api, methods=['GET', 'DELETE', 'PUT'])
