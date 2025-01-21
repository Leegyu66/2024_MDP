from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.String(10))
    user_password = db.Column(db.String(128))
    user_name = db.Column(db.String(10))
    user_age = db.Column(db.DateTime)
    user_picture = db.Column(db.String(100))

    def set_password(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)


class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_date = db.Column(db.DateTime, default=datetime.today, onupdate=datetime.today)
    product_audio = db.Column(db.String(120), unique=True, nullable=False)
    product_word = db.Column(db.String(30))
    product_accuracy = db.Column(db.Integer)
    product_image = db.Column(db.String(100))
    modify_image = db.Column(db.String(100))
