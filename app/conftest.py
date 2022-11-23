import pytest 

@pytest.fixture
def new_user():
    email = 'jack@gmail.com'
    return email

@pytest.fixture
def new_recipe():
    recipe = 'Caramelized Brussel Sprouts'
    return recipe 
