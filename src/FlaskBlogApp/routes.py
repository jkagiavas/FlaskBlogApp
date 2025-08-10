from os import abort
from unicodedata import category

from flask import (render_template,
                   redirect,
                   url_for,
                   request,
                   flash)
from .forms import SignupForm, LoginForm, NewArticleForm, AccountUpdateForm, CommentForm
from . import app, db, bcrypt
from .models import User, Article, Category, Topic, Comment
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image

@app.errorhandler(404)
def page_not_found(e):
    # note that we ser the 404 status explicity
    return render_template('errors/404.html'), 404


@app.errorhandler(415)
def page_not_found(e):
    # note that we ser the 415 status explicity
    return render_template('errors/415.html'), 415

#το size είναι ένα tuple της μορφής (640,480)
def image_save(image, where, size):
    random_filename = secrets.token_hex(12)
    file_name , file_extension = os.path.splitext(image.filename)
    image_filename =random_filename + file_extension

    image_path =os.path.join(app.root_path, 'static/images', where, image_filename)

    img = Image.open(image)
    img.thumbnail(size)
    img.save(image_path)

    return image_filename

@app.route("/index/")
@app.route("/")
def root():
    page = request.args.get("page", 1, type=int)
    articles = Article.query.order_by(Article.date_created.desc()).paginate(per_page=2, page=page)
    return render_template("index.html", articles=articles)


@app.route("/articles_by_author/<int:author_id>")
def articles_by_author(author_id):

    user = User.query.get_or_404(author_id)

    page = request.args.get("page", 1, type=int)
    articles = Article.query.filter_by(author=user).order_by(Article.date_created.desc()).paginate(per_page=2, page=page)


    return render_template("articles_by_author.html", articles=articles, author=user)


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
    if current_user.is_authenticated:
        return redirect(url_for("root"))
    form = LoginForm()


    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"Η εισοδος του χρήστη με email {email} στην σελίδα μας έγινε με επιτυχία", "success")
            login_user(user, remember=form.remember_me.data)

            next_link = request.args.get("next")
            return redirect(next_link) if next_link else redirect(url_for("root"))
        else:
            flash("Η είσοδος του χρήστη ήταν ανεπιτυχής, παρακαλώ δοκιμάστε ξανά με τα σωστά email/password. ", "warning")

    return render_template("login.html", form=form)


@app.route("/logout/")
def logout():
    logout_user()
    flash("Εγινε αποσύνδεση του χρήστη", "success")
    return redirect(url_for("root"))


@app.route("/new_article/", methods=["GET", "POST"])
@login_required
def new_article():

    form = NewArticleForm()

    # Categories για χρήστη
    if current_user.username == "jkayabas_dev":
        form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    else:
        autism = Category.query.filter_by(name="Autism").first()
        form.category.choices = [(autism.id, 'Αυτισμός')] if autism else []

    # Topics αν η κατηγορία είναι Autism
    autism = Category.query.filter_by(name="Autism").first()
    if autism:
        form.topic.choices = [(t.id, t.name) for t in Topic.query.filter_by(category_id=autism.id).all()]

    if request.method == 'POST' and form.validate_on_submit():
        article_title = form.article_title.data
        article_body = form.article_body.data
        category_id = form.category.data
        topic_id = form.topic.data if category_id == autism.id and form.topic.data else None

        # image_save(image, where, size)
        if form.article_image.data:
            try:
                image_file = image_save(form.article_image.data, 'articles_images', (640, 360))
            except:
                abort(415)
            article = Article(article_title=article_title,
                              article_body=article_body,
                              author=current_user,
                              article_image=image_file,
                              category_id=category_id,
                              topic_id=topic_id
                              )

        else:
            article = Article(
                article_title=article_title,
                article_body=article_body,
                author=current_user,
                category_id=category_id,
                topic_id=topic_id
            )


        db.session.add(article)
        db.session.commit()

        flash(f"Το άρθρο με τίτλο «{article.article_title}» δημιουργήθηκε με επιτυχία", "success")
        return redirect(url_for("root"))



    return render_template("new_article.html", form=form, page_title="Εισαγωγή Νέου Άρθρου")


@app.route("/full_article/<int:article_id>", methods=["GET", "POST"])
def full_article(article_id):
    article = Article.query.get_or_404(article_id)

    form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Πρέπει να συνδεθείτε για να σχολιάσετε.", "danger")
            return redirect(url_for("login"))
        comment = Comment(
            content=form.content.data,
            author=current_user,
            article=article
        )
        db.session.add(comment)
        db.session.commit()
        flash("Το σχόλιό σας προστέθηκε!", "success")
        return redirect(url_for("full_article", article_id=article.id))

    comments = Comment.query.filter_by(article_id=article.id).order_by(Comment.date_posted.asc()).all()
    return render_template("full_article.html", article=article, comments=comments, form=form)


@app.route("/delete_article/<int:article_id>", methods=["GET", "POST"])
@login_required
def delete_article(article_id):

    article = Article.query.filter_by(id=article_id, author=current_user).first()

    if article:
        db.session.delete(article)
        db.session.commit()

        flash("Το άρθρο διεγράφει με επιτυχία.", "success")
        return redirect(url_for("root"))
    flash("Το άρθρο δεν βρέθηκε.", "warning")

    return redirect(url_for("root"))

@app.route("/account/", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm(username=current_user.username, email=current_user.email)

    if request.method == 'POST' and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        #image_save(image, where, size)
        if form.profile_image.data:
            try:
                image_file = image_save(form.profile_image.data, 'profiles_images', (150, 150))
            except:
                abort(415)

            current_user.profile_image = image_file

        db.session.commit()

        flash(f"Ο λογαριασμός του χρήστη <b>{current_user.username}</b> ενημερώθηκε με επίτυχία", "success")

        return redirect(url_for('root'))
    return render_template("account_update.html", form=form)

@app.route("/edit_article/<int:article_id>", methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()

    form = NewArticleForm(article_title=article.article_title, article_body=article.article_body)

    if request.method == 'POST' and form.validate_on_submit():
        article.article_title = form.article_title.data
        article.article_body = form.article_body.data

        # image_save(image, where, size)
        if form.article_image.data:
            try:
                image_file = image_save(form.article_image.data, 'articles_images', (640, 360))
            except:
                abort(415)

            article.article_image =  image_file


        db.session.commit()

        flash(f"Το άρθρο με τίτλο <b>{article.article_title} </b>ενημερώθηκε με επιτυχία.", "success")

        return redirect(url_for('root'))
    return render_template("new_article.html", form=form, page_title="Επεξεργασία Άρθρου")

@app.route('/autism')
def autism():
    category = Category.query.filter_by(name='Autism').first_or_404()
    topics = Topic.query.filter_by(category_id=category.id).all()
    articles = Article.query.filter_by(category_id=category.id).order_by(Article.date_created.desc()).all()
    return render_template('autism.html', category=category, topics=topics, articles=articles)

@app.route('/autism/topic/<string:topic_name>')
def topic_articles(topic_name):
    topic = Topic.query.filter_by(name=topic_name).first_or_404()
    articles = Article.query.filter_by(topic_id=topic.id).order_by(Article.date_created.desc()).all()
    return render_template('topic_articles.html', topic=topic, articles=articles)

@app.route('/autism/topic_redirect')
def topic_articles_redirect():
    topic_name = request.args.get('topic_name')
    if topic_name:
        return redirect(url_for('topic_articles', topic_name=topic_name))
    return redirect(url_for('autism'))

@app.route('/projects')
def projects():
    category = Category.query.filter_by(name='Projects').first_or_404()
    user = User.query.filter_by(username='jkayabas_dev').first()
    if not user:
        flash("Ο χρήστης jkayabas_dev δεν βρέθηκε.", "warning")
        return redirect(url_for('home'))

    articles = Article.query.filter_by(category_id=category.id, user_id=user.id).order_by(Article.date_created.desc()).all()
    return render_template('projects.html', articles=articles)
