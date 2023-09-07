from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/welcome')
def main_user_page():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.user_by_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template('welcome.html', user=user, recipes=Recipe.all_recipes())

@app.route('/addrecipe/page')
def add_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('add_recipe.html')

@app.route('/makerecipe', methods=['POST'])
def make_recipe():
    if'user_id' not in session:
        return redirect('/logout')
    if not Recipe.valid_recipe(request.form):
        return redirect('/addrecipe/page')
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'thirty': int(request.form['thirty'])
    }
    Recipe.add_recipe(data)
    return redirect('/welcome')

@app.route('/logout')
def recipe_logout():
    session.clear()
    return redirect('/')

@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('show_recipe.html', recipe=Recipe.recipe_by_id({'id':id}))

@app.route('/editpage/<int:id>')
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('edit_recipe.html', recipe=Recipe.recipe_by_id({'id':id}))

@app.route('/editrecipe/<int:id>', methods=['POST'])
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Recipe.valid_recipe(request.form):
        return redirect(f'/editpage/{id}')
    data = {
        'id':id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'thirty': request.form['thirty']
    }
    Recipe.save_changes(data)
    return redirect('/welcome')

@app.route('/removerecipe/<int:id>')
def remove_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    Recipe.remove({'id':id})
    return redirect('/welcome')



