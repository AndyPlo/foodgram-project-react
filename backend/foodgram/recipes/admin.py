from django.contrib import admin

from . import models


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit')
    list_filter = ('name', )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'text', 'cooking_time',
        'image', 'author', 'pub_date'
    )
    list_editable = (
        'name', 'cooking_time',
        'image', 'author'
    )
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'


@admin.register(models.Recipe_ingredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')
