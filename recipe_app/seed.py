import os
import sys
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Chef, Recipe, Base

faker = Faker()

sys.path.append(os.getcwd())
engine = create_engine('sqlite:///db/recipes.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# Create some instances
chef1 = Chef(name='John', speciality='Italian Cuisine')
chef2 = Chef(name='Jane', speciality='French Cuisine')
session.add(chef1)
session.add(chef2)
session.commit()

# Create recipes using Faker
for _ in range(10):
    name = faker.word()
    ingredients = faker.text(max_nb_chars=200)
    instructions = faker.text(max_nb_chars=500)
    chef = faker.random_element([chef1, chef2])
    recipe = Recipe.create_recipe(name=name, ingredients=ingredients, instructions=instructions, chef=chef)
    session.add(recipe)

session.commit()
session.close()

print("Seed data has been created successfully!")
