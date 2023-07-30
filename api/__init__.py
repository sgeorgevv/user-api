from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine
import dotenv
import os

"""
Import the enviromental variables from the .env file.
"""
dotenv.load_dotenv("env_vars.env")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
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
Configure the app's database route to connect to a Mongo DB on a chosen host.
If a standard connection to a local Mongo DB is required, a hard coded host configuration can be used as such:
"mongodb://localhost:27017/{MONGO_DB}"
"""
app.config["MONGODB_SETTINGS"] = {
    'db': MONGO_DB,
    'host': f'mongodb://{MONGO_USER}:{MONGO_PASS}@{DB_SERVER}:{DB_PORT}/{MONGO_DB}'
}

"""
Initialize the connection to the Database. 
"""
db = MongoEngine(app)

from api import views