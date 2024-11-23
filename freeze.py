from app import app  # Import your Flask app from app.py
from flask_frozen import Freezer

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()  # This will generate the static files
