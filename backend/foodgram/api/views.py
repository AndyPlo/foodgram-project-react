from recipes.models import Ingredient, Recipe
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view
# from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          SetPasswordSerializer, UserCreateSerializer,
                          UserReadSerializer)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserReadSerializer
        return UserCreateSerializer

    @action(detail=False, methods=['get'],
            serializer_class=UserReadSerializer,
            pagination_class=None)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def set_password(request):
    serializer = SetPasswordSerializer(request.user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response(
        'Пароль успешно изменен!',
        status=status.HTTP_204_NO_CONTENT
    )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
