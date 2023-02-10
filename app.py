import click
from flask import Flask

from .make_data import make_data
from .utils import CustomJSONEncoder
from .blueprint.order import order_bp
from .blueprint.ticket import ticket_bp
from .blueprint.comments import comment_bp
from .blueprint.hotel import hotel_bp
from .blueprint.sight import sight_bp
from .blueprint.station import station_bp
from .blueprint.user import user_bp

from .blueprint.index import index_bp
from .extensions import db, cors
from .settings import config
from .models import User, Sight, Hotel, Station, Ticket, Order, Comment

# 初始化APP
app = Flask(__name__, template_folder='templates', static_folder="static")
# 加载配置
app.config.from_object(config['development'])
# 挂载json处理类
app.json_encoder = CustomJSONEncoder

# 初始化SQLAlchemy和CORS
db.init_app(app)
"""首次运行项目，取消下面代码注释，生成数据库文件和虚拟数据"""
# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     print("数据库创建finished")
#     # print(app.config['SQLALCHEMY_DATABASE_URI'])
#     print("生成数据")
#     make_data()
#     print("生成数据finished")

# 加载跨域组件
cors.init_app(app)

# 挂载蓝图
app.register_blueprint(index_bp)
app.register_blueprint(user_bp)
app.register_blueprint(sight_bp)
app.register_blueprint(hotel_bp)
app.register_blueprint(station_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(ticket_bp)
app.register_blueprint(order_bp)


# # 设置命令
# @app.cli.command('initdb')
# @click.option('--drop', is_flag=True, help='Create after drop.')
# def initdb(drop):
#     """Initialize the database."""
#     if drop:
#         click.confirm('This operation will delete the database, do you want to continue?', abort=True)
#         db.drop_all()
#         click.echo('Drop tables.')
#     db.create_all()
#     click.echo('Initialized database.')
#
#
# def create_db():
#     with app.app_context():
#         db.drop_all()
#         db.create_all()
#         print("finished")
#         print(app.config['SQLALCHEMY_DATABASE_URI'])
#     return None


if __name__ == '__main__':
    app.run(debug=True)
