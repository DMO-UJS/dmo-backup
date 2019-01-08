from flask import Blueprint, jsonify, request

from app.libs.error_code import PswModSuccess, ParameterException
from app.libs.token_auth import auth
from app.models.user import User
from app.validators.forms import ClientForm, UserPswForm

user=Blueprint('user',__name__)


@user.route('/user/<int:uid>',methods=['GET'])
@auth.login_required
def get_user(uid):
    user=User.query.get(uid)
    if not user:
        return jsonify('用户不存在!')
    r={
        'nickname':user.nickname,
        'email':user.email
    }
    return jsonify(r),201

@user.route('/login',methods=['POST'])
def user_login():
    data = request.json
    form = ClientForm(data=data)
    if form.validate():
        identity = User.verify(form.account.data, form.secret.data)
        user = User.query.get(identity['uid'])
        user_info={
            'uid':identity['uid'],
            'auth':identity['scope'],
            'nickname':user.nickname
        }
        return jsonify(user_info), 201

@user.route('/pswmod',methods=['POST'])
def user_psw_mod():
    form = UserPswForm(data=request.json)
    if form.validate():
        User.modify_password(form.uid.data,form.secret.data)
        return PswModSuccess()
    else:
        return ParameterException()
    pass