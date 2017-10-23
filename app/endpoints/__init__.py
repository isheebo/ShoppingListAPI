from app.models import User, ShoppingList, Item


def parse_auth_header(request):
    """
    parse_auth_header is a helper function for obtaining a user's ID
    by using the Authorization header.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header:
        # check if we have are using the JWT-Based Aunthentication mechanism
        if len(auth_header.split()) != 2 or (auth_header.split()[0]).title() != "Bearer":
            message = "Authentication Header is poorly formatted. The acceptable format is `Bearer <jwt_token>`"
            return None, message, "failure", 403, None  # Forbidden

        token = auth_header.split()[1]
        user_id, err = User.verify_token(token)

        if isinstance(user_id, int) and err is None:
            return user_id, "successful obtained user_id", "success", 200, token
        message = f"error in token: {err}"
        return None, message, "failure", 401, None

    message = "Authorization header must be set for a successful request"
    return None, message, "failure", 403, None  # Unauthorized


def get_shoppinglist(user_id, list_id):
    """Returns a shoppinglist specified by <list_id> if
       the User specified by <user_id> has that list.
    """
    try:
        list_id = int(list_id)
        shoppinglist = ShoppingList.query.filter(
            ShoppingList.user_id == user_id).filter(ShoppingList.id == list_id).first()
        if shoppinglist:
            return shoppinglist, None, "success", 200
        status = "failure"
        message = "shopping list with that ID cannot be found!"
        status_code = 404
        return None, message, status, status_code
    except ValueError:
        status = "failure"
        status_code = 400
        message = "shopping list IDs must be integers"
        return None, message, status, status_code


def get_item(user_id, list_id, item_id):
    shoppinglist, message, status, status_code = get_shoppinglist(
        user_id, list_id)

    if shoppinglist is None:
        return None, message, status, status_code

    try:
        item_id = int(item_id)
        item = Item.query.filter(Item.shoppinglist_id == list_id).filter(
            Item.id == item_id).first()
        if item:
            return item, None, "success", 200

        status = "failure"
        message = "item with that ID cannot be found!"
        status_code = 404
        return None, message, status, status_code

    except ValueError:
        status = "failure"
        status_code = 400
        message = "item IDs must be integers"
        return None, message, status, status_code
