from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        null=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Поле должно содержать HEX-код выбранного цвета.'
            )
        ]

    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=200,
        unique=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    name = models.CharField(
        'Название',
        max_length=200
    )
    text = models.TextField(
        'Описание'
    )
    cooking_time = models.IntegerField(
        'Время приготовления, мин',
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Recipe_ingredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Recipe_ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return (f'{self.recipe.name}: '
                f'{self.ingredient.name} - '
                f'{self.amount} '
                f'{self.ingredient.measurement_unit}')

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_combination'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Добавил в избранное'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт'
    )

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


class Shopping_cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='Добавил в корзину'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
        verbose_name='Рецепт в корзине'
    )

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]
