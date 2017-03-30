from models.user import User
from routes import *
from app import UPLOAD_FOLDER
from flask import Flask
from functools import wraps
# from app import UPLOAD_FOLDER
from flask import g
from uuid import uuid3, NAMESPACE_DNS
from PIL import Image
from flask import current_app
from utils.utils import encript_password
from utils.utils import generate_salt


main = Blueprint('user', __name__)

pyid = id
Model = User

def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        # print('user', u)
        return u


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        # your code
        print('login required')
        u = current_user()
        if u is None:
            return render_template('user_login.html')
        print('login_required u', u)
    return function


@main.route('/')
def login_view():
    u = current_user()
    # print('u:', u)
    if u is not None:
        return redirect('/node/show')
        # return render_template('node.html')
    return render_template('user_login.html')

@main.route('/register_view')
def register_view():
    return render_template('user_register.html')

@main.route('/register', methods=['GET','POST'])
def register():
    print('register was called')
    form = request.form
    u = User(form)
    u.salt = generate_salt()
    u.password = encript_password(u.password, u.salt)
    if u.valid():
        print('u is valid')
        # u.save()
        print('u.username',u.username)
        if u.username == 'ahe':
            u.is_administrator = True
            print('u.is_administrator', u.is_administrator)
        else:
            u.is_administrator = False
        u.save()
        print('register u.password:',u.password)
    else:
        abort(400)
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
    user = User.query.filter_by(username=u.username).first()
    # print('login user.password', user.password)
    if user is not None and user.validate_login(user):
        print('登录成功')
        session['user_id'] = user.id
    else:
        print('登录失败')
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/logout')
# @login_required
def logout():
    print('logout was called')
    # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
    session.pop('user_id')
    user = current_user()
    print('logout u', user)
    if user is not None:
        print('登出失败')
    else:
        print('登出成功')
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/update_password', methods=['POST'])
def update_password():
    u = current_user()
    password = request.form.get('password', '123')
    if u.change_password(password):
        print('修改成功')
    else:
        print('用户密码修改失败')
    return redirect('/user/profile')


# @main.route('/upload_avatar', methods=['POST'])
# def upload_avatar():
#     u = current_user()
#     file = request.files['file']
#     if file:
#         filename = u.username + file.filename
#         file.save(os.path.join(UPLOAD_FOLDER, filename))
#     # return redirect(url_for('uploaded_file', filename=filename))
#     return redirect(url_for('update_avatar', filename=filename))

# @main.route('/uploads/<filename>')
# def uploaded_file(filename):
#     print('uploaded_file was called', uploaded_file)
#     return send_from_directory(UPLOAD_FOLDER, filename)


# @main.route('/update_avatar/<filename>')

# @main.route('/upload_avatar', methods=['POST'])
# def upload_file():
#     f = request.files.get('uploaded')
#     u = current_user()
#     if f:
#         filename = f.filename
#         # path = UPLOAD_FOLDER + filename
#         # f.save(path)
#         # u.avatar = '/' + path
#         PROJECT_DIR = os.path.abspath(os.path.dirname(__name__))
#         print('PROJECT_DIR:', PROJECT_DIR)
#         # C:\Users\pc\Documents\bbs_bk
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         print('filepath:', filepath)
#         savepath = os.path.join(PROJECT_DIR, filepath)
#         print('savepath:', savepath)
#         # C:/static/avatar/background1.jpg
#         u.avater = filepath
#         f.save(savepath)
#
#         # full_path = project_path + path
#         # u.avatar = full_path
#         u.save()
#         return redirect('/user/profile')
#     else:
#         return '<h1>没有上传</h1>'

@main.route('/upload_avatar', methods=['POST'])
def upload_file():
    print('upload')
    # 通过 request.files 访问上传的文件
    # uploaded 是上传时候的文件名
    f = request.files.get('uploaded')
    u = current_user()
    print(request)
    print('upload, ', request.files)
    if f:
        filename = u.username + f.filename
        print('filename, ', filename)
        path = UPLOAD_FOLDER + filename
        print(os.getcwd())
        f.save(path)
        # full_path =
        u.avatar = '/' + path
        # u.avatar = path
        u.save()
        print('debug path:', u.avatar)
        print('file was successfully saved')
        return redirect('/user/profile')
    else:
        return '<h1>没有上传</h1>'



# upload_avatar
# @main.route('/upload_avatar', methods=['POST'])
# def update_avatar():
#     u = current_user()
#     filename = request.files['file'].filename
#     img = Image.open(request.files['photo'])
#     format = img.format
#     filename = save_avatar(img, filename, format)
#     url_path = current_app.config['UPLOADED_PHOTOS_URL']
#     u.avatar = url_path + filename
#     u.save()
#     # avatar = request.form.get('avatar', '')
#     # filename = avatar.save(sub_img, folder=folder_name, name='avatar.jpg')
#     # print('avatar is none', avatar is None)
#     # if u.change_avatar(avatar):
#     #     print('用户头像修改成功')
#     # else:
#     #     print('用户头像修改失败')
#     return redirect('/user/profile')
#
#
# def save_avatar(img, filename, format):
#     path = current_app.config['UPLOADED_PHOTOS_DEST']
#     p = os.path.join(path, filename)
#     save_all = False
#     append_image = []
#     if type(img) == list:
#         save_all = True
#         append_image = img[1:]
#         img = img[0]
#
#     img.save(p + '.' + format.lower(), save_all=save_all, append_images=append_image)
#
#     return filename + '.' + format.lower()





# @main.route('/upload_avatar', methods=['post'])
# # @user_required
# def upload_avatar():
#     print('upload_avatar was called')
#     # u = g.user
#     u = current_user()
#     print('debug request.files:', request.files)
#     print('debug photo in request.files:', 'photo' in request.files)
#     if 'photo' in request.files:
#         form = request.form
#         filename = str(uuid3(NAMESPACE_DNS, str(u.id) + u.username + str(time.time()))).replace('-','')
#         try:
#             # x = int(form['x'])
#             # y = int(form['y'])
#             # w = int(form['nw'])
#             # h = int(form['nh'])
#             img = Image.open(request.files['photo'])
#             format = img.format
#             # croped_img = crop_img(img, x, y, w, h)
#             filename = save_avatar(img, filename, format)
#             url_path = current_app.config['UPLOADED_PHOTOS_URL']
#             old_name = u.avatar.split(url_path)[1]
#             # remove_avatar(old_name)
#             u.avatar = url_path + filename
#             u.save()
#         except Exception as e:
#             print(e)
#             print('请上传大小不超过2Mb的图片文件', 'error')
#     # return redirect(url_for('user.setting_view'))
#     return redirect('/user/profile')
#
# def save_avatar(img, filename, format):
#     path = current_app.config['UPLOADED_PHOTOS_DEST']
#     p = os.path.join(path, filename)
#     save_all = False
#     append_image = []
#     if type(img) == list:
#         save_all = True
#         append_image = img[1:]
#         img = img[0]
#
#     img.save(p + '.' + format.lower(), save_all=save_all, append_images=append_image)
#
#     return filename + '.' + format.lower()



# @main.route('/upload_avatar', methods=['POST'])
# def upload_avatar():
#     print('upload_avatar was called')
#     file = request.files['file']
#     if file:
#         filename = file.filename
#         file.save(os.path.join(UPLOAD_FOLDER, filename))
#     return redirect(url_for('.update_avatar', filename=filename))


# @main.route('/update_avatar/<string:filename>', methods=['GET', 'POST'])
# def update_avatar(filename):
#     u = current_user()
#     if u.change_avatar(filename):
#         print('修改成功')
#     else:
#         print('用户头像修改失败')
#     return redirect('/user/profile')





@main.route('/profile', methods=['GET'])
# @login_required
def profile():
    print('frofile was called')
    u = current_user()
    if u is not None:
        # print('profile', u.id, u.username, u.password)
        return render_template('profile.html', user=u)
    else:
        abort(401)
