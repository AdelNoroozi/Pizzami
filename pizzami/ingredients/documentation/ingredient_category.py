from drf_spectacular.utils import OpenApiResponse

from pizzami.ingredients.serializers import IngredientCategoryCompleteOutputSerializer

GET_INGREDIENT_CATEGORIES_200_RESPONSE = OpenApiResponse(
    response=IngredientCategoryCompleteOutputSerializer(many=True),
    description="created_at, updated_at & is_active fields are only visible to users with staff privileges."
)

CREATE_INGREDIENT_CATEGORY_201_RESPONSE = OpenApiResponse(
    response=IngredientCategoryCompleteOutputSerializer,
    description="a new ingredient category created successfully."
)

UPDATE_INGREDIENT_CATEGORY_200_RESPONSE = OpenApiResponse(
    response=IngredientCategoryCompleteOutputSerializer,
    description="ingredient category updated successfully."
)

SAVE_INGREDIENT_CATEGORY_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: image alt text does not contain /"
                "ingredient category's name."
)

INGREDIENT_CATEGORY_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

INGREDIENT_CATEGORY_403_RESPONSE = OpenApiResponse(
    description="non-staff user is trying to create, update or delete a new ingredient category"
)

INGREDIENT_CATEGORY_404_RESPONSE = OpenApiResponse(
    description="ingredient category with specified id does not exist"
)

DELETE_INGREDIENT_CATEGORY_204_RESPONSE = OpenApiResponse(
    description="ingredient category deleted successfully."
)

CHANGE_INGREDIENT_CATEGORY_ACTIVATION_STATUS_200_RESPONSE = OpenApiResponse(
    response={"message": "ingredient category activated/deactivated successfully"})

CHANGE_INGREDIENT_CATEGORY_ACTIVATION_STATUS_RESPONSES = {
    200: CHANGE_INGREDIENT_CATEGORY_ACTIVATION_STATUS_200_RESPONSE,
    401: INGREDIENT_CATEGORY_401_RESPONSE,
    403: INGREDIENT_CATEGORY_403_RESPONSE,
    404: INGREDIENT_CATEGORY_404_RESPONSE
}

DELETE_INGREDIENT_CATEGORY_400_RESPONSE = OpenApiResponse(
    description="can't delete this category as long as it has ingredients or some food category is using it as one of "
                "its compounds."
)

DELETE_INGREDIENT_CATEGORY_RESPONSES = {
    204: DELETE_INGREDIENT_CATEGORY_204_RESPONSE,
    400: DELETE_INGREDIENT_CATEGORY_400_RESPONSE,
    401: INGREDIENT_CATEGORY_401_RESPONSE,
    403: INGREDIENT_CATEGORY_403_RESPONSE,
    404: INGREDIENT_CATEGORY_404_RESPONSE
}
