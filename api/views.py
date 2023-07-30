from flask_restful import Resource, reqparse, abort
from werkzeug.security import generate_password_hash, check_password_hash
from . import api
from .models import Users, token_required, generate_token, is_password_strong

class Register(Resource):
    """
    This class handles the creation of new users. It requires a username, password, and email address.
    """
    def post(self):
        """
        This method handles the POST request to register a new user.
        """
        parser = reqparse.RequestParser()
        
        parser.add_argument("username", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)
        
        body = parser.parse_args()
        
        # Validate username
        if body.get("username"):
            new_username = body.get("username")
        else:
            return {"Error": "Please include a username in your request."}, 400
        
        # Validate password
        if not body.get("password"):
            return {"Error": "Please include a password in your request."}, 400

        if not is_password_strong(body.get("password")):
            return {"Error": "Your password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character."}, 400
        
        # Validate email
        if body.get("email"):
            new_email = body.get("email")
        else:
            return {"Error": "Please include a email in your request."}, 400
    
        # Attempt to create a new user
        try:
            new_user = Users(
                username = new_username,
                email = new_email,
                password = generate_password_hash(body.get("password"), method= "pbkdf2:sha256", salt_length=8))
            new_user.save()
            
        except Exception as error:
            abort(500, description=f"An error occurred while processing your request: {error}")

        return {"Success": "User added successfully"}, 201


class Login(Resource):
    """
    This class handles the login of existing users. It requires a username and password.
    """
    def post(self):
        """
        This method handles the POST request to login a user.
        """
        parser = reqparse.RequestParser()

        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)

        body = parser.parse_args()

        username = body.get("username")
        password = body.get("password")

        # Validate username and password
        if not username:
            return {"Error": "Please include a username in your request."}, 400
        if not password:
            return {"Error": "Please include a password in your request."}, 400

        # Attempt to find the user in the database
        try:
            current_session_user = Users.objects(username=username).first()  
        except Exception as error:
            abort(500, description=f"An error occurred while processing your request: {error}")

        # If user is found, check the password and return an auth token
        if current_session_user:
            hashed_password = current_session_user.password

            if check_password_hash(hashed_password, password):
                token = generate_token(username)
                return {"Please use this access token in your headers for authorized requests. It's valid for 30 minutes.": token}
            else:
                return {"Error": "Incorrect password."}, 401
        else:
            return {"Error": "Username doesn't exist."}, 404


class UserData(Resource):
    """
    This class handles the retrieval and updating of user data. 
    """
    method_decorators = [token_required]
    def get(self, current_user):
        """
        This method handles the GET request to retrieve a user's data.
        """
        return {
            "Username": current_user.username,
            "Email" : current_user.email
        }
    
    def patch(self, current_user):
        """
        This method handles the PATCH request to update a user's data.
        """
        parser = reqparse.RequestParser()

        parser.add_argument("data_to_change", type=dict)
        parser.add_argument("password", type=str)

        body = parser.parse_args()

        data_to_change = body.get("data_to_change")
        password = body.get("password")
        
        # Validate password and update the data
        if check_password_hash(current_user.password, password):
            for field in data_to_change:
                if not hasattr(current_user, field):
                    return {"Error": f"{field.title()} isn't a valid field."}, 400

            for field in data_to_change:
                if field == "password":
                    current_user.password = generate_password_hash(data_to_change["password"], method= "pbkdf2:sha256", salt_length=8)
                else:
                    current_user[field] = data_to_change[field]

            current_user.save()
            return {"Success": "Data has been updated successfully."}, 200
        else:
            return {"Error": "Invalid password."}, 400


# Adding resources to the api
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(UserData, "/user-data")
