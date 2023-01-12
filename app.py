from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()



@app.route('/', methods=['GET'])
def get_home():
  """
  Redirect to list of users
  """
  return redirect('/users')



@app.route('/users', methods=['GET'])
def get_users():
  """
  Show all users
  """

  users = User.query.filter()
  if users == None:
    users = []

  return render_template("users.html", users=users)



@app.route('/users/new', methods=['GET'])
def get_new_user():
  """
  Show an add form for users
  """

  return render_template("new_user.html")



@app.route('/users/new', methods=['POST'])
def post_new_user():
  """
  Process the add form
  """
  first_name = request.form["first-name"]
  last_name = request.form["last-name"]
  image_url = request.form["image-url"]

  new_user = User(first_name = first_name, last_name=last_name, image_url=image_url)

  db.session.add(new_user)
  db.session.commit()

  return redirect("/users")



@app.route('/users/<int:userid>', methods=['GET'])
def get_user_by_userid(userid):
  """
  Show information about the given user
  """

  user = User.query.get(userid)

  return render_template('display_user.html', user=user)



@app.route('/users/<int:userid>/edit', methods=['GET'])
def get_user_edit_form(userid):
  """
  Show the edit page for a user
  """
  user = User.query.get(userid)

  return render_template("edit_user.html", user=user)


@app.route('/users/<int:userid>/edit', methods=['POST'])
def post_user_edit_form(userid):
  """
  Process the edit form.
  """
  user = User.query.get(userid)

  user.first_name = request.form["first-name"]
  user.last_name = request.form["last-name"]
  user.image_url = request.form["image-url"]

  db.session.commit()

  return redirect("/users")



@app.route('/users/<userid>/delete', methods=['POST'])
def delete_user(userid):
  """Delete the user"""
  user = User.query.get(userid)
  db.session.delete(user)


  db.session.commit()

  return redirect("/users")

