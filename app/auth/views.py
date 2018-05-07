# coding: utf8
from flask import render_template, flash, redirect, url_for
from . import auth
from .. import db
from forms import RegistrationForm
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    form = LoginForm()
    flash(u'登陆成功')
    return render_template('login.html', title=u'登陆', form=form)


@auth.route('/logout')
def logout():
    pass


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data,
                    # email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', title=u'注册', form=form)