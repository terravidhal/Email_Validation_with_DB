from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re  # the regex module



class Users:
    DB = 'users_schema'
    def __init__(self, data):
        self.id = data["idusers"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.created_at = data["created_at"].strftime("%B %drd %Y %H:%M:%S %p")
        self.updated_at = data["updated_at"].strftime("%B %drd %Y %H:%M:%S %p")

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users_Arr = []
        for one_user in results:
            #print('one_user++++++++',one_user)
            users_Arr.append(cls(one_user))
            #print(cls(one_user))
        return users_Arr
    

    @classmethod
    def create_user(cls, datas):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(eml)s, NOW(), NOW());"
        results = connectToMySQL(cls.DB).query_db(query, datas)
        user_id_created = results
        return user_id_created 

    # READ
    # ONE elt
    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM users WHERE idusers = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    # UPDATE
    @classmethod
    def update(cls,data):
        query = """UPDATE users 
                SET first_name=%(fname)s, last_name=%(lname)s, email=%(eml)s , updated_at = NOW() 
                WHERE idusers = %(id)s;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    

    # DELETE        
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM users WHERE idusers = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    

    # VALIDATE USER INFOS
    @staticmethod
    def validate_user_infos(data):
        NAME_REGEX = re.compile(r'^[a-zA-Z]{2,15}$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if not NAME_REGEX.match(data['fname']):
            flash("Invalid first name")
            is_valid = False
        if not NAME_REGEX.match(data['lname']):
            flash("Invalid last name")
            is_valid = False
        if not EMAIL_REGEX.match(data['eml']):
            flash("Invalid email address")
            is_valid = False

        return is_valid
    

    # NINJA Bonus: Also validate that the email being added is unique
    @classmethod
    def is_unique_email(cls, data):
        query = "SELECT email FROM users;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        is_valid = True
        for elt in results:
            #print(elt)  
            if elt["email"] == data["eml"]:
                flash("Email already exists")
                is_valid = False
               
        return is_valid
    
    