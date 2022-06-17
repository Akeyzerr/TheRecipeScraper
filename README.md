# Task: Python Recipe Web Scraper
---
## Code Academy Team 4
### V.Georgiev, R.Kostov, A.Toporchev

# Project requirements
  
1. **Recipe scraping:**
- [Scraping target](https://recepti.gotvach.bg "Gotvach.bg")
- Get the proper n recipes depending on the input and collect them in a chosen data structure.

2. **Data processing:**
- [x] The data must be filtered depending on the allergens
- [x] The data must be sorted
- [x] The formatted data must be stored in a file

3. **Output:**
- [x] The data must be stored in a file and sent to be represented in a Google Sheet
- [x] The format of the representation is not predefined
- [ ] Graphical representation of the data

4. **Overall requirements:**
- [ ] Tests
- [x] Documentation
- [x] OOP design
- [ ] Modules:
    - [x] requests,
    - [x] beautifulsoup4 
    - [x] pandas 
    - [x] OAuth 
    - [x] GSpread 

## _Input example_
_Proper inputs should include:_
- n - number of recipes (required)
- product(s)
- dish name
- last cooked
- allergens 

Example:
```
    python main.py -n <number of dishes> -p <products>
    python main.py -n <number of dishes> -d <dish>
    python main.py -n <number of dishes> -l <last cooked>
    python main.py -a <allergens>
```
## Models
All models have implementation of methods that expand the received data. 
#### Chef
Prototype data class that holds a single chef data and calculates chef popularity as per assignment. The model has _le__ and __eq__ methods implemented for sorting as per assignment.

#### Ingredient
Prototype data class that holds a single ingredient entry data - name, quantity and unit of measurement. The model has _le__ and __eq__ methods used for sorting.

#### Recipe
Recipe - prototype data class that holds a single recipe data; the model has __lt__, __eq__ methods implemented for sorting of the requested recipes. This can be realized in a pandas DataFrame over a class prototype for speed and convenience at a later stage. The model has builtin functionality to map received recipe ingredients with a prebuilt allergens array.


## Modules
#### Settings
Classes for every other module, providing ad hoc features and single point of configuration of the IO params
    - argParser Settings Module - _Singleton_ class to provide the values (names) of the parameters ("-n", "-l", "-a", etc.)
    - General Settings Module - general purpose class that currently delivers timeout values to the modules that use _requests_  

#### argParser 
Handles the sys.argv array, stores and provides the values to other modules in a jit fashion. This module expects only correct input as a GUI (facade) will most likely be implemented at some point. 

#### FulfillInquiry
Executive producer module that orchestrates the execution of the program. 

#### SetupRequest
Builder class that constructs the recipe basae URL for the GetRecipeLink generator.

#### GetRecipeLink
Builder class that constructs a single recipe URL for the scraper. This module handles the scraping target pagination and delivers links on next() call.

#### RecipeRequestParser
Factory class that parses the requested html for use in the builder modules.

#### ChefBuilder
Builder class that constructs Chef object from given RecipeRequestParser data.

#### IngredientsBuilder
Builder class that constructs Ingredient object from given RecipeRequestParser data.

#### RecipeIngredients
Storage class that holds multiple Ingredient objects. This storage class has comparison methods implemented used for the sorting.

#### RecipeBuilder
Builder class that constructs Recipe object from given RecipeRequestParser data, Ingredients and Chef object.

#### RecipeStorage
Container class for Recipe objects. That module is WIP and will be able to export the data in several file formats.

#### GSUploader
Handles the data upload to GSheet.

#### CLI/TUI
Module that represents the collected data to the user and provides UI for the sorting, export to JSON file and upload.


## __Project structure__
Project structure :
```
recipes-scraper/
    |--- data/
        |--- allergens.py
        |--- measurements.py
    |--- modules/
        |--- models/
            |--- chef.py
            |--- ingredient_entry.py
            |--- recipe.py
            |--- recipe_ingredients.py
        |--- __init__.py
        |--- argparser.py
        |--- chef_builder.py
        |--- fulfill_inquiry.py
        |--- get_recipe_link.py
        |--- gs_upload.py
        |--- handlers.py
        |--- ingredients_builder.py
        |--- menu.py
        |--- recipe_builder.py
        |--- recipe_request_parser.py
        |--- recipe_storage.py
        |--- settings.py
        |--- setup_request.py
        |--- validators.py
    |--- project_exceptions/
        |---argParser_exceptions.py
    |--- test/
        |--- unit_tests/
            |--- __init__.py
            |--- test_argparser.py
    |--- __init__.py
    |--- .gitignore
    |--- main.py
    |--- README.md
    |--- requirements_py2.txt
    |--- requirements_py3.txt
  ```