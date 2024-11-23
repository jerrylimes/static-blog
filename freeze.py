from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()

@freezer.register_generator
def post():
    posts = ["my-first-post", "learning-flask"]
    for post_slug in posts:
        yield {"post_slug": post_slug + ".html"}