import os
from flask import Flask, render_template
from flask_frozen import Freezer
from markupsafe import Markup

app = Flask(__name__)
freezer = Freezer(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/blog")
def blog():
    posts = []
    for filename in os.listdir("posts"):
        if filename.endswith(".html"):
            with open(os.path.join("posts", filename)) as f:
                content = f.read()
                title = os.path.splitext(filename)[0].replace("-", " ").title()
                posts.append({"title": title, "content": Markup(content)})
    return render_template("blog.html", posts=posts)


@app.route("/blog/<post_slug>.html")
def post(post_slug):
    post_file = f"posts/{post_slug}.html"
    if os.path.exists(post_file):
        with open(post_file) as f:
            content = Markup(f.read())
            title = post_slug.replace("-", " ").title()
            return render_template("post.html", title=title, content=content)
    else:
        return "Post not found", 404


if __name__ == '__main__':
    freezer.freeze()

if __name__ == '__main__':
    app.run(debug=True)
