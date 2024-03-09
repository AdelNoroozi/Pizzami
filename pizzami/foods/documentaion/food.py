from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from pizzami.foods.serializers import FoodDetailedOutputSerializer, FoodCompleteOutputSerializer

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
    OpenApiParameter(name="tags__name", description="must be a tag"),
    OpenApiParameter(name="created_by", description="must be the id of a user profile"),
    OpenApiParameter(name="is_original", description="must be true or false"),
    OpenApiParameter(name="is_confirmed", description="must be true or false"),
    OpenApiParameter(name="is_public", description="must be true or false"),
    OpenApiParameter(name="price__gt", description="must be a float"),
    OpenApiParameter(name="price__lt", description="must be a float"),
    OpenApiParameter(name="order_by", description="can be rate, price, ordered_count, position, created_at or "
                                                  "updated_at. a - symbol can be added before the param for descending"
                                                  " order."),
]

CREATE_FOOD_201_RESPONSE = OpenApiResponse(
    response=FoodCompleteOutputSerializer,
    description="a new food created successfully."
)

SAVE_FOOD_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: there is some ingredient that "
                "should not be inside foods from this category."
)

FOOD_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

CREATE_FOOD_RESPONSES = {
    201: CREATE_FOOD_201_RESPONSE,
    400: SAVE_FOOD_400_RESPONSE,
    401: FOOD_401_RESPONSE
}

RETRIEVE_FOOD_200_RESPONSE = OpenApiResponse(
    response=FoodCompleteOutputSerializer,
    description="only staff users can see is_public, is_confirmed, is_active, position & all timestamped fields."
)

FOOD_404_RESPONSE = OpenApiResponse(
    description="no food found with given id inside your access zone"
)

RETRIEVE_FOOD_RESPONSES = {
    200: RETRIEVE_FOOD_200_RESPONSE,
    404: FOOD_404_RESPONSE
}

UPDATE_FOOD_200_RESPONSE = OpenApiResponse(
    response=FoodCompleteOutputSerializer,
    description="food updated successfully"
)

UPDATE_FOOD_RESPONSES = {
    200: UPDATE_FOOD_200_RESPONSE,
    400: SAVE_FOOD_400_RESPONSE,
    401: FOOD_401_RESPONSE,
    404: FOOD_404_RESPONSE
}

CHANGE_FOOD_ACTIVATION_STATUS_200_RESPONSE = OpenApiResponse(
    response={"message": "food activated/deactivated successfully"})

FOOD_403_RESPONSE = OpenApiResponse(
    description="you are not allowed to perform this action on this food"
)

CHANGE_FOOD_ACTIVATION_STATUS_RESPONSES = {
    200: CHANGE_FOOD_ACTIVATION_STATUS_200_RESPONSE,
    401: FOOD_401_RESPONSE,
    403: FOOD_403_RESPONSE,
    404: FOOD_404_RESPONSE
}

CHANGE_FOOD_CONFIRMATION_STATUS_200_RESPONSE = OpenApiResponse(
    response={"message": "food confirmed/rejected/suspended successfully"})

CHANGE_FOOD_CONFIRMATION_STATUS_400_RESPONSE = OpenApiResponse(
    description="invalid request, probably due to invalid action or trying to change foods status to an status which "
                "the food is already in."
)

CHANGE_FOOD_CONFIRMATION_STATUS_RESPONSES = {
    200: CHANGE_FOOD_CONFIRMATION_STATUS_200_RESPONSE,
    400: CHANGE_FOOD_CONFIRMATION_STATUS_400_RESPONSE,
    401: FOOD_401_RESPONSE,
    403: FOOD_403_RESPONSE,
    404: FOOD_404_RESPONSE
}
