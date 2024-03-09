from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from pizzami.foods.serializers import FoodCategoryCompleteOutputSerializer, FoodCategoryDetailedOutputSerializer, \
    FoodCategoryPaginatedOutputSerializer

CREATE_FOOD_CATEGORY_201_RESPONSE = OpenApiResponse(
    response=FoodCategoryCompleteOutputSerializer,
    description="a new food category created successfully."
)

SAVE_FOOD_CATEGORY_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: a compound's min value is larger "
                "than its max value."
)

FOOD_CATEGORY_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

FOOD_CATEGORY_403_RESPONSE = OpenApiResponse(
    description="non-staff user is trying to create, update or delete a new food category"
)

GET_FOOD_CATEGORIES_200_RESPONSE = OpenApiResponse(
    response=FoodCategoryPaginatedOutputSerializer(),
    description="just for list representation and contains only id, icon & name"
)

RETRIEVE_FOOD_CATEGORY_200_RESPONSE = OpenApiResponse(
    response=FoodCategoryDetailedOutputSerializer,
    description="API's staff purposes: admins see complete details of a food category. /// \n"
                "API's non-staff purposes: customers want to create a new food and need specific details containing"
                "information about compounds. "
                "is customizable, is_active, position & all timestamped fields are only included for staff purposes"
)

FOOD_CATEGORY_404_RESPONSE = OpenApiResponse(
    description="active food category with specified id does not exist"
)

DELETE_FOOD_CATEGORY_204_RESPONSE = OpenApiResponse(
    description="food category deleted successfully."
)

UPDATE_FOOD_CATEGORY_200_RESPONSE = OpenApiResponse(
    response=FoodCategoryCompleteOutputSerializer,
    description="food category updated successfully"
)

CHANGE_FOOD_CATEGORY_ACTIVATION_STATUS_200_RESPONSE = OpenApiResponse(
    response={"message": "food category activated/deactivated successfully"})

CHANGE_FOOD_CATEGORY_ACTIVATION_STATUS_RESPONSES = {
    200: CHANGE_FOOD_CATEGORY_ACTIVATION_STATUS_200_RESPONSE,
    401: FOOD_CATEGORY_401_RESPONSE,
    403: FOOD_CATEGORY_403_RESPONSE,
    404: FOOD_CATEGORY_404_RESPONSE
}

GET_FOOD_CATEGORIES_PARAMETERS = [
    OpenApiParameter(name="is_customizable", description="can be true or false"),
    OpenApiParameter(name="page_size", description="must be a valid int"),
    OpenApiParameter(name="page", description="must be a valid int")
]
