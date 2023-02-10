import os.path

from flask import Blueprint, render_template, request, jsonify, abort
from werkzeug.utils import secure_filename

from ..settings import BaseConfig

index_bp = Blueprint('index', __name__)


# 主页
@index_bp.route('/')
def index():
    return render_template('index.html')


@index_bp.route('/admin')
def admin():
    return render_template('admin.html')


# 上传文件
@index_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('image')
    filename = secure_filename(file.filename)
    if filename != '':
        app_config = BaseConfig()
        file_ext = os.path.splitext(filename)[1]  # 文件后缀，判断文件类型是否合法
        if file_ext not in app_config.UPLOAD_EXTENSIONS:
            abort(400)
        file_path = os.path.join(app_config.UPLOAD_PATH, filename)
        print(file_path)
        file_path = os.path.abspath(file_path)
        # print(file_path)
        file.save(file_path)
        return jsonify({
            "code": 200,
            "message": "上传成功！",
            "data": os.path.join("http://127.0.0.1:5000/"+"static/files/", filename)
        })
    return jsonify({
        "code": 200,
        "message": "文件为空！"
    })
