import functools
from flask.helpers import url_for
from werkzeug.utils import redirect
from transform.db import get_db
from flask import Blueprint, render_template, request, session, flash, g
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 로그인 view
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # fectchone() : 쿼리의 결과값 하나를 출력.
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username, )
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        # check_password_hash : password를 암호화하고, user['password']와 비교
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # error가 없다면 세션을 비우고 user의 id를 세션에 추가.
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('main.main'))

        # error 를 뿌려줌.
        flash(error)

    return render_template('auth/login.html')


# 로그아웃 view
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.main'))


# view 함수가 실행되기 전에 실행할 함수 지정
# 사용자가 어떤 URL을 요청하든 이 함수를 먼저 실행
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id, )
        ).fetchone()


# 사용자 인증을 요구하는 데코레이터
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
