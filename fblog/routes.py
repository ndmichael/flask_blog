from flask import render_template, url_for, flash, redirect, request, abort
from fblog.forms import SignupForm, LoginForm, CreatePost, UpdatePost
from fblog import app, db, bcrypt
from fblog.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc
from secrets import token_hex
import os



def save_picture(form_picture):
    # return form_picture
    random_hex = token_hex(3)
    fname, fext = os.path.splitext(form_picture.filename)
    picture_file = fname + random_hex + fext
    pic_path = os.path.join(app.root_path, 'static/images', picture_file)
    form_picture.save(pic_path)
    return picture_file

    

#index route
@app.route("/")
@app.route("/home")
def index():
    blogs = Post.query.order_by(desc(Post.date_posted))
    return render_template("index.html", blogs=blogs, title="Home page")

#about route
@app.route("/about")
def about():
    return render_template("about.html")


#post details route
@app.route("/post/<int:id>")
@login_required
def post_details(id):
    post = Post.query.get_or_404(id)
    return render_template("post_details.html", post=post, title="post details")


# new post
@app.route("/create/post", methods=["GET", "POST"])
@login_required
def create_post():
    if not current_user.is_authenticated:
        flash(f'login to have access', 'info')
        return redirect(url_for('login'))
    form = CreatePost()
    if form.validate_on_submit():
        # image_file = save_picture(form.image.data.filename)
        # print(image_file)
        if form.image.data:
            print(form.image.data)
            image_file = save_picture(form.image.data)
            print(image_file)
            post = Post(title=form.title.data, content=form.content.data, image=image_file, author=current_user)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit() 
        flash(f'post created {form.title.data}', 'success')
        return redirect(url_for('index'))
    return render_template("create_post.html", form=form, title="new post")


# update post
@app.route("/update/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = UpdatePost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.image = save_picture(form.image.data)
        db.session.commit()
        flash(f"post updated", 'success')
        return redirect(url_for('post_details', id=post.id))
    else:
        form.title.data = post.title
        form.content.data = post.content
        form.image.data = post.image
        print(post.image)
    return render_template("update_post.html", form=form)


#delete post route
@app.route("/post/<int:post_id>/delete/", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f"{post.title} has been deleted", 'success')
    return redirect(url_for('index'))


#login route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'you are login as {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'wrong email and password', 'danger')
    return render_template("login.html", form=form, title="login")


# route for logout
@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash('you have been logged out', 'warning')
    return redirect('login')


#register route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        pw = form.password.data
        email = form.email.data
        username = form.username.data

        hashed_pw = bcrypt.generate_password_hash(pw)
        user = User(email=email, password=hashed_pw, username=username)
        db.session.add(user) # preparing it for saving
        db.session.commit() # saving it to table

        flash(f'Account created for {username}', 'success')
        return redirect(url_for('index'))
    return render_template("register.html", form=form, title="Register")
