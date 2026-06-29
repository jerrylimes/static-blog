"""
    Author: Jerry Li
    Date: 2025-03-22
    Version: 0.1
"""

from flask import Flask, render_template, abort
from flask_frozen import Freezer
from jinja2 import ChoiceLoader, FileSystemLoader
import os

app = Flask(__name__, template_folder="assets/templates")

app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader("common/templates")
])

# Serve static files from the 'assets' folder
app.static_folder = "assets"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/posts/<post_name>.html")
def serve_post(post_name):
    post_path = os.path.join("posts", f"{post_name}.html")
    if os.path.exists(post_path):
        # Read the post content here and pass it to the template
        with open(post_path, "r") as file:
            file = open(post_path, encoding="utf8")
            content = file.read()
        return render_template("post.html", content=content)
    else:
        abort(404)  # Return a 404 error if the post doesn't exist


freezer = Freezer(app)

# Register generator for dynamic posts


@freezer.register_generator
def serve_post():
    # List all files in the 'posts' directory
    posts_dir = "posts"
    for file_name in os.listdir(posts_dir):
        if file_name.endswith(".html"):
            # Pass the post name without '.html'
            yield {"post_name": file_name[:-5]}


if __name__ == "__main__":
    freezer.freeze()
