from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()  # 使用SQLAlchemy 进行ORM管理，方便
cors = CORS()  # 解决跨域问题
