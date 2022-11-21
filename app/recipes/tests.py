from django.test import TestCase
import pytest
#from users.models import User
#from django.contrib.auth.models import User
# Create your tests here.
from users.models import User


def create_new_recipe():
    create_recipe = 'Caramlized Brussel Sprouts'
    return create_recipe

@pytest.mark.xfail
def test_create_new_recipe(create_recipe):
    assert new_recipe == create_recipe
