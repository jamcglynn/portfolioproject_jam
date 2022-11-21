from django.test import TestCase
#from users.models import User
#from django.contrib.auth.models import User
# Create your tests here.
from users.models import User


def create_new_user():
    new_email = 'jack1@gmail.com'
    return new_email

def test_create_new_user(new_user):
    assert create_new_user() != new_user
