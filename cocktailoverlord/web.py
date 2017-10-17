from db import CocktailDB
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from urllib.parse import quote, unquote

app = Flask(__name__, static_folder="img")
db = CocktailDB("tmp.sqlite3")
c=db.get_available_cocktails()

@app.route("/")
def cocktail_overview():
    return render_template('main.html',
                           cocktails=db.get_available_cocktails())

def search_list(ingredients):
    if len(ingredients) == 0:
        possible = db.cocktail_ingredients(db.get_available_cocktails())
    else:
        possible = db.cocktail_ingredients(db.find_cocktail_using_all_ingredients(ingredients))
    
    return render_template('search.html',
                           searching=sorted(ingredients),
                           possible=sorted(set(possible) - set(ingredients)),
                           cocktails=db.find_cocktail_using_all_ingredients(ingredients))

@app.template_filter('add_search_ingredient')
def add_search_ingredient(s,new):
    return set(s) | set([new])

@app.template_filter('del_search_ingredient')
def del_search_ingredient(s,new):
    return set(s) - set([new])

@app.template_filter('create_search_path')
def create_search_path(s):
    return '/'.join([quote(i) for i in s])

@app.route("/search/<path:searchpath>")
def search(searchpath):
    ingredients = set([ unquote(p) for p in searchpath.split("/") ])

    return search_list(ingredients)
    
@app.route("/search")
@app.route("/search/")
def search_start():
    return search_list([])

@app.route("/refill", methods=["GET", "POST"])
def refill():
    if request.method == 'GET':
        return render_template('refill.html',
                               locations=db.storage(),
                               ingredients=db.ingredients()
        )
    else:
        print(request.form)
        v = {}
        for key,value in request.form.items():
            storage, attribute = key.split('.')
            if not storage in v:
                v[storage] = { attribute: value }
            else:
                v[storage][attribute] = value
        print(v)
        for storage, contents in v.items():
            if contents['ingredient'] == '':
                db.set_storage_contents(storage, None, 0)
            else:
                db.set_storage_contents(storage, contents['ingredient'], contents['amount'])
        return render_template('refill.html',
                               locations=db.storage(),
                               ingredients=db.ingredients())

if __name__ == '__main__':
    app.debug=True
    app.run()
