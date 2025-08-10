from typing import Optional

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from .models import User, Category, Topic
from flask_login import current_user


def maxImageSize(max_size=2):
    max_bytes = max_size * 1024 * 1024
    def _check_file_size(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f'Το μέγεθος της εικόνας δε μπορεί να υπερβαίνει τα {max_size} ΜΒ')
    return _check_file_size

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
    remember_me = BooleanField(label="Remember me")

    submit = SubmitField("Είσοδος")


class NewArticleForm(FlaskForm):
    article_title = StringField(label="Τιτλος Άρθρου",
                           validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                      Length(min =3, max=50,message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    article_body = TextAreaField(label="Κείμενο Άρθρου",
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                    Length(min =5,message="Αυτό το πεδίο πρέπει να έχει τουλαχιστον 5 χαρακτήρες")])
    article_image = FileField('Εικόνα Προφίλ', validators=[Optional('strip_whitespace=True'),
                                                           FileAllowed(['jpg', 'jpeg', 'png'],
                                                                       'Επιτρέπονται μονο αρχεία τύπου jpg, jpeg και png'),
                                                           maxImageSize(max_size=2)])
    category = SelectField('Κατηγορία', coerce=int)

    # Αυτό για τα Topics, μόνο αν είναι Autism
    topic = SelectField('Topic', coerce=int, choices=[], validate_choice=False)

    submit = SubmitField('Αποστολή')




class AccountUpdateForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                       Length(min =3, max=15,message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="Εmail",
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                                    Email(message="Παρακαλώ εισάγετε ένα σωστό Email")])
    profile_image = FileField('Εικόνα Προφίλ', validators=[Optional('strip_whitespace=True'),
                                                           FileAllowed(['jpg', 'jpeg', 'png'],
                                                                       'Επιτρέπονται μονο αρχεία τύπου jpg, jpeg και png'),
                                                                       maxImageSize(max_size=2)])

    submit = SubmitField("Αποστολή")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Αυτο το username υπάρχει ήδη')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Αυτό το email υπάρχει ήδη')

class CommentForm(FlaskForm):
    content = TextAreaField(
        'Σχόλιο',
        validators=[
            DataRequired(message="Το σχόλιο δεν μπορεί να είναι κενό."),
            Length(min=2, max=500, message="Το σχόλιο πρέπει να έχει 2 έως 500 χαρακτήρες.")
        ]
    )
    submit = SubmitField('Προσθήκη Σχολίου')