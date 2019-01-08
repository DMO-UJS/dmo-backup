from datetime import datetime
from flask import jsonify

from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.OntologyLibray import db



class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))
    create_time = Column(Integer)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @staticmethod
    def register_by_email(nickname, account, secret):
        user = User()
        user.nickname = nickname
        user.email = account
        user.password = secret
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFound(msg ='用户不存在!')
        if not user.check_password(password):
            raise AuthFailed(msg='密码错误！')
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id,'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)


    @staticmethod
    def modify_password(uid,secret):
        user = User.query.get(uid)
        user.password=secret
        db.session.commit()