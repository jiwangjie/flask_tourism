import functools
from datetime import datetime, date

from flask import session, g
from flask.json import JSONEncoder, jsonify
import numpy as np


class CustomJSONEncoder(JSONEncoder):
    """自定义Json化，没用到"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return JSONEncoder.default(self, obj)


def login_required(func):
    @functools.wraps(func)  # 修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        user = session.get('user')
        if not user:
            # WITHOUT_LOGIN是一个常量
            return jsonify({
                "code": 200,
                "message": "用户尚未登录",
                "data": ""
            })
        else:
            # 已经登录的话 g变量保存用户信息，相当于flask程序的全局变量
            g.user = user
            return func(*args, **kwargs)
    return inner

