# coding: utf8
from flask import render_template, url_for, redirect, request
from . import main
from ..models import Post, Comment
from .. import db
from flask_login import login_required, current_user
from form import CommentForm, PostForm
from flask_babel import gettext as _


@main.route('/')
def index():
    # posts = Post.query.all()
    page_index = request.args.get('page', 1, type=int)
    query = Post.query.order_by(Post.created.desc())
    pagination = query.paginate(page_index, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('index.html',
                           title=_(u'欢迎来到老子的博客'),
                           posts=posts,
                           pagination=pagination)


@main.route('/about')
def about():
    return 'about'


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def post(id):
    # Detail 详情页
    post = Post.query.get_or_404(id)
    # 评论窗体
    form = CommentForm()
    # 保存评论
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post)
        db.session.add(comment)
        db.session.commit()

    return render_template('posts/detail.html',
                           title=post.title,
                           form=form,
                           post=post)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()  # 表单实例化
    if id == 0:
        post = Post(author=current_user)  # 模型实例化
    else:
        post = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()  # 保存到库中

        return redirect(url_for('.post', id=post.id))
    title = _(u'添加新文章')
    if id > 0:
        title = _(u'编辑 - %(title)', title=post.title)  # 如果是post，则是编辑
    return render_template('posts/edit.html',
                           title=title,
                           form=form,
                           post=post)

# @main.template_test('current_link')
# def is_current_link(link):
#     return link == request.path
