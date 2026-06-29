"""
    Author: Jerry Li, Claude
    Date: 2025-03-22
    Version: 0.1
"""

from flask import Flask, render_template, abort
from flask_frozen import Freezer
from jinja2 import ChoiceLoader, FileSystemLoader
import markdown
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
    md_path = os.path.join("posts", f"{post_name}.md")
    html_path = os.path.join("posts", f"{post_name}.html")
    if os.path.exists(md_path):
        with open(md_path, encoding="utf8") as file:
            content = markdown.markdown(file.read(), extensions=["codehilite", "fenced_code"])
        return render_template("post.html", content=content)
    elif os.path.exists(html_path):
        with open(html_path, encoding="utf8") as file:
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
            yield {"post_name": file_name[:-5]}
        elif file_name.endswith(".md"):
            yield {"post_name": file_name[:-3]}


if __name__ == "__main__":
    freezer.freeze()
