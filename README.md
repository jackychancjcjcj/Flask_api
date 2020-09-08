# Flask_api
基于flask框架的api设计  
## [api_v1.py](https://github.com/jackychancjcjcj/Flask_api/blob/master/api_v1.py)
    1. 基于flask设计api
    2. 功能只有验证超级用户
## [api_v2.py](https://github.com/jackychancjcjcj/Flask_api/blob/master/api_v2.py)
    1. 注册用户，录入sqlite数据库
    2. 可申请token，免登录
## Flask入门教程（李辉）
#### 初始化
```Python
from flask import Flask
app = Flask(__name__)
```
#### 启动
```Python
if __name__ == '__main__':
    app.run(debug=TRUE) #debug开着方便修改代码
```
#### 添加路由
```Python
@app.route('/',methods=['GET']) #可以绑定多个路由
```
#### 传入参数
```Python
@app.route('/<int:id>',methods=['GET'])
def get_id(id):
        pass
```
#### 修改视图函数名
```python
from flask import url_for
# ...
@app.route('/')
def hello():
    return 'Hello'
@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name
@app.route('/test')
def test_url_for():
# 下面是一些调用示例：
    print(url_for('hello')) # 输出：/
# 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli')) # 输出：/user/greyli
    print(url_for('user_page', name='peter')) # 输出：/user/peter
    print(url_for('test_url_for')) # 输出：/test# 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL后面。
    print(url_for('test_url_for', num=2)) # 输出：/test?num=2
    return 'Test page'
```
#### 数据库
使用的是SQLite，因为不需要单独启动数据库服务器，基于文件，适合访问量低的程序。  
```python
from flask_sqlalchemy import SQLAlchemy # 导入扩展
import os
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db') # 告诉SQLALCHEMY连接数据库地址
db = SQLAlchemy(app) # 初始化扩展，传入程序实例 app
```
创建数据库模型（app.py),创建两张表：用户信息和电影信息
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) # 主键
    name = db.Column(db.String(20))
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影标题
    year = db.Column(db.String(4)) # 电影年
```
上边模型创建后还没生成表，需要在app.py所在的根目录下运行flask shell(与直接打开python shell 区别是这种方式激活了程序上下文）  
$ flask shell  
>>> from app import db  
>>> db.create_all()  
如果后续需要改动模型  
>>> db.drop_all()  
>>> db.create_all()  
下面展示如何向数据库添加数据  
>>> from app import User, Movie # 导入模型类  
>>> user = User(name='Grey Li') # 创建一个 User 记录  
>>> m1 = Movie(title='Leon', year='1994') # 创建一个 Movie 记录  
>>> m2 = Movie(title='Mahjong', year='1996') # 再创建一个 Movie记录  
>>> db.session.add(user) # 把新创建的记录添加到数据库会话  
>>> db.session.add(m1)  
>>> db.session.add(m2)  
>>> db.session.commit() # 提交数据库会话，只需要在最后调用一次即可  
提示：在实例化模型类的时候，我们并没有传入 id 字段（主键），因为SQLAlchemy 会自动处理这个字段。  
