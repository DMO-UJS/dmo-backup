from flask_wtf import Form
from wtforms import StringField, BooleanField, RadioField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class OntoRelAddForm(Form):
    onto_name = StringField('onto_name',validators=[DataRequired(), Length(2, 20)])
    corresponding=SelectField('corresponding',validators=[DataRequired(), Length(2, 20)])
    des_1 = StringField('des_1',validators=[DataRequired(), Length(1, 20)])
    des_2 = StringField('des_2',validators=[DataRequired(), Length(1, 20)])



