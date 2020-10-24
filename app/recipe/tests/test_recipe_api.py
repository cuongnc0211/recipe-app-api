from django.contrib.auth import get_user_model
from django.tests import TestCase
from django.urls import TestCase

from rest_framework.test import APIClient
from rest_framework import test, status

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse('recipe:recipe-list')

def sample_recipe(user, **params):
    """Create and return a sample test"""
    defaults = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that unauthentication is required"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTest(TestCase):
    """Test authorized recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model.objects.create_user(
            'testuser@dev.com',
            'testpassword'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """test retrieve list of recipes"""

        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.get(RECIPE_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_recipes_for_user(self):
        """ test user retrieve own recipes"""
        user2 = get_user_model().objects.filter(user=self.user)
        sample_recipe(user=self.user)
        sample_recipe(user=user2)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
