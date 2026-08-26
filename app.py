from datetime import timedelta
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db, User, Transaction
from dotenv import load_dotenv

load_dotenv()

#Import blueprints
from auth import auth
from dashboard import main

app= Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=30)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Please login first."

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app.register_blueprint(auth)
app.register_blueprint(main)

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)