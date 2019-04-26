from flask_wtf import FlaskForm
from wtforms import StringField, StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class Post(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add to list book')


class UploadImage(FlaskForm):
    image = FileField('upload', validators=[DataRequired()])
    upload = SubmitField('Upload & Analyze')
