from flask_wtf import Form
from wtforms import StringField, BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length


class OntoAddForm(Form):
    onto_name = StringField('onto_name',validators=[DataRequired(), Length(2, 20)])

    pub_priv = RadioField('pub_priv')

