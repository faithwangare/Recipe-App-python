import os
import sys

sys.path.append(os.getcwd())
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///db/recipes.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    ingredients = Column(Text)
    instructions = Column(Text)
    chef_id = Column(Integer, ForeignKey('chefs.id'))

    chef = relationship("Chef", backref="recipes")

    def __repr__(self):
        return f'Recipe: {self.name}'

    @classmethod
    def get_all_recipes(cls):
        return session.query(cls).all()

    @classmethod
    def get_recipe_by_name(cls, name):
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def create_recipe(cls, name, ingredients, instructions, chef):
        recipe = cls(name=name, ingredients=ingredients, instructions=instructions, chef=chef)
        session.add(recipe)
        session.commit()
        return recipe

    def update_recipe(self, name=None, ingredients=None, instructions=None):
        if name:
            self.name = name
        if ingredients:
            self.ingredients = ingredients
        if instructions:
            self.instructions = instructions
        session.commit()

    def delete_recipe(self):
        session.delete(self)
        session.commit()


class Chef(Base):
    __tablename__ = 'chefs'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    speciality = Column(String())

    def __repr__(self):
        return f'Chef: {self.name}'

    def get_recipes(self):
        return session.query(Recipe).filter_by(chef=self).all()


Base.metadata.create_all(engine)


if __name__ == '__main__':
    # Create some instances
    chef1 = Chef(name='John', speciality='Italian Cuisine')
    chef2 = Chef(name='Jane', speciality='French Cuisine')

    recipe1 = Recipe.create_recipe(
        name='Pancakes',
        ingredients='Flour, Milk, Eggs, Sugar',
        instructions='1. Mix all ingredients. 2. Cook on a griddle.',
        chef=chef1
    )
    recipe2 = Recipe.create_recipe(
        name='Spaghetti Bolognese',
        ingredients='Ground beef, Onion, Garlic, Tomato sauce, Spaghetti',
        instructions='1. Brown the ground beef. 2. Saute onion and garlic. 3. Add tomato sauce. 4. Serve with cooked spaghetti.',
        chef=chef2
    )

    # Get all recipes
    recipes = Recipe.get_all_recipes()
    for recipe in recipes:
        print(recipe)

    # Get recipe by name
    recipe = Recipe.get_recipe_by_name('Pancakes')
    if recipe:
        print(recipe.ingredients)
        print(recipe.instructions)

    # Update a recipe
    if recipe:
        recipe.update_recipe(ingredients='Flour, Milk, Eggs, Sugar, Vanilla extract')

    # Delete a recipe
    if recipe:
        recipe.delete_recipe()

    session.close()
