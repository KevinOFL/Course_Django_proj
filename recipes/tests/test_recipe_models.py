from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelsTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_default(self):
        recipe = Recipe(
            category = self.make_category(name='salade'),
            author = self.make_author(username='Tio Test'),
            title = 'Recipe test',
            description =' Recipe description test', 
            slug = 'recipe-test',
            preparation_time = 10,
            preparation_time_unit = 'Minutos', 
            servings = 1,
            servings_time = 'Mesa', 
            preparation_steps = 'Recipe preparation steps test', 
        )
        recipe.full_clean()
        recipe.save()
        return recipe


    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_time', 65),
    ])
    def test_recipe_fields_max_lenght(self, field, max_lenght):
        setattr(self.recipe, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.preparation_steps_is_html, 
            msg='Recipe is preparation_steps_is_html is not False'
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False'
        )