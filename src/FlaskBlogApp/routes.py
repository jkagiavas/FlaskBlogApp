from flask import (render_template,
                   redirect,
                   url_for,
                   request,
                   flash)
from FlaskBlogApp.forms import SignupForm, LoginForm, NewArticleForm
from FlaskBlogApp import app, db, bcrypt
from FlaskBlogApp.models import User, Article


@app.route("/index/")
@app.route("/")
def root():
    articles = Article.query.all()
    return render_template("index.html", articles=articles)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        encrypted_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, email=email, password=encrypted_password)
        db.session.add(user)
        db.session.commit()

        flash(f"Ο Λογαριασμός του χρήστη <b>{username}</b> δημιουργήθηκε με επιτυχία")
        return redirect(url_for('login'))

    return render_template("signup.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    msg=""

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        print(email, password)
        flash(f"Η εισοδος του χρήστη με email {email} στην σελίδα μας έγινε με επιτυχία", "success")

    return render_template("login.html", form=form)


@app.route("/logout/")
def logout():
    return redirect(url_for("root"))


@app.route("/new_article/", methods=["GET", "POST"])
def new_article():
    form = NewArticleForm()

    if request.method == 'POST' and form.validate_on_submit():
        article_title = form.article_title.data
        article_body = form.article_body.data

        print(article_title, article_body)



    return render_template("new_article.html", form=form)

