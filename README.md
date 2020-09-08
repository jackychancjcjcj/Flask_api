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
##### 示例
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
##### 读取的方法很多，参考书的42页
    >>> from app import Movie # 导入模型类
    >>> movie = Movie.query.first() # 获取 Movie 模型的第一个记录（返回模型类实例）
    >>> movie.title # 对返回的模型类实例调用属性即可获取记录的各字段数据'Leon'
    >>> movie.year'1994'
    >>> Movie.query.all() # 获取 Movie 模型的所有记录，返回包含多个模型类实例的列表[<Movie 1>, <Movie 2>]
    >>> Movie.query.count() # 获取 Movie 模型所有记录的数量2
    >>> Movie.query.get(1) # 获取主键值为 1 的记录<Movie 1>
    >>> Movie.query.filter_by(title='Mahjong').first() # 获取 title字段值为 Mahjong 的记录<Movie 2>
    >>> Movie.query.filter(Movie.title=='Mahjong').first() # 等同于上面的查询，但使用不同的过滤方法<Movie 2>
##### 更新
    >>> movie = Movie.query.get(2)
    >>> movie.title = 'WALL-E' # 直接对实例属性赋予新的值即可
    >>> movie.year = '2008
    >>> db.session.commit() # 注意仍然需要调用这一行来提交改动
##### 删除
    >>> movie = Movie.query.get(1)
    >>> db.session.delete(movie) # 使用 db.session.delete() 方法删除记录，传入模型实例
    >>> db.session.commit() # 提交改动
#### 用户验证
Flask用Werkzeug内置的函数生成密码散列值，`werkzeug.security.generate_password_hash()`用来给定的密码生成密码散列值，`werkzeug.security.check_password_hash()`用来检查散列值是否对应。
##### 示例
    >>> from werkzeug.security import generate_password_hash, check_password_hash
    >>> pw_hash = generate_password_hash('dog') # 为密码 dog 生成密码散列值
    >>> pw_hash # 查看密码散列值
    'pbkdf2:sha256:50000$mm9UPTRI$ee68ebc71434a4405a28d34ae3f170757fb424663dc0ca15198cb881edc0978f'
    >>> check_password_hash(pw_hash, 'dog') # 检查散列值是否对应密码 dog
    True
    >>> check_password_hash(pw_hash, 'cat') # 检查散列值是否对应密码 cat
    False
我们在`User`类中增加`username`和`password`两个字段，同时添加两个方法来验证用户名和密码。
```python
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) # 用户名
    password_hash = db.Column(db.String(128)) # 密码散列值
    
    def set_password(self, password): # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password) #将生成的密码保持到对应字段
        
    def validate_password(self, password): # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)# 返回布尔值
```
值得注意的是，这样修改了表结构，我们需要重新建表（drop，再create），数据会清空。（若想保留数据，需要导入数据迁移工具包）  
另外我们也可以通过[`Flask-Login`](https://github.com/maxcountryman/flask-login)实现用户验证
#### 部署上线
这边使用的是书作者的项目代码
##### 获取
    git clone https://github.com/greyli/watchlist.git
