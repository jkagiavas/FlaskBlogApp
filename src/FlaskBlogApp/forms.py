
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from FlaskBlogApp.models import User

def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('Αυτο το email υπάρχει ήδη')

class SignupForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                       Length(min =3, max=15,message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="Εmail",
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                    Email(message="Παρακαλώ εισάγετε ένα σωστό Email"), validate_email])

    password = StringField(label="Password",
                           validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                       Length(min =3, max=15,message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    password2 = StringField(label="Επιβεβαίωση Password",
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                        Length(min =3, max=15,message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες"),
                                        EqualTo('password', message="Τα δύο πεδία pasword πρέπει να είναι τα ίδια")])
    submit = SubmitField("Εγγραφή")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Αυτο το username υπάρχει ήδη')

class LoginForm(FlaskForm):

    email = StringField(label="email",
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                    Email(message="Email")])

    password = StringField(label="Password",
                           validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό.")])

    submit = SubmitField("Είσοδος")


class NewArticleForm(FlaskForm):
    article_title = StringField(label="Τιτλος Άρθρου",
                           validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                      Length(min =3, max=50,message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    article_body = TextAreaField(label="Κείμενο Άρθρου",
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                    Length(min =5,message="Αυτό το πεδίο πρέπει να έχει τουλαχιστον 5 χαρακτήρες")])

    submit = SubmitField("Αποστολή")
