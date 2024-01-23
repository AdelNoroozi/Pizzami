from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from pizzami.foods.serializers import FoodDetailedOutputSerializer

GET_FOODS_200_RESPONSE = OpenApiResponse(
    response=FoodDetailedOutputSerializer(many=True),
    description="Represents a list of foods. If the set parameter has the value 'mine' it will show foods created by"
                "requesting user. This list can be filtered these parameters: category, creator, being original, "
                "price range, confirmed & publicity. It can also be ordered by rate, price, ordered_count, position,"
                " created_at, modified_at ascending & descending. Searching is also available on this list. The output"
                " format for staff users or users who request their own set of foods is different."
)

GET_FOODS_200_PARAMETERS = [
    OpenApiParameter(name="set", description="can be null or 'mine'"),
    OpenApiParameter(name="search", description="can be any string"),
    OpenApiParameter(name="category", description="must be the id of a food category"),
    OpenApiParameter(name="created_by", description="must be the id of a user profile"),
    OpenApiParameter(name="is_original", description="must be true or false"),
    OpenApiParameter(name="is_confirmed", description="must be true or false"),
    OpenApiParameter(name="is_public", description="must be true or false"),
    OpenApiParameter(name="price__gt", description="must be a float"),
    OpenApiParameter(name="price__lt", description="must be a float"),
    OpenApiParameter(name="order_by", description="can be rate, price, ordered_count, position, created_at or "
                                                  "modified_at. a - symbol can be added before the param for descending"
                                                  " order."),
]
