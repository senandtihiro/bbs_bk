from models import *


from . import ModelMixin
from . import db
from utils.utils import encript_password


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    # avatar = db.Column(db.String())
    salt = db.Column(db.String())
    avatar = db.Column(db.String(200), default='/static/avatar/default_avatar.gif')
    is_administrator = db.Column(db.Boolean, default=False, index=True)
    nodes = db.relationship('Node', backref='user')
    topics = db.relationship('Topic', backref='user')
    comments = db.relationship('Comment', backref='user')
    blog_comments = db.relationship('BlogComment', backref='user')
    weibo_comments = db.relationship('WeiboComment', backref='user')


    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')


    def valid(self):
        print('valid was called')
        user = User.query.filter_by(username=self.username).first()
        # print('user', user)
        # if user is not None:
        #     return False
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password
        # return u.username == self.username and u.password == self.password

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False


    # def get_avatar(self, filepath):
    #     with open(filepath, 'rb') as f:
    #         self.avatar = f.read()
    #     return self.avatar

    # def change_avatar(self, filename):
    #     self.avatar = send_from_directory('uploads/', filename)
    #     self.save()

    def change_avatar(self, avatar):
        print('change_avatar was called')
        print('length of avatar > 2?', len(avatar))
        print('change_avatar was called')
        if len(avatar) > 2:

            self.avatar = avatar
            self.save()
            return True
        else:
            return False


                # def valid_login(self, u):
    #     if u is not None:
    #         username_equals = u.username == self.username
    #         password_equals = u.password == self.password
    #         return username_equals and password_equals
    #     else:
    #         return False
    #
    # # 验证注册用户的合法性的
    # def valid(self):
    #     valid_username = User.query.filter_by(username=self.username).first() == None
    #     valid_username_len = len(self.username) >= 6
    #     valid_password_len = len(self.password) >= 6
    #     valid_captcha = self.captcha == '3'
    #     msgs = []
    #     if not valid_username:
    #         message = '用户名已经存在'
    #         msgs.append(message)
    #     elif not valid_username_len:
    #         message = '用户名长度必须大于等于 6'
    #         msgs.append(message)
    #     elif not valid_password_len:
    #         message = '密码长度必须大于等于 6'
    #         msgs.append(message)
    #     elif not valid_captcha:
    #         message = '验证码必须输入 3'
    #         msgs.append(message)
    #     status = valid_username and valid_username_len and valid_password_len and valid_captcha
    #     return status, msgs
