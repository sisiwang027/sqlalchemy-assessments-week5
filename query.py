"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

# Answer: Datatype is object of Basequery.


# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

# Answer: An association table is a table connecting two tables with many to many 
#         relationship, and there are no meaningful fields in it. For example,
#         the relationship of table A and B is many to many, and table C is an association
#         of them. Table C connects the A and B with many to one relationship whith them. 

# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries

# Get the brand with the brand_id of ``ram``.
# another version: q1 = db.session.query(Brand).get('ram')
q1 = Brand.query.get('ram')

# Get all models with the name ``Corvette`` and the brand_id ``che``.
# another version: q2 = db.session.query(Model).filter(Model.name=='Corvette', Model.brand_id=='che').all()
q2 = Model.query.filter_by(name='Corvette', brand_id='che').all()

# Get all models that are older than 1960.
# another version: q3 = db.session.query(Model).filter(Model.year < 1960).all()
q3 = Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
# another version: q4 = db.session.query(Brand).filter(Brand.founded > 1920).all()
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
# another version: q5 = db.session.query(Model).filter(Model.name.like('Cor%')).all()
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
# another version: q6 = db.session.query(Brand).filter(Brand.founded == 1903, Brand.discontinued == None).all()
q6 = Brand.query.filter(Brand.founded == 1903, Brand.discontinued == None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
# another version: q7 = db.session.query(Brand).filter((Brand.founded < 1950) | (Brand.discontinued.isnot(None))).all()
q7 = Brand.query.filter(db.or_(Brand.founded < 1950, Brand.discontinued != None)).all()

# Get all models whose brand_id is not ``for``.
# another version: q8 = db.session.query(Model).filter(Model.brand_id != 'for').all()
q8 = Model.query.filter(Model.brand_id != 'for').all()

# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    #get all rows where , return a list of row objects.
    models = Model.query.filter(Model.year == year).options(db.joinedload('brand')).all()

    for model in models:
        print 'Model name: ' + model.name, '\n', 'Brand name' + model.brand.name, '\n', 'Brand headquarters: ' + model.brand.headquarters


def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    #left outerjoin brands and models.
    brands = Brand.query.options(db.joinedload('model')).all()

    for brand in brands:
        #iterate all brands

        print "Brand name: " + brand.name

        if brand.model:
            #for each brand, iterate its all models, and print them

            model_info = ''
            for one_model in brand.model:
                model_info = model_info + one_model.name + "(" + str(one_model.year) + ")" + "\t"
            print "Model info: " + model_info
        else:
            print "Model name: " + "--" + "(" + "--" + ")"


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    brands = Brand.query.filter(Brand.name.like('%{}%'.format(mystr))).all()

    return brands


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    models = Model.query.filter(Model.year >= start_year, Model.year < end_year).all()

    return models
