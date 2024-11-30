from database.db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_employee = db.Column(db.Boolean, default=False)

    def check_password(self, password):
        """Check if the provided password matches the stored password"""
        return self.password == password

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user by username and password"""
        user = cls.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
