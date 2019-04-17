from flask_wtf import FlaskForm
from wtforms import StringField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class Post(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add to list book')