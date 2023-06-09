import os
import sys
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
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __repr__(self):
        return f'Recipe: {self.name}'

    @classmethod
    def get_all_recipes(cls):
        return session.query(cls).all()

    @classmethod
    def get_recipe_by_name(cls, name):
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def create_recipe(cls, name, ingredients, instructions, chef, category):
        recipe = cls(name=name, ingredients=ingredients, instructions=instructions, chef_id=chef.id, category_id=category.id)
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

    recipes = relationship("Recipe", backref="chef")

    def __repr__(self):
        return f'Chef: {self.name}'

    def get_recipes(self):
        return session.query(Recipe).filter_by(chef=self).all()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String())

    recipes = relationship("Recipe", backref="category")

    def __repr__(self):
        return f'Category: {self.name}'

    def get_recipes(self):
        return session.query(Recipe).filter_by(category=self).all()


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    # Create some instances
    chef1 = Chef(name='John', speciality='Italian Cuisine')
    chef2 = Chef(name='Jane', speciality='French Cuisine')

    category1 = Category(name='Breakfast')
    category2 = Category(name='Dinner')

    recipe1 = Recipe.create_recipe(
        name='Pancakes',
        ingredients='Flour, Milk, Eggs, Sugar',
        instructions='1. Mix all ingredients. 2. Cook on a griddle.',
        chef=chef1,
        category=category1
    )
    recipe2 = Recipe.create_recipe(
        name='Spaghetti Bolognese',
        ingredients='Ground beef, Onion, Garlic, Tomato sauce, Spaghetti',
        instructions='1. Brown the ground beef. 2. Saute onion and garlic. 3. Add tomato sauce. 4. Serve with cooked spaghetti.',
        chef=chef2,
        category=category2
    )

    # Get all recipes
    recipes = Recipe.get_all_recipes()
    for recipe in recipes:
        print(recipe)

    # Get recipe by name
    recipe = Recipe.get_recipe_by_name
