from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiOptionalAuthMixin
from pizzami.ingredients.services import get_ingredient_categories


class IngredientCategoryAPI(ApiOptionalAuthMixin, APIView):

    @extend_schema()
    def get(self, request):
        print(request.user.is_staff)
        data = get_ingredient_categories(request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)
