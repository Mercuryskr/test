from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建app对象
app = Flask(__name__)

class Config(object):
    # 数据库的连接信息
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/toutiao'
    # 在Flask中是否追踪数据修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 显示生成的SQL语句，可用于调试
    SQLALCHEMY_ECHO = True

#加载配置信息
app.config.from_object(Config)

# 创建SQLALCHEMY对象
db = SQLAlchemy(app)

# 定义模型类
class User(db.Model):

    # 用户基本信息
    __tablename__ = 'user_basic'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    mobile = db.Column(db.String, doc='手机号')
    password = db.Column(db.String, doc='密码')
    name = db.Column('user_name', db.String, doc='昵称')
    profile_photo = db.Column(db.String, doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    is_media = db.Column(db.Boolean, default=False, doc='是否是自媒体')
    is_verified = db.Column(db.Boolean, default=False, doc='是否实名认证')
    introduction = db.Column(db.String, doc='简介')
    certificate = db.Column(db.String, doc='认证')
    article_count = db.Column(db.Integer, default=0, doc='发帖数')
    following_count = db.Column(db.Integer, default=0, doc='关注的人数')
    fans_count = db.Column(db.Integer, default=0, doc='被关注的人数（粉丝数）')
    like_count = db.Column(db.Integer, default=0, doc='累计点赞人数')
    read_count = db.Column(db.Integer, default=0, doc='累计阅读人数')

    account = db.Column(db.String, doc='账号')
    email = db.Column(db.String, doc='邮箱')
    status = db.Column(db.Integer, default=STATUS.ENABLE, doc='状态，是否可用')
    # 1.定义关系字段
    # userlist=False返回的数据不再使用列表容器
    # primaryjoin主连接
    profile = db.relationship('UserProfile', uselist=False, primaryjoin='User.id==foreign(UserProfile.id)')

    # 2.定义和Relation表的关系字段，查关注对象
    following = db.relationship('Relation', primaryjoin='User.id==foreign(Relation.id)')

    # 定义查询当前用户的所有粉丝列表
    fans = db.relationship('Relation',  primaryjoin='User.id==foreign(Relation.target_user_id)')




class UserProfile(db.Model):
    """
    用户资料表
    """
    __tablename__ = 'user_profile'

    class GENDER:
        MALE = 0
        FEMALE = 1
    # User.id: 从面向对象角度理解
    # user_basic.user_id:从数据库表的角度理解
    # 2.定义外键，User.id作为外键关联
    id = db.Column('user_id', db.Integer,  primary_key=True, doc='用户ID')
    gender = db.Column(db.Integer, default=0, doc='性别')
    birthday = db.Column(db.Date, doc='生日')
    real_name = db.Column(db.String, doc='真实姓名')
    id_number = db.Column(db.String, doc='身份证号')
    id_card_front = db.Column(db.String, doc='身份证正面')
    id_card_back = db.Column(db.String, doc='身份证背面')
    id_card_handheld = db.Column(db.String, doc='手持身份证')
    ctime = db.Column('create_time', db.DateTime, default= datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    register_media_time = db.Column(db.DateTime, doc='注册自媒体时间')

    area = db.Column(db.String, doc='地区')
    company = db.Column(db.String, doc='公司')
    career = db.Column(db.String, doc='职业')


class Relation(db.Model):
    """
    用户关系表
    """
    __tablename__ = 'user_relation'

    class RELATION:
        DELETE = 0
        FOLLOW = 1
        BLACKLIST = 2

    id = db.Column('relation_id', db.Integer, primary_key=True, doc='主键ID')
    # User.id作为外键关联
    user_id = db.Column(db.Integer,  doc='用户ID')
    target_user_id = db.Column(db.Integer, doc='目标用户ID')
    relation = db.Column(db.Integer, doc='关系')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    # 偶像名字
    target_user = db.relationship('User', primaryjoin='Relation.target_user_id==foreign(User.id)', uselist=False)




"""粉丝偶像偶像名
用户id=1的偶像
sql:
select a.target_user_id, a.user_id, b.user_name from user_relation as a inner join user_basic as b on
a.target_user_id=b.user_id where a.user_id=1
user_id  target_user_id      user_name
1	        2	            13552285417
1	        3	            18811179159
1	        5	            张三

"""
"""
分页查询取page为几的所有
User.query.paginate(page=None, per_page=None).items
查此数据所在第几页
User.query.paginate().page
共几页
User.query.paginate().pages
"""





@app.route('/')
def hello_world():
    try:
        user = User(mobile='139111111111', name='python')
        db.session.add(user) # 只保存在会话层的session,数据库里没有数据
        db.session.flush() # 将db.session记录的sql传到数据库中执行
        # a=1/0
        # print(a)
        profile = UserProfile(id=user.id)
        db.session.add(profile)
        db.session.commit()

    except:
        db.session.rollback()

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
