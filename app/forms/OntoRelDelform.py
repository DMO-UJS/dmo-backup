from flask_wtf import Form
from wtforms import StringField, BooleanField, RadioField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class OntoRelDelForm(Form):
    onto_name =SelectField('onto_name',validators=[DataRequired(), Length(2, 20)])
    onto_rel =SelectField('onto_rel',validators=[DataRequired(), Length(2, 20)])


