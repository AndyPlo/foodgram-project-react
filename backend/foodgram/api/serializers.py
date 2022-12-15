from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import (Favorite, Ingredient, Recipe, Recipe_ingredient,
                            Shopping_cart, Tag)
from rest_framework import serializers
from users.models import Subscribe, User

# -----------------------------------------------------------------------------
#                            Приложение users
# -----------------------------------------------------------------------------


class UserReadSerializer(UserSerializer):
    """[GET] Cписок пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        try:
            return Subscribe.objects.filter(user=self.context['request'].user,
                                            author=obj).exists()
        except Exception:
            return False


class UserCreateSerializer(UserCreateSerializer):
    """[POST] Создание нового пользователя."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }

    def validate(self, obj):
        invalid_usernames = ['me', 'set_password',
                             'subscriptions', 'subscribe']
        if self.initial_data.get('username') in invalid_usernames:
            raise serializers.ValidationError(
                {'username': 'Вы не можете использоват этот username.'}
            )
        return obj


class SetPasswordSerializer(serializers.Serializer):
    """[POST] Изменение пароля пользователя."""
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, obj):
        try:
            validate_password(obj['new_password'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)}
            )
        return super().validate(obj)

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError(
                {'current_password': 'Неправильный пароль.'}
            )
        if (validated_data['current_password']
           == validated_data['new_password']):
            raise serializers.ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего.'}
            )
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data


class RecipeSerializer(serializers.ModelSerializer):
    """Список рецептов без ингридиентов."""
    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time')


class SubscriptionsSerializer(serializers.ModelSerializer):
    """[GET] Список авторов на которых подписан пользователь."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=self.context['request'].user,
                                        author=obj).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscribeAuthorSerializer(serializers.ModelSerializer):
    """[POST, DELETE] Подписка на автора и отписка."""
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def validate(self, obj):
        if (self.context['request'].user == obj):
            raise serializers.ValidationError({'Ошибка подписки.'})
        return obj

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=self.context['request'].user,
                                        author=obj).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

# -----------------------------------------------------------------------------
#                            Приложение recipes
# -----------------------------------------------------------------------------


class IngredientSerializer(serializers.ModelSerializer):
    """[GET] Список ингредиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """[GET] Список тегов."""
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Список ингредиентов с количеством для рецепта."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Recipe_ingredient
        fields = ('id', 'name',
                  'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """[GET] Список рецептов."""
    author = UserReadSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source='recipes')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image',
                  'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(user=self.context['request'].user,
                                       recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return Shopping_cart.objects.filter(user=self.context['request'].user,
                                            recipe=obj).exists()


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Ингредиент и количество для создания рецепта."""
    id = serializers.IntegerField()

    class Meta:
        model = Recipe_ingredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """[POST, PATCH, DELETE] Создание, изменение и удаление рецепта."""
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    author = UserReadSerializer(read_only=True)
    id = serializers.ReadOnlyField()
    ingredients = RecipeIngredientCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients',
                  'tags', 'image',
                  'name', 'text',
                  'cooking_time', 'author')
        extra_kwargs = {
            'ingredients': {'required': True, 'allow_blank': False},
            'tags': {'required': True, 'allow_blank': False},
            'name': {'required': True, 'allow_blank': False},
            'text': {'required': True, 'allow_blank': False},
            'cooking_time': {'required': True},
        }

    def validate(self, obj):
        if not obj.get('tags'):
            raise serializers.ValidationError(
                {'tags': 'Нужно указать минимум 1 тег.'}
            )
        if not obj.get('ingredients'):
            raise serializers.ValidationError(
                {'ingredients': 'Нужно указать минимум 1 ингредиент.'}
            )
        if (len({ingredient['id'] for ingredient in obj.get('ingredients')})
           != len(obj.get('ingredients'))):
            raise serializers.ValidationError(
                {'ingredients': 'Ингредиенты должны быть уникальны.'}
            )
        return obj

    def tags_and_ingedients_set(self, recipe, tags, ingredients):
        recipe.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(pk=ingredient['id'])
            Recipe_ingredient.objects.create(recipe=recipe,
                                             ingredient=current_ingredient,
                                             amount=ingredient['amount'])

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        self.tags_and_ingedients_set(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        try:
            # instance.image = validated_data.pop('image')
            instance.name = validated_data.pop('name')
            instance.text = validated_data.pop('text')
            instance.cooking_time = validated_data.pop('cooking_time')
        except Exception as error_field:
            raise serializers.ValidationError(
                {str(error_field)[1:-1]: ['Обязательное поле.']})
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        Recipe_ingredient.objects.filter(
            recipe=instance,
            ingredient__in=instance.ingredients.all()).delete()
        self.tags_and_ingedients_set(instance, tags, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance).data
