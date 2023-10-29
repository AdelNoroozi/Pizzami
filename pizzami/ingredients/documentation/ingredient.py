from drf_spectacular.utils import OpenApiResponse

from pizzami.ingredients.serializers import IngredientCompleteOutputSerializer

GET_INGREDIENTS_200_RESPONSE = OpenApiResponse(
    response=IngredientCompleteOutputSerializer,
    description="created_at, updated_at & is_active fields are only visible to users with staff privileges."
)
