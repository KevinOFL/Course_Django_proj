from django.test import TestCase
from recipes.models import Category, Recipe
from django.contrib.auth.models import User

class RecipeTestBase(TestCase):
    def setUp(self) -> None:
            return super().setUp()
        
    def make_category(self, name='Categoria'):
          return Category.objects.create(name=name)
    
    def make_author(
        self,
        first_name='User',
        last_name='Test',
        username='userTest',
        password='test12345',
        email='user123@gmail.com',
    ):
        return User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email=email,
            )
    
    def make_recipe(
        self,
        category_data = None,
        author_data = None,
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
    ):
        if category_data is None:
             category_data = {}

        if author_data is None:
             author_data = {}
        
        return Recipe.objects.create(
                category = self.make_category(**category_data),
                author = self.make_author(**author_data),
                title = title,
                description =description, 
                slug = slug,
                preparation_time = preparation_time,
                preparation_time_unit = preparation_time_unit, 
                servings = servings,
                servings_time = servings_time, 
                preparation_steps = preparation_steps, 
                preparation_steps_is_html = preparation_steps_is_html, 
                is_published = is_published,
        )