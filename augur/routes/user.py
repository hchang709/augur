import json
from flask import Flask, request, Response, send_from_directory, redirect, flash
from flask_login import LoginManager, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from ..models import User


#登录页面
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#将登录信息提交到服务器
def create_user_routes(server):
    @server.login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @server.app.route(f'/{server.api_version}/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        nxt = request.args.get('next')
        if form.validate_on_submit():
            user = User()
            login_user(user)
            flash('Logged in successfully.')
        return redirect(nxt or '/')
