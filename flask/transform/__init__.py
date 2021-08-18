import os
import secrets
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
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
        key = secrets.token_urlsafe(16)
        os.environ["SECRET_KEY"] = key
        app.config.from_mapping(
            # 데이터 보안을 위해 사용. 개발 중에는 편의를 위해 'dev', 실 가동 환경에서는 꼭 랜덤값으로 엎어써야함.
            SECRET_KEY=key,
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


# 업로드 폴더에 있는 파일들 삭제하는 함수
def file_clear():
    dir_path = UPLOAD_DIR_PATH
    file_list = os.listdir(dir_path)

    for file in file_list:
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    print("업로드 파일 삭제 성공!")


# 업로드한 파일들 일정 시간에 삭제되게 스케줄링
sched = BackgroundScheduler()
sched.add_job(file_clear, 'cron', hour=4)   # 오전 4시에 file_clear 함수 실행
sched.start()


# app 이 종료되면 스케줄러도 같이 종료
def OnExitApp():
    sched.shutdown()
    print("exit Flask application")


atexit.register(OnExitApp)
