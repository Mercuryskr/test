from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# 0.定义项目配置类
class Config(object):

    # mysql数据库连接信息
    # SQLALCHEMY_DATABASE_URI = "mysql://账号:密码@ip地址:3306/数据库名称"
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/toutiao"
    # 数据库修改跟踪操作
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 输出orm转换出来的sql语句
    SQLALCHEMY_ECHO = True


# 创建app对象
app = Flask(__name__)
# 加载配置信息
app.config.from_object(Config)

# 创建数据库对象
db = SQLAlchemy(app)


# 定义模型类，完成数据库表的映射
# 继承：db.Model
class User(db.Model):
    """
    用户基本信息
    """
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

    # user.profile.gender 用户资料表中的gender属性
    # relationship 关系字段，只是在面向对象的层次，方便查询而设计的关系字段，在数据库并不存在
    # 1.定义关系字段
    # uselist=False 返回的数据不再使用列表容器
    profile = db.relationship("UserProfile", uselist=False)

    # 定义和Relation表的关系字段
    following = db.relationship("Relation", uselist=True)


"""
User --- UserProfile  [一对一]
# 需求：当有一个User对象，根据User对象获取 UserProfile 用户资料表中的gender字段值
user = User.query.get(5)
user.profile.gender


User --- Relation [多对多]

# 需求：当有一个User对象，想根据User对象获取 Relation 用户关系表中的字段 target_user_id的值
user = User.query.get(1)
user.following[0].target_user_id



"""


class UserProfile(db.Model):
    """
    用户资料表
    """
    __tablename__ = 'user_profile'

    class GENDER:
        MALE = 0
        FEMALE = 1
    # User.id ： 从面向对象角度理解
    # user_basic.user_id： 从数据库表的角度理解
    # 2.定义外键，User.id作为外键关联
    id = db.Column('user_id', db.Integer, db.ForeignKey(User.id) ,primary_key=True, doc='用户ID')
    # id = db.Column('user_id', db.Integer, db.ForeignKey("user_basic.user_id") ,primary_key=True, doc='用户ID')
    gender = db.Column(db.Integer, default=0, doc='性别')
    birthday = db.Column(db.Date, doc='生日')
    real_name = db.Column(db.String, doc='真实姓名')
    id_number = db.Column(db.String, doc='身份证号')
    id_card_front = db.Column(db.String, doc='身份证正面')
    id_card_back = db.Column(db.String, doc='身份证背面')
    id_card_handheld = db.Column(db.String, doc='手持身份证')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
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
    # 2.User.id作为外键关联
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), doc='用户ID')
    target_user_id = db.Column(db.Integer, doc='目标用户ID')
    relation = db.Column(db.Integer, doc='关系')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')






@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()