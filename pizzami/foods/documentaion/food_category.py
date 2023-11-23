from drf_spectacular.utils import OpenApiResponse

from pizzami.foods.serializers import FoodCategoryCompleteOutputSerializer, FoodCategoryBaseOutputSerializer

CREATE_FOOD_CATEGORY_201_RESPONSE = OpenApiResponse(
    response=FoodCategoryCompleteOutputSerializer,
    description="a new food category created successfully."
)

SAVE_FOOD_CATEGORY_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: a compound's min value is larger /"
                "than its max value."
)

FOOD_CATEGORY_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

FOOD_CATEGORY_403_RESPONSE = OpenApiResponse(
    description="non-staff user is trying to create, update or delete a new food category"
)

GET_FOOD_CATEGORIES_200_RESPONSE = OpenApiResponse(
    response=FoodCategoryBaseOutputSerializer(many=True),
    description="just for list representation and contains only id, icon & name"
)