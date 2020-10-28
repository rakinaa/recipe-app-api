from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='test@gmail.com', password='testpass'):
  """Create a sample user"""
  return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

  def test_create_user_with_email_successful(self):
    """test creating a new user with an email is successful"""
    email = 'test@gmail.com'
    password = "pass123"
    user = get_user_model().objects.create_user(
      email=email,
      password=password
    )

    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))
  
  def test_new_user_email_normalized(self):
    """test the email is normalized"""
    email = 'test@gmaIl.com'
    user = get_user_model().objects.create_user(
      email=email,
      password='test123'
    )

    self.assertEqual(user.email, email.lower())

  def test_new_user_invalid_email(self):
    """test no email raises error"""
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(email=None, password='test123')

  def test_tag_str(self):
    """test tag string representation"""
    email = 'test@gmail.com'
    password = "pass123"
    tag = models.Tag.objects.create(
      user=sample_user(),
      name='vegan'
    )

    self.assertEqual(str(tag), tag.name)

  def test_ingredient_str(self):
    """test ingredient string representation"""
    ingredient = models.Ingredient.objects.create(
      user=sample_user(),
      name='cucumber'
    )

    self.assertEqual(str(ingredient), ingredient.name)

  def test_recipe_str(self):
    """test recipe string representation"""
    recipe = models.Recipe.objects.create(
      user=sample_user(),
      title='steak',
      time_minutes=5,
      price=5.00,
    )

    self.assertEqual(str(recipe), recipe.title)

  @patch('uuid.uuid4')
  def test_recipe_file_name_uuid(self, mock_uuid):
    """Test that image is save in the correct location"""
    uuid = 'test-uuid'
    mock_uuid.return_value = uuid
    file_path = models.recipe_image_file_path(None, 'myimage.jpg')

    exp_path = f'uploads/recipe/{uuid}.jpg'
    self.assertEqual(file_path, exp_path)