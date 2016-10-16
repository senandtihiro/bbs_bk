from routes.user import current_user
from routes import *
from models.weibo import Weibo
from models.weibo_comment import WeiboComment
from models.blog_comment import BlogComment




# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('api', __name__)


@main.app_context_processor
def inject_permissions():
    return dict(u=current_user)


# /api/weibo/add
# @main.route('/weibo/', methods=['POST'])
# def add():
#     form = request.form
#     u = current_user()
#     weibo_list = Weibo.query.order_by(Weibo.id.desc()).all()
#
#     r = {
#         'data': []
#     }
#     if t.valid():
#         t.save()
#         r['success'] = True
#         r['data'] = t.json()
#     else:
#         r['success'] = False
#         message = t.error_message()
#         r['message'] = message
#     return json.dumps(r, ensure_ascii=False)

# @main.route('/')
# def index():
#     print('weibo index was called')
#     u = current_user()
#     if u is None:
#         return redirect(url_for('user.login_view'))
#     # 查找所有的 todo 并返回
#     weibo_list = Weibo.query.order_by(Weibo.id.desc()).all()
#     for weibo in weibo_list:
#         weibo.comments_num = len(weibo.comments)
#         print('打印每个微博的comment_number', weibo.comments_num)
#     # for i in weibo_list:
#     #     i.comment = i.comments()
#     #     for j in i.comment:
#     #         j.avatar = j.get_avatar()
#     #     i.comments_num = len(i.comment)
#     #     i.avatar = i.get_avatar()
#     return render_template('weibo_index_bk.html', weibos=weibo_list)


@main.route('/weibo/add', methods=['POST'])
def add():
    print('api.py weibo add was called')
    form = request.form
    u = current_user()
    t = Weibo(form)
    t.name = u.username
    r = {
        'data': []
    }
    if t.valid():
        t.save()
        print('api.weibo.add.r', r)
        print('api.weibo.add.t', t)
        r['success'] = True
        r['data'] = t.json()
    else:
        r['success'] = False
        message = t.error_message()
        r['message'] = message
    print('api.py weibo.add.response', r)
    return json.dumps(r, ensure_ascii=False)


# /api/weibo/update
@main.route('/weibo/update', methods=['POST'])
def update():
    form = request.form
    print('update中的form是：', form)
    # u = current_user()
    # t = Weibo(form)
    weibo_id = int(form.get('id', -1))
    print('微博的ID：',weibo_id)
    w = Weibo.query.get(weibo_id)
    print('update中取到的微博：',w)
    weibo = form.get('weibo', '')
    r = {
        'data': []
    }
    # if u.id != w.user_id:
    #     r['success'] = False
    print('get到的微博：',weibo)
    w.weibo = weibo
    w.save()
    print('新微博内容：',w.weibo)
    r['success'] = True
    r['data'] = w.json()
    print('r的内容',r)

    return json.dumps(r, ensure_ascii=False)

@main.route('/weibo/delete/<int:weibo_id>', methods=['GET'])
def delete(weibo_id):
    print('api.weibo.deleted was called')
    w = Weibo.query.get(weibo_id)
    w.delete()
    r = {
        'success': True,
        'data': w.json(),
    }
    return json.dumps(r, ensure_ascii=False)

@main.route('/weibo/comment', methods=['GET','POST'])
def weibo_comment():
    print('api.blog.comment was called')
    form = request.form
    u = current_user()
    c = WeiboComment(form)
    c.name = u.username
    c.user_id = u.id
    c.weibo_id = int(form.get('weibo_id', -1))
    print('评论微博的id：',c.weibo_id)
    r = {
        'data': []
    }
    if c.valid():
        c.save()
        print('评论保存成功',c)
        r['success'] = True
        r['data'] = c.json()
    else:
        r['success'] = False
        message = c.error_message()
        r['message'] = message
    print('评论中r的内容r的内容：：', r)
    return json.dumps(r, ensure_ascii=False)


@main.route('/blog/comment', methods=['GET','POST'])
def comment():
    print('api.blog.comment was called')
    form = request.form
    u = current_user()
    c = BlogComment(form)
    c.name = u.username
    c.user_id = u.id
    c.blog_id = int(form.get('blog_id', -1))
    print('评论博客的id：',c.blog_id)
    r = {
        'data': []
    }
    if c.valid():
        c.save()
        print('评论保存成功')
        r['success'] = True
        r['data'] = c.json()
    else:
        r['success'] = False
        message = c.error_message()
        r['message'] = message
    print('评论中r的内容r的内容：：', r)
    return json.dumps(r, ensure_ascii=False)

# @main.route('/weibo/comment', methods=['POST'])
# def comment():
#     u = current_user()
#     if u is not None:
#         form = request.form
#         c = Comment(form)
#         c.weibo_id = int(form.get('weibo_id', -1))
#         c.name = u.username
#         c.comment = form.get('comment', '')
#         c.save()
#         r = {
#             'success': True,
#             'data': c.json(),
#         }
#         return json.dumps(r, ensure_ascii=False)
#     else:
#         abort(401)

# TODO
"""
2016/9/14
因为我已经强化了代码
所以作业只需要实现两个功能
1，评论
2，更新微博

实现步骤如下
1，现在 api.py 里实现 api 功能（记住返回数据的格式要和 上面的 delete add 相同）
2，在 api.js 里实现 js api 功能（调用服务器，照猫画虎）
3，给 html 页面中的相应元素绑定功能，在 weibo.js 中
4，需要注意的是页面中每个微博都要添加一个 更新微博 按钮
    点击这个按钮后要 append 一个 input 一个 button
    button 需要提前用事件委托绑定一个事件（用来调用 api.js 中的更新微博函数）
"""
