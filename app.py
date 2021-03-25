"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'helloworld'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def show_user_list():
    """Show all users in database """
    post = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.j2', users=users, post=post)

@app.route('/users/new')
def show_add_user_form():
    return render_template('form.j2')

@app.route('/', methods=["POST"])
def create_user():
    """ Create User """
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name,image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>')
def show_user_page(user_id):
    """ Show User Page """
    try:
        user = User.query.get_or_404(user_id)
        post = Post.query.filter(Post.user_id == user_id).all()
        return render_template('user.j2', user=user, post=post)
    except:
        return render_template('404.j2')

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """ Show Edit Form """
    user = User.query.get_or_404(user_id)
    return render_template('edit.j2', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """ Update User """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    if request.form["image_url"] == "":
        user.image_url = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
    else:
        user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def remove_user(user_id):
    """Remove User from Database """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')


@app.route('/users/<int:user_id>/posts/new')
def render_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post.j2', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    if request.form["title"] == "" or request.form["content"] == "":
        flash("Please fill in the form completely")
        return redirect(f'/users/{user.id}/posts/new')
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route('/posts/<int:post_id>')
def show_user_post(post_id):
    """ Render Single Post """
    post = Post.query.get_or_404(post_id)
    return render_template('single-post.j2', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """ Render Edit Post Form """
    tags = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.j2', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.form["title"] == "" or request.form["content"] == "":
        flash("Please fill in the form completely")
        return redirect(f'/posts/{post.id}/edit')
    post.title = request.form["title"]
    post.content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")



@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def remove_post(post_id):
    """Remove Post from Database """
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


@app.route('/tags')
def render_tag_template():
    """ Render Tags Template """
    tags = Tag.query.all()
    return render_template('tags.j2', tags=tags)

@app.route('/tags/new', methods=["GET", "POST"])
def render_tag_form():
    """ Render Tag Form """
    if request.method == "POST":
        if request.form["name"] == "":
            flash("Please fill in the form completely")
            return redirect('/tags/new')
        tag = request.form["name"]
        new_tag = Tag(name=tag)
        db.session.add(new_tag)
        db.session.commit()
        return redirect('/tags')
    else:   
        return render_template('tag-form.j2')

@app.route('/tags/<int:tag_id>')
def render_tag_page(tag_id):
    """ Render Individual Tag Page """
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.j2', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag_form(tag_id):
    """ Render Edit Tag Form """
    tag = Tag.query.get_or_404(tag_id)
    if request.method == "POST":
        if request.form["name"] == "":
            flash("Please fill in the form completely")
            return redirect(f"/tags/{tag_id}/edit")
        tag.name = request.form["name"]
        db.session.add(tag)
        db.session.commit()
        return redirect('/tags')
    else:
        return render_template('edit-tag.j2', tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def remove_tag(tag_id):
    """Remove Tag from Database """
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect(f'/tags')