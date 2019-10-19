import os
import bson
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'myHunCuisine'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')

@app.route('/myHunCuisineDB')
def get_myHunCuisineDB():
     return render_template("huncuisine.html", myHunCuisineDB=mongo.db.myHunCuisineDB.find(), page_title="Edit Recipes")
     
@app.route('/get_categories')
def get_categories():
    return render_template('managecat.html', categories=mongo.db.categories.find())
    
@app.route('/get_categories_only')
def get_categories_only():
    return render_template('categories.html', categories=mongo.db.categories.find())    
    
@app.route('/get_images')
def get_images():
    return render_template('index.html', images=mongo.db.img_url.find())    
                          
@app.route('/base')
def get_base():
    return render_template("base.html")
    
@app.route('/index')
def get_index():
    return render_template("index.html", myHunCuisineDB=mongo.db.myHunCu_isineDB.find(), page_title="Main Page")
    
print(get_index)    
    
@app.route('/recipes')
def get_recipes():
    return render_template("recipes.html", myHunCuisineDB=mongo.db.myHunCuisineDB.find(), page_title="Recipes")    
    
@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html", get_categories=mongo.db.categories.find(), page_title="Add Your New Recipe")
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    myHunCuisineDB = mongo.db.myHunCuisineDB
    myHunCuisineDB.insert_one(request.form.to_dict())
    return redirect(url_for('get_myHunCuisineDB'))
    
@app.route('/insert_category', methods=['POST'])    
def insert_category():
    categories = mongo.db.categories
    categories.insert_one(request.form.to_dict())
   # category_doc = {'category_name': request.form.get['category_name']}
   # categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    
@app.route('/new_gategory')
def new_gategory():
    return render_template('addcategory.html')
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.myHunCuisineDB.find_one({"_id":ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=the_recipe, get_categories=mongo.db.categories.find(), page_title="Edit Recipes")

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories')) 
    
@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipe = mongo.db.myHunCuisineDB
    category = mongo.db.categories
    recipe.update( {'_id': ObjectId(recipe_id)},
    {
        'category_name':request.form.get('category_name'),
        'recipe_title':request.form.get('recipe_title'),
        'img_url': request.form.get('img_url'),
        'recipe_ingredients': request.form.get('recipe_ingredients'),
        'recipe_preparation': request.form.get('recipe_preparation'),
        'is_favourite':request.form.get('is_favourite')
    })
    return redirect(url_for('get_myHunCuisineDB')) 
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.myHunCuisineDB.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_myHunCuisineDB'))
    
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))    
    
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one(
                           {'_id': ObjectId(category_id)}))
 
 
 
   
    
if __name__ == '__main__':
    
   app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
          
            