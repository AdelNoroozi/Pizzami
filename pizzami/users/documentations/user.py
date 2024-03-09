from drf_spectacular.utils import OpenApiParameter

GET_USERS_PARAMETERS = [
    OpenApiParameter(name="search", description="can be any str. this will be done on users' 'email' & 'public name'."),
    OpenApiParameter(name="is_active", description="must be true or false"),
    OpenApiParameter(name="is_admin", description="must be true or false"),
    OpenApiParameter(name="is_superuser", description="must be true or false"),
    OpenApiParameter(name="order_by", description="can be created_at or updated_at. a - symbol can be added before the "
                                                  "param for descending order.")
]
