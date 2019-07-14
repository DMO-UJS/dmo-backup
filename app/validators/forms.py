from wtforms import Form, StringField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.models.user import User


class ClientForm(Form):
    account=StringField(validators=[DataRequired(),length(min=3,max=30)])
    secret=StringField()




class  UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{3,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()

class  UserPswForm(Form):
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{3,22}$')
    ])
    uid = StringField(validators=[DataRequired()])
