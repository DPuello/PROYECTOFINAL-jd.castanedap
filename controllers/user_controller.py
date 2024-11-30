from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user
from models.user import User
from database.db import db

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@user_blueprint.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    is_admin = request.form.get('is_admin', False)
    is_employee = request.form.get('is_employee', False)

    # Check if username and password are provided
    if not username or not password:
        return jsonify({
            "error": "Missing credentials", 
            "message": "Username and password are required"
        }), 400

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({
            "error": "Username taken",
            "message": "This username is already registered"
        }), 409

    # Create new user
    is_admin = is_admin != False
    is_employee = is_employee != False
    new_user = User(username=username, password=password, is_admin=is_admin, is_employee=is_employee)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)

    return redirect(url_for("icecreamshop_bp.index"))


@user_blueprint.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@user_blueprint.route("/login", methods=["POST"]) 
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if username and password are provided
    if not username or not password:
        return jsonify({
            "error": "Missing credentials",
            "message": "Username and password are required"
        }), 400

    # Authenticate user using class method
    user = User.authenticate(username, password)
    if not user:
        return jsonify({
            "error": "Invalid credentials",
            "message": "Invalid username or password"
        }), 401

    login_user(user)
    return redirect(url_for("user.welcome"))

@user_blueprint.route("/welcome", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@user_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("user.login"))

@user_blueprint.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")

