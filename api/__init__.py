from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import dotenv
import os

"""
Import the enviromental variables from the .env file.
"""
dotenv.load_dotenv("api\env_vars.env")
SQL_DB = os.getenv("SQL_DB")
SQL_USER = os.getenv("SQL_USER")
SQL_PASS = os.getenv("SQL_PASS")
DB_SERVER = os.getenv("SERVER")
DB_PORT = os.getenv("PORT")
SECRET_KEY = os.getenv("SECRET_KEY")

"""
Initialize the RESTful API and configure the secret key for later use. 
"""
app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = SECRET_KEY

"""
Configure the app's database route to connect to an SQL DB on a chosen host.
"""
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{SQL_USER}:{SQL_PASS}@localhost/{SQL_DB}"


"""
Initialize the connection to the Database. 
"""
db = SQLAlchemy(app)

from api import views