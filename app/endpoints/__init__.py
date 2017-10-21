from app.models import User


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
