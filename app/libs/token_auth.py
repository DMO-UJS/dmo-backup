from collections import namedtuple
from flask import current_app, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired, \
    BadSignature

from app.libs.error_code import AuthFailed

auth=HTTPBasicAuth()
User = namedtuple('User', ['uid',  'scope'])

@auth.verify_password
def verify_password(token,password):
    user_info = verify_auth_token(token)
    if not user_info or 'token is ' in user_info:
        return False
    else:
        g.user = user_info
        return True


#token解码
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid',
                         error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired',
                         error_code=1003)
    uid = data['uid']
    scope = data['scope']
    # request 视图函数
    # allow = is_in_scope(scope, request.endpoint)
    # if not allow:
    #     raise Forbidden()
    return User(uid,scope)
