
from flask import Blueprint, current_app, jsonify, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, \
    BadSignature


from app.models.user import User
from app.validators.forms import ClientForm

token=Blueprint('token',__name__)


@token.route('/gettoken', methods=['POST'])
def get_token():
    data = request.json
    form = ClientForm(data=data)
    if form.validate():
        identity=User.verify(form.account.data,form.secret.data)
        expiration = current_app.config['TOKEN_EXPIRATION']
        token = generate_auth_token(identity['uid'],
                                    identity['scope'],
                                    expiration)
        t = {
            'token': token.decode('ascii')
        }
        return jsonify(t), 201


def generate_auth_token(uid, scope=None,
                        expiration=7200):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'scope':scope
    })