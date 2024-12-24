from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=250)])
    price = StringField('Price', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[DataRequired(), Length(max=1000)])
    image_url = StringField('Image URL', validators=[DataRequired(), Length(max=1200)])
    link_url = StringField('Link URL', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Post')