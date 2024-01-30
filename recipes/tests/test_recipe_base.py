from django.test import TestCase
from recipes.models import Category, Recipe
from django.contrib.auth.models import User

class RecipeTestBase(TestCase):
    def setUp(self) -> None:
            category = Category.objects.create(
                name='Category'
            )
            author = User.objects.create(
                first_name='User',
                last_name='Test',
                username='userTest',
                password='test12345',
                email='user123@gmail.com',
            )
            recipe = Recipe.objects.create(
                category = category,
                author = author,
                title = 'Recipe test',
                description =' Recipe description test', 
                slug = 'recipe-test',
                preparation_time = 10,
                preparation_time_unit = 'Minutos', 
                servings = 1,
                servings_time = 'Mesa', 
                preparation_steps = 'Recipe preparation steps test', 
                preparation_steps_is_html = False, 
                is_published = True,
            )
            
            return super().setUp()
        