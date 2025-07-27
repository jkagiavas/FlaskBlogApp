from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(30), default ='default_profile_image.jpg')

    articles = db.relationship('Article', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.username}: {self.email}"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    articles = db.relationship('Article', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    articles = db.relationship('Article', backref='topic', lazy=True)

    def __repr__(self):
        return f"<Topic {self.name}>"



class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    article_title = db.Column(db.String(50), nullable=False)
    article_body  = db.Column(db.Text(), nullable=False)
    article_image = db.Column(db.String(30), default ='default_article_image.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=True)
    comments = db.relationship('Comment', backref='article', lazy=True)

    def __repr__(self):
        return f"{self.date_created}: {self.article_title}"



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)

    def __repr__(self):
        return f"Comment by {self.user_id} on article {self.article_id}"