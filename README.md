# RESTful API with Flask, Flask-RESTful, and MySQL

This is a simple RESTful API developed with Flask and Flask-RESTful, using MongoDB as the database via MYSQLAlchemy. It's a basic user management system where you can register new users, login with registered users, and get or update the user's data. All user passwords are securely hashed before being stored.

## Features

- User registration with server-side validation for password strength
- Login system with hashed password comparison
- Generation of a unique access token upon successful login
- Token-based user authentication
- Ability for users to get and update their data

## How to Run

1. Clone the repository.
2. Install the required dependencies found in the `requirements.txt` file using `pip install -r requirements.txt`.
3. Ensure you have a running MYSQL instance and fill in the `env_vars.env` file.
4. Run the application with `python run.py`.

## Endpoints

- `POST /register`: Register a new user. The request body should include `username`, `email`, and `password`.
- `POST /login`: Login as an existing user. The request body should include `username` and `password`.
- `GET /user-data`: Get the data of the logged-in user. The request should include the access token in the headers.
- `PATCH /user-data`: Update the data of the logged-in user. The request should include the access token in the headers, and the request body should include `data_to_change` (a dictionary of fields to change) and `password`.

Please note that all the request and response bodies should be in JSON format.

## Contribution

Feel free to fork the project, make some updates, and submit pull requests. Feedback is always welcome.

## License

This project is licensed under the terms of the MIT license.
