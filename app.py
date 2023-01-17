from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug=True
toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
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

@app.route('/users/<int:userid>/posts/new', methods=['GET'])
def get_blog_post_form(userid):
  """Show form to add a post for that user."""
  user = User.query.get(userid)
  all_tags = db.session.query(Tag).all()

  return render_template('new_blog_form.html', user=user, all_tags=all_tags)


@app.route('/users/<int:userid>/posts/new', methods=['POST'])
def take_blog_post_form(userid):
  """Take blog post"""
  post = Post(title=request.form['title'], content=request.form['content'].replace("%0D%0A", "\n"),  author_id=userid)
    
  tag_ids = request.form.getlist("tag")
  post.tags = []

  for tag_id in tag_ids:
    tag = Tag.query.get(int(tag_id))
    post.tags.append(tag)

  db.session.add(post)
  db.session.commit()

  return redirect(f"/users/{userid}")


@app.route('/posts/<int:postid>', methods=['GET'])
def get_post(postid):
  """Show blog post"""
  post = Post.query.get(postid)

  return render_template('display_post.html', post=post)


@app.route('/posts/<int:postid>/edit', methods=['GET'])
def get_edit_post(postid):
  """get edit post form"""
  post = Post.query.get(postid)
  all_tags = db.session.query(Tag).all()

  return render_template('edit_blog_form.html', post=post, all_tags=all_tags)


@app.route('/posts/<int:postid>/edit', methods=['POST'])
def post_edit_post(postid):
  """accept post for post edit"""
  post=Post.query.get(postid)
  
  post.title = request.form['title']
  post.content = request.form['content'].replace("%0D%0A", "\n")

  tag_ids = request.form.getlist("tag")
  post.tags = [] 

  for tag_id in tag_ids:
    tag = Tag.query.get(int(tag_id))
    post.tags.append(tag)


  db.session.commit()
  return redirect(f"/users/{post.author_id}")


@app.route('/posts/<int:postid>/delete', methods=['POST'])
def delete_post(postid):
  """Delete a post"""
  post = Post.query.get(postid)
  user_id = post.author_id
  db.session.delete(post)
  db.session.commit()
  
  return redirect(f"/users/{user_id}")
  
  
@app.route('/tags', methods=['GET'])
def get_tags():
  """List all tags, with links to the tag detail page"""

  tags = db.session.query(Tag).all()

  return render_template('tags.html', tags=tags)



@app.route('/tags/<int:tagid>', methods=['GET'])
def get_tag(tagid):
  """Show detail about a tag. Have links to edit form and to delete"""
  tag = Tag.query.get(tagid)

  return render_template('tag_detail.html', tag=tag)


@app.route('/tags/new', methods=['GET'])
def get_tag_form():
  """Show a form to add a new tag"""
  return render_template('new_tag.html')


@app.route('/tags/new', methods=['POST'])
def post_tag_form():
  """Process add form, adds tag, and redirect to tag list"""
  try:
    tag = Tag(name=request.form["tag-name"])
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")
  except:
    return render_template("/error.html", msg="You may have tried to create a tag that already exists.")


@app.route('/tags/<int:tagid>/edit', methods=['GET'])
def get_tag_edit_form(tagid):
  """Show edit form for a tag"""
  tag = Tag.query.get(tagid)

  return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tagid>/edit', methods=['POST'])
def post_tag_edit_form(tagid):
  """Process edit form, edit tag, and redirect to the tags list"""
  tag = Tag.query.get(tagid)
  tag.name = request.form["tag-name"]
  db.session.commit()

  return redirect(f"/tags/{tagid}")


@app.route('/tags/<int:tagid>/delete', methods=['POST'])
def delete_tag(tagid):
  """Delete a tag"""
  tag = Tag.query.get(tagid)
  db.session.delete(tag)
  db.session.commit()

  return redirect("/tags")