#!/usr/bin/env python3
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Recipe, Chef, Category, Base, engine

engine = create_engine('sqlite:///db/recipes.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@click.group()
def func():
    pass


@click.command()
def list_recipes():
    recipes = Recipe.get_all_recipes()
    if recipes:
        click.echo("All Recipes:")
        for recipe in recipes:
            click.echo(recipe)
    else:
        click.echo("No recipes found")


@click.command()
def list_chefs():
    chefs = session.query(Chef).all()
    if chefs:
        click.echo("All Chefs:")
        for chef in chefs:
            click.echo(chef)
    else:
        click.echo("No chefs found")


@click.command()
def list_categories():
    categories = session.query(Category).all()
    if categories:
        click.echo("All Categories:")
        for category in categories:
            click.echo(category)
    else:
        click.echo("No categories found")


@click.command()
@click.option("--name", prompt="Enter the recipe name", help="Recipe name")
@click.option("--ingredients", prompt="Enter the ingredients", help="Recipe ingredients")
@click.option("--instructions", prompt="Enter the instructions", help="Recipe instructions")
@click.option("--chef-id", prompt="Enter the chef ID", help="Chef ID")
@click.option("--category-id", prompt="Enter the category ID", help="Category ID")
def add_recipe(name, ingredients, instructions, chef_id, category_id):
    recipe = Recipe.create_recipe(name=name, ingredients=ingredients, instructions=instructions,
                                  chef_id=chef_id, category_id=category_id)
    click.echo("Recipe added successfully")


func.add_command(list_recipes)
func.add_command(list_chefs)
func.add_command(list_categories)
func.add_command(add_recipe)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    func()
