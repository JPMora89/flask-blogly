"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

def connect_db(app):
        with app.app_context():
            db.app = app
            db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    def __repr__(self):
        return f"Id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, image_url: {self.image_url}, posts: {self.posts}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    posts = db.relationship('Post', cascade='all, delete, delete-orphan')

    def get_full_name(self):
        return f"{self.first_name}{self.last_name}"

        
class Post(db.Model):
  """A Post made by a User"""

  __tablename__ = "posts"

  def __repr__(self):
    content_str = self.content
    if len(self.content) > 30:
      content_str = f"{self.content}..."

    return f"Id: {self.id} title: {self.title} created_at: {self.created_at}  content: {content_str}"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String, nullable=False)
  content = db.Column(db.String, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now())
  author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

  author = db.relationship("User")
  tags = db.relationship("Tag", secondary="post_tags", backref="posts")
  

class Tag(db.Model):
  """Tags for Posts (M:M)"""
  __tablename__ = "tags"

  id = db.Column(db.Integer, unique=True, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  
  


class PostTag(db.Model):
  """Mapping of Posts to Tags"""

  __tablename__ = "post_tags"

  post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)

  tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)