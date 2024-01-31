from drf_spectacular.utils import OpenApiResponse

from pizzami.ingredients.serializers import IngredientCompleteOutputSerializer

GET_INGREDIENTS_200_RESPONSE = OpenApiResponse(
    response=IngredientCompleteOutputSerializer(many=True),
    description="created_at, updated_at & is_active fields are only visible to users with staff privileges."
)

CREATE_INGREDIENT_201_RESPONSE = OpenApiResponse(
    response=IngredientCompleteOutputSerializer,
    description="a new ingredient created successfully."
)

UPDATE_INGREDIENT_200_RESPONSE = OpenApiResponse(
    response=IngredientCompleteOutputSerializer,
    description="ingredient updated_successfully"
)

SAVE_INGREDIENT_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: image alt text does not contain /"
                "ingredient's name, category with specified id does not exist."
)

INGREDIENT_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

INGREDIENT_403_RESPONSE = OpenApiResponse(
    description="non-staff user is trying to create, update or delete a new ingredient"
)

INGREDIENT_404_RESPONSE = OpenApiResponse(
    description="ingredient with specified id does not exist"
)

DELETE_INGREDIENT_204_RESPONSE = OpenApiResponse(
    description="ingredient deleted successfully."
)

CHANGE_INGREDIENT_ACTIVATION_STATUS_200_RESPONSE = OpenApiResponse(
    response={"message": "ingredient activated/deactivated successfully"})

CHANGE_INGREDIENT_ACTIVATION_STATUS_RESPONSES = {
    200: CHANGE_INGREDIENT_ACTIVATION_STATUS_200_RESPONSE,
    401: INGREDIENT_401_RESPONSE,
    403: INGREDIENT_403_RESPONSE,
    404: INGREDIENT_404_RESPONSE
}
