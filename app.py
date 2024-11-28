import os
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


@app.route('/<path:post_name>.html')
def post(post_name):
    # The `post_name` will include the folder path if it's inside a folder like 'hello'
    post_path = f'{post_name}.html'  # Check the root directory first

    # If the post doesn't exist in the root, check the posts directory
    if not os.path.exists(post_path):
        post_path = f'posts/{post_name}.html'  # Check posts folder

    # If the post is inside a nested folder like posts/hello/
    if not os.path.exists(post_path):
        post_path = f'posts/{post_name}.html'

    try:
        with open(post_path, 'r') as file:
            content = file.read()
        return render_template('post.html', title=post_name.capitalize(), content=content, post_name=post_name)
    except FileNotFoundError:
        abort(404)


@app.route('/markdown/<path:filename>.md')
def render_markdown(filename):
    # Define the Markdown file path
    # Assuming a "markdown" folder in the root directory
    md_file_path = Path(f'markdown/{filename}.md')

    if md_file_path.exists():
        # Read the Markdown file
        with open(md_file_path, 'r') as md_file:
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
