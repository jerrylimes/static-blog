import os
import json
import markdown
from flask_frozen import Freezer
from flask import Flask, render_template, abort
from pathlib import Path

app = Flask(__name__)
app.config['FREEZER_RELATIVE_URLS'] = True

# Base route for the homepage


@app.route('/')
def index():
    post_files = os.listdir('posts/')
    posts = [post.replace('.html', '')
             for post in post_files if post.endswith('.html')]
    print(f"Posts: {posts}")  # Debugging line
    return render_template('index.html', posts=posts)

# Route for individual posts


# Load metadata.json
with open("metadata.json") as f:
    pages = json.load(f)

# Create a dictionary mapping filenames to metadata
page_dict = {p["filename"]: p for p in pages}


@app.route('/<path:post_name>.html')
def post(post_name):
    # Possible post locations
    possible_paths = [
        f"{post_name}.html",  # Check root directory
        f"posts/{post_name}.html"  # Check posts folder
    ]

    # Find the actual post path
    post_path = next((p for p in possible_paths if os.path.exists(p)), None)

    if not post_path:
        abort(404)

    try:
        with open(post_path, encoding="utf8") as file:
            content = file.read()

        # Find metadata for the current post
        page_data = page_dict.get(post_name + ".html", {})

        return render_template(
            "post.html",
            title=page_data.get("title", post_name.capitalize()),
            content=content,
            prev_page=page_data.get("prev"),
            next_page=page_data.get("next")
        )

    except FileNotFoundError:
        abort(404)


@app.route('/markdown/<path:filename>.html')
def render_markdown(filename):
    # Define the Markdown file path
    # Assuming a "markdown" folder in the root directory
    md_file_path = Path(f'markdown/{filename}.md')

    if md_file_path.exists():
        # Read the Markdown file
        with open(md_file_path, 'r') as md_file:
            md_file = open(md_file_path, encoding="utf8")
            content = md_file.read()

        # Convert Markdown to HTML with syntax highlighting
        html_content = markdown.markdown(
            content,
            # Add Pygments-based syntax highlighting
            extensions=['fenced_code', 'codehilite']
        )

        # Render the HTML inside a layout
        return render_template('markdown.html', content=html_content, title=filename.capitalize())
    else:
        abort(404)  # Return a 404 error if the file doesn't exist


freezer = Freezer(app)


if __name__ == '__main__':
    freezer.freeze()
