"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy


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

        
