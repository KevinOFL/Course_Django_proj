from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from recipes.tests.test_recipe_base import RecipeMixin
import time

class RecipebaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def sleep(self, seconds=3):
        time.sleep(seconds)
        
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()