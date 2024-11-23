from flask_frozen import Freezer
from flask import Flask, render_template, abort
import os

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


freezer = Freezer(app)


if __name__ == '__main__':
    freezer.freeze()
