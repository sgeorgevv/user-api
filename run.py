from api import app, db

"""
Deploy the API on a local server for development. 
"""
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
