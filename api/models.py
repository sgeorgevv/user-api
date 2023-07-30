from . import db, SECRET_KEY
from flask_restful import request
from mongoengine import  StringField, EmailField
from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature
from functools import wraps
import re

"""
We define a standard schema for our Users collection to ensure all the user data stored is homogeneous.
Please add as many fields as neccessary, but don't forget to edit the end points in the views as possible.
"""

class Users(db.Document):
    username = StringField(required=True, max_length=120)
    email = EmailField(required=True, unique=True, max_length=120)
    password = StringField(required=True, max_length=120)
    
    meta = {"strict": True}

"""
Check if the password is strong. Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character
"""

def is_password_strong(password):
    password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.fullmatch(password_regex, password) is not None


"""
Token Generator and a wrapper to authenticate it. Generates a 30 minute token to be used as authentication for high level security endpoints. 
"""
def generate_token(username):
    serializer = Serializer(SECRET_KEY, 1800)
    return serializer.dumps({"username": username}).decode("utf-8")

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token:
            try: 
                serializer = Serializer(SECRET_KEY)
                decoded_token = serializer.loads(token)
                current_user = Users.objects(username=decoded_token["username"]).first()         
                if not current_user:
                    return {"Error": "User not found!"}, 401 
            except BadSignature:
                return {"Error" : "Access Token is invalid!"}, 401    
        else:
            return {"Error" : "Access Token is missing from your request!"}, 401
        

        return func(current_user, *args, **kwargs)
    
    return wrapper

