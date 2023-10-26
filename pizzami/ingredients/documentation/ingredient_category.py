from drf_spectacular.utils import OpenApiResponse

from pizzami.ingredients.serializers.ingredient_category import IngredientCategoryCompleteOutputSerializer

GET_INGREDIENT_CATEGORIES_RESPONSE = OpenApiResponse(
    response=IngredientCategoryCompleteOutputSerializer,
    description="created_at, updated_at & is_active fields are only visible to users with staff privileges."
)
