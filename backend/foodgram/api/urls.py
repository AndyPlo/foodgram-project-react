from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()
v1_router.register(r'recipes', views.RecipeViewSet, basename='recipe')
v1_router.register(r'users', views.UserViewSet, basename='users')
v1_router.register(
    r'ingredients', views.IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('users/set_password/', views.set_password, name='set_password'),
    path('', include(v1_router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
