from flask import Blueprint, request

from app.models.OntologyLibray import db
from app.models.user import User

from app.validators.forms import ClientForm, UserEmailForm

client=Blueprint('client',__name__)


@client.route('/register',methods=['POST'])
def create_client():
    data=request.json
    form=ClientForm(data=data)
    if form.validate():
        __register_user_by_email()
        return 'success'
    else:
        return 'Failed'


def __register_user_by_email():
    form=UserEmailForm(data=request.json)
    if form.validate():
        User.register_by_email(form.nickname.data,form.account.data,form.secret.data)


