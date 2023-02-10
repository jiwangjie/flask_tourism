import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    """配置开发环境"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'a secret string')  # 密钥，可自定义
    # 数据库信息，这里使用SQLite，比MySql轻便简单
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'flaskProject/data.db'))
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_PATH = os.path.join(os.path.dirname(__file__), "static/files/")  # 上传文件的路径
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif', '.jpge']  # 上传的文件类型


class DevelopmentConfig(BaseConfig):
    """开发环境"""
    pass


class ProductionConfig(BaseConfig):
    """生产环境"""
    pass


class TestingConfig(BaseConfig):
    """测试环境"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
