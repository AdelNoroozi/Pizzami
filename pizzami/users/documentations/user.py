from drf_spectacular.utils import OpenApiParameter, OpenApiResponse

GET_USERS_PARAMETERS = [
    OpenApiParameter(name="search", description="can be any str. this will be done on users' 'email' & 'public name'."),
    OpenApiParameter(name="page_size", description="must be a valid int"),
    OpenApiParameter(name="page", description="must be a valid int"),
    OpenApiParameter(name="is_active", description="must be true or false"),
    OpenApiParameter(name="is_admin", description="must be true or false"),
    OpenApiParameter(name="is_superuser", description="must be true or false"),
    OpenApiParameter(name="order_by", description="can be created_at or updated_at. a - symbol can be added before the "
                                                  "param for descending order.")
]

REQUEST_PASSWORD_200_RESPONSE = OpenApiResponse(
    description="reset password email sent successfully."
)

REQUEST_PASSWORD_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: email is invalid or does not exist."
)

REQUEST_PASSWORD_408_RESPONSE = OpenApiResponse(
    description="something went wrong."
)

REQUEST_PASSWORD_RESPONSES = {
    200: REQUEST_PASSWORD_200_RESPONSE,
    400: REQUEST_PASSWORD_400_RESPONSE,
    408: REQUEST_PASSWORD_408_RESPONSE
}

RESET_PASSWORD_200_RESPONSE = OpenApiResponse(
    description="password reset successfully."
)

RESET_PASSWORD_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: password & confirm password don't"
                " match."
)

RESET_PASSWORD_403_RESPONSE = OpenApiResponse(
    description="Invalid or expired token."
)

RESET_PASSWORD_RESPONSES = {
    200: RESET_PASSWORD_200_RESPONSE,
    400: RESET_PASSWORD_400_RESPONSE,
    403: RESET_PASSWORD_403_RESPONSE
}
