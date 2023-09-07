from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db= "recipes_db"
class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.thirty = data['thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.author = None
    
    @classmethod
    def add_recipe(cls,form_data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, thirty, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(thirty)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id;"
        result = connectToMySQL(db).query_db(query)
        recipes = []
        for row in result:
            one_recipe = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_recipe.author = user.User(user_data)
            recipes.append(one_recipe)
        return recipes
    
    @classmethod
    def recipe_by_id(cls,data):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False
        result = result[0]
        one_recipe = cls(result)
        user_data = {
            "id": result['users.id'],
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "email": result['email'],
            "password": "",
            "created_at": result['users.created_at'],
            "updated_at": result['users.updated_at']
        }
        one_recipe.author = user.User(user_data)
        return one_recipe
    

    @classmethod
    def save_changes(cls,form_data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, thirty = %(thirty)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def remove(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    
    
    @staticmethod
    def valid_recipe(form_data):
        is_valid = True
        if len(form_data['name']) < 2:
            flash("The name must be at least 2 characters long.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("The description must have a minimum of 3 characters.")
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash("Instructions must have a minimum of 3 characters.")
            is_valid = False
        if form_data['date_made'] == '':
            flash("Please enter date made.")
        if 'thirty' not in form_data:
            flash("Please give the cooking time.")
            is_valid = False
        return is_valid
    