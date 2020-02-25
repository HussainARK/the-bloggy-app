from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pathlib import Path

# Making the app:

app = Flask(__name__)

# Creating and connecting to the Database:

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


# Creating a Database Table as a Class:


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default='N/A')
    content = db.Column(db.Text, nullable=False, default='N/A')
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post' + str(self.id)


# Do routing and create views for Webpages:

# Routing and Creating the view of the Home Page:

@app.route('/')
def index():
    return render_template('index.html')

# Creating and Routing the view of the Posts Page:


@app.route('/posts/', methods=['GET', 'POST'])
@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']

        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts/')

    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

# Routing and Creating the view of the Deleting Page:


@app.route('/posts/delete/<int:id>/')
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/posts/')

# Routing and Creating the view of the Editing Page:


@app.route('/posts/edit/<int:id>/', methods=['GET', 'POST'])
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()

        return redirect('/posts/')
    else:
        return render_template('edit.html', post=post)

# Creating and Routing the Page that Creates a New Page:


@app.route('/posts/new/', methods=['GET', 'POST'])
@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts/')
    else:
        return render_template('new_post.html')

# Ceating and Routing the "About" Page:


@app.route('/about')
@app.route('/about/')
def about():
    return render_template('about.html')

# Doing Something but it's just a Good Practice:


if __name__ == "__main__":
    app.run(debug=False)

# End
