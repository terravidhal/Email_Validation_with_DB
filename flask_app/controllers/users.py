from flask_app import app
from flask import Flask, render_template,redirect, request 
# import the class 'Users' from folder 'flask_app/models/user.py
from flask_app.models.user import Users 


@app.route("/")
def home():
   return redirect('/users/new')


@app.route("/users")
def index():
   users = Users.get_all()
   return render_template("index.html",all_Users = users)


@app.route("/users/new")
def create_new_user():
   return render_template("create.html")



@app.route('/new', methods=["POST"])
def create():
    datass = {
        "fname": request.form["inputName"],
        "lname": request.form["inputlast_name"],
        "eml": request.form["inputEmail"]
    }

    if not Users.validate_user_infos(datass): # ADD 'VALIDATE' METHOD USERS_INFOS
        return redirect("/")
    
    if not Users.is_unique_email(datass): # ADD 'VALIDATE' METHOD UNIQUE EMAIL
        return redirect("/")
    
    Users.create_user(datass)
    return redirect('/users')


@app.route('/user/show/<int:user_id>')
def show(user_id):
    data = {'id': user_id}
    user = Users.get_one(data)
    return render_template("show_user.html", User = user)
    


@app.route('/user/update/<int:user_id>')
def show_update_page(user_id):
    data = {'id': user_id}
    user = Users.get_one(data)
    return render_template("update_user.html", User = user)


@app.route('/edit/<int:user_id>',methods=['POST'])
def update(user_id):
    data = {
        'fname': request.form['NewFirstName'],
        'lname': request.form['NewLastName'],
        'eml': request.form['NewEmail'],
        'id': user_id
    }
    Users.update(data)
    return redirect(f'/user/show/{user_id}')



@app.route('/user/delete/<int:user_id>')
def delete(user_id):
    data = {"id": user_id}
    Users.delete(data)
    return redirect('/users')




    

