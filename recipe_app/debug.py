from ipdb import set_trace
from models import Recipe, Chef, Base, engine, Session

# Create the database tables
Base.metadata.create_all(engine)

# Initialize the database session
session = Session()

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
set_trace()
# Delete a recipe
if recipe:
    recipe.delete_recipe()

session.close()
