from datetime import datetime
from app.models import User, ShoppingList, Item


def parse_auth_header(request):
    """
    parse_auth_header is a helper function for obtaining a user's ID
    by using the Authorization header.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header:
        # check if we are using the JWT-Based Authentication mechanism
        if len(auth_header.split()) != 2 or (auth_header.split()[0]).title() != "Bearer":
            message = "Authentication Header is poorly formatted. The acceptable format is `Bearer <jwt_token>`"
            return None, message, "failure", 403, None  # Forbidden

        token = auth_header.split()[1]
        user_id, err = User.verify_token(token)

        if isinstance(user_id, int) and err is None:
            return user_id, "successful obtained user_id", "success", 200, token
        return None, err, "failure", 401, None

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


def parse_notify_date(date_string):
    split_date = date_string.split("-")

    if len(split_date) != 3 or len(split_date[0]) != 4 or \
            not (0 < len(split_date[1]) < 3) \
            or not (0 < len(split_date[2]) < 3):
        return None, "the acceptable date format is `yyyy-mm-dd`"

    try:
        year = int(split_date[0])
        month = int(split_date[1])
        day = int(split_date[2])

        today_year = datetime.today().year
        today_month = datetime.today().month
        today_day = datetime.today().day

        try:
            formed_date = datetime.strptime(
                f"{year}-{month}-{day}", "%Y-%m-%d")
            month_string = formed_date.strftime("%B")

            if year < today_year:
                return None, f"The year {year} already passed, please use a valid year"

            if year > 2100:
                return None, "By {0}, you may be in afterlife, please "\
                    "consider years in range ({1}-2099)".format(year,
                                                                today_year)

            if year == datetime.today().year and month < datetime.today().month:
                return None, f"Invalid date, {month_string} {today_year} has already passed by"

            if year == today_year and month == today_month and day < today_day:
                return None, "Use dates starting from {}".format(datetime.now().strftime("%d/%m/%Y"))

            return str(formed_date).split()[0], "success"

        except ValueError:
            return None, "The given date is invalid and doesn't exist on the calendar"
    except ValueError:
        return None, "dates must be specified as strings but with integer values"
