import os
import secrets
from flask import Flask, send_from_directory
from path import UPLOAD_DIR_PATH
from . import main
from . import order
from . import db
from . import auth
from . import upload
from . import distribution


def create_app():
    # instance_relative_config=True -> app에게 설정파일은 instance 폴더에 있다. (설정값, DB파일 등)
    app = Flask(__name__, instance_relative_config=True)

    # instance 폴더가 없으면 생성
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # upload_files 폴더가 없으면 생성
    try:
        os.makedirs(UPLOAD_DIR_PATH)
    except OSError:
        pass

    # app의 기본 설정 세팅
    if os.environ["FLASK_ENV"] == "development":
        app.config.from_mapping(
            # 데이터 보안을 위해 사용. 개발 중에는 편의를 위해 'dev', 실 가동 환경에서는 꼭 랜덤값으로 엎어써야함.
            SECRET_KEY='dev',
            # SQlite DB 파일의 경로.
            # instance 밑에 transform.sqlite 라는 이름.
            DATABASE=os.path.join(app.instance_path, 'transform.sqlite'),
            UPLOAD_FOLDER=UPLOAD_DIR_PATH,
        )
    else:
        app.config.from_mapping(
            # 데이터 보안을 위해 사용. 개발 중에는 편의를 위해 'dev', 실 가동 환경에서는 꼭 랜덤값으로 엎어써야함.
            SECRET_KEY=secrets.token_urlsafe(16),
            # SQlite DB 파일의 경로.
            # instance 밑에 transform.sqlite 라는 이름.
            DATABASE=os.path.join(app.instance_path, 'transform.sqlite'),
            UPLOAD_FOLDER=UPLOAD_DIR_PATH,
        )

    app.register_blueprint(main.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(distribution.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(auth.bp)

    @app.route('/upload_files/<path:filename>')
    def download(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    db.init_app(app)

    return app
