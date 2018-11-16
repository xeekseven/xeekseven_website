import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from xeekwebsite_server.db import get_db
import uuid
from xeekwebsite_server.util import execption_handle
from xeekwebsite_server.LogFactory import LogInfo

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
@execption_handle
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            author_id = str(uuid.uuid1())
            db.execute(
                'INSERT INTO user (username, password, author_id) VALUES (?, ?, ?)',
                (username, generate_password_hash(password),author_id)
            )
            db.execute('INSERT INTO author (author_id,author_name,headimg) VALUES (?, ?, ?)',
                (author_id,'xer','#'))
            db.commit()
            LogInfo().logger.info('/auth/register 注册用户:%s' % username)
            return redirect(url_for('auth.login'))
        LogInfo().logger.error('/auth/register 发生了错误:%s' % str(error))
        flash(error)
        
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
@execption_handle
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect username.(账号不正确)...'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.(密码不正确)...'
        
        if error is None:
            session.clear()
            session['user_id'] = user['author_id']
            #,userinfo={ 'username':username,'author_id':author_id }
            LogInfo().logger.info('/auth/register 用户登录:%s' % username)
            return redirect(url_for('home.index'))
        LogInfo().logger.error('/auth/register 发生了错误:%s' % str(error))
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
@execption_handle
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE author_id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
@execption_handle
def logout():
    session.clear()
    return redirect(url_for('home.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view