# coding: utf8
from flask import render_template, request
from . import main


@main.route('/')
def hello_world():
    return render_template('index.html', title='welcome')


@main.route('/about')
def about():
    return 'about'


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# @main.template_test('current_link')
# def is_current_link(link):
#     return link == request.path
