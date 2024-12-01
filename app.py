import os
from dotenv import load_dotenv
from flask import Flask
# from flask_mysqldb import MySQL
from flask_login import LoginManager
from database.db import db, init_db
from controllers.icecreamshop_controller import icecreamshop_blueprint
from controllers.ingredient_controller import ingredient_blueprint
from controllers.product_controller import product_blueprint
from controllers.user_controller import user_blueprint
from models.user import User

file_path = os.path.join(os.path.abspath(os.getcwd()), "database", "site.db")

# load_dotenv()
app = Flask(__name__, template_folder="views")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + file_path
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_LINK")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")

login_manager = LoginManager(app)
login_manager.login_view = "user.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.init_app(app)
# uncomment to reset db data
# init_db(app)
app.register_blueprint(icecreamshop_blueprint)
app.register_blueprint(ingredient_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    app.run(debug=False)
