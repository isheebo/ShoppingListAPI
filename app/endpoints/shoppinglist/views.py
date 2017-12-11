from datetime import datetime
from flask import Blueprint, request, jsonify
from flask.views import MethodView

from app.endpoints import parse_auth_header, get_shoppinglist, parse_notify_date
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

        # prevents errors due to empty string names
        name = request.form.get("name")
        notify_date = request.form.get("notify date")

        name = name.strip() if name else ""
        notify_date = notify_date.strip() if notify_date else ""

        if name and notify_date:
            name = name.lower()
            name_already_exists = ShoppingList.query.filter(
                ShoppingList.user_id == user_id).filter(ShoppingList.name == name).all()
            if name_already_exists:
                return jsonify({
                    "status": "failure",
                    "message": f"a shopping list with name '{name}' already exists"
                }), 409

            date_string, message = parse_notify_date(notify_date)
            if date_string is None:
                return jsonify({
                    "status": "failure",
                    "message": message,
                }), 400

            shoppinglist = ShoppingList(user_id, name, date_string)
            shoppinglist.save()
            return jsonify({
                "status": "success",
                "message": f"'{shoppinglist.name}' successfully created"
            }), 201
        return jsonify({
            "status": "failure",
            "message": "'name' and 'notify date' of the shoppinglist are required fields"
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
        search_query = request.args.get('q', None, type=str)
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
        if search_query is not None:
            query_object = query_object.filter(ShoppingList.name.like(
                '%' + search_query.strip().lower() + '%'))

        # pg_object refers to the pagination object obtained
        pg_object = query_object.paginate(
            page=page, per_page=per_page, error_out=False)

        next_page = None
        if pg_object.has_next:
            next_page = "/api/v1/shoppinglists?page={0}{1}{2}".format(
                pg_object.next_num,
                '' if per_page == 20 else f'&limit={per_page}',
                '' if search_query is None else f'&q={search_query}')

        previous_page = None
        if pg_object.has_prev:
            previous_page = "/api/v1/shoppinglists?page={0}{1}{2}".format(
                pg_object.prev_num,
                '' if per_page == 20 else f'&limit={per_page}',
                '' if search_query is None else f'&q={search_query}')

        shoppinglists = []
        for shoppinglist in pg_object.items:
            shoppinglists.append({
                "id": shoppinglist.id,
                "name": shoppinglist.name,
                "date created": shoppinglist.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "notify date": shoppinglist.notify_date.strftime("%Y-%m-%d"),
                "date modified": shoppinglist.date_modified.strftime("%Y-%m-%d %H:%M:%S")
            })

        if shoppinglists:
            if search_query is not None:
                return jsonify({
                    "status": "success",
                    "matched lists": shoppinglists,
                    "next page": next_page,
                    "previous page": previous_page
                }), 200

            return jsonify({
                "status": "success",
                "lists": shoppinglists,
                "next page": next_page,
                "previous page": previous_page
            }), 200

        if search_query is not None:
            return jsonify({
                "status": "success",
                "message": "your query did not match any shopping lists"
            }), 200

        return jsonify({
            "status": "success",
            "message": "No shoppinglists found!"
        }), 200


class ShoppingListByID(MethodView):
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
            return jsonify({
                "id": shoppinglist.id,
                "name": shoppinglist.name,
                "notify date": shoppinglist.notify_date.strftime("%Y-%m-%d"),
            }), status_code
        return jsonify({
            "status": status,
            "message": message
        }), status_code

    @staticmethod
    def delete(list_id):
        user_id, message, status, status_code, _ = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": message
            }), status_code

        shoppinglist, message, status, status_code = get_shoppinglist(
            user_id, list_id)
        if shoppinglist and shoppinglist.delete():
            return jsonify({
                "status": status,
                "message": f"shopping list with ID {list_id} deleted successfully"
            }), status_code

        return jsonify({
            "status": status,
            "message": message
        }), status_code

    @staticmethod
    def put(list_id):
        user_id, message, status, status_code, _ = parse_auth_header(request)
        if user_id is None:
            return jsonify({
                "status": status,
                "message": message
            }), status_code

        shoppinglist, message, status, status_code = get_shoppinglist(
            user_id, list_id)
        if shoppinglist:  # a shoppinglist with list_id exists in the database

            name = request.form.get("name")
            notify_date = request.form.get("notify date")

            name = name.strip() if name else ""
            notify_date = notify_date.strip() if notify_date else ""

            if name and notify_date:
                name = name.lower()
                name_already_exists = ShoppingList.query.filter(ShoppingList.user_id == user_id).filter((
                    (ShoppingList.name == name) & (ShoppingList.id != list_id))).all()

                date_string, message = parse_notify_date(notify_date)
                if date_string is None:
                    return jsonify({
                        "status": "failure",
                        "message": message,
                    }), 400

                if shoppinglist.name == name and shoppinglist.notify_date.strftime("%Y-%m-%d") == date_string:
                    return jsonify({
                        "status": "failure",
                        "message": "No changes were made to the list"
                    }), 200

                if name_already_exists:  # if name already exists and is not the current shopping list name, then do:-
                    return jsonify({
                        "status": "failure",
                        "message": f"a shopping list with name '{name}' already exists"
                    }), 409

                shoppinglist.name = name
                shoppinglist.notify_date = date_string
                shoppinglist.date_modified = datetime.now()
                shoppinglist.save()
                return jsonify({
                    "status": "success",
                    "data": {
                        "id": shoppinglist.id,
                        "name": shoppinglist.name,
                        "date modified": shoppinglist.date_modified,
                        "notify date": shoppinglist.notify_date
                    },
                    "message": "shoppinglist has been successfully edited!"
                }), 200

            return jsonify({
                "status": "failure",
                "message": "'name' and 'notify date' of the shoppinglist are required fields"
            }), 400

        return jsonify({
            "status": status,
            "message": message
        }), status_code


shopping_list_api = ShoppingListAPI.as_view("shopping_list_api")
shopping_list_by_id = ShoppingListByID.as_view("shopping_list_by_id")

list_blueprint.add_url_rule(
    "/shoppinglists", view_func=shopping_list_api, methods=['POST', 'GET'])
list_blueprint.add_url_rule(
    "/shoppinglists/<list_id>", view_func=shopping_list_by_id, methods=['GET', 'DELETE', 'PUT'])
