import csv
import os
from foodgram import settings

from django.core.management.base import BaseCommand
from progress.bar import IncrementalBar
from recipes.models import Ingredient


def ingredient_create(row):
    Ingredient.objects.get_or_create(
        name=row[0],
        measurement_unit=row[1]
    )


class Command(BaseCommand):
    help = "Load ingredients to DB"

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'ingredients.csv')
        with open(path, 'r', encoding='utf-8') as file:
            row_count = sum(1 for row in file)
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            bar = IncrementalBar('ingredients.csv'.ljust(17), max=row_count)
            next(reader)
            for row in reader:
                bar.next()
                ingredient_create(row)
            bar.finish()
        self.stdout.write("[!] The ingredients has been loaded successfully.")
