# -*- coding: utf-8 -*-

from doctor.models.base import db
from sqlalchemy.dialects.mysql import TINYINT
from datetime import datetime


class User(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(32), unique=True, nullable=False)
    nickname = db.Column(db.String(32), nulslable=True)
    realname = db.Column(db.String(32), nullable=True)
    sex = db.Column(db.SmallInteger, default=0, nullable=False)
    province = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(20), nullable=True)
    headimgurl = db.Column(db.String(150), nullable=True)
    regtime = db.Column(db.DateTime, default=datetime.now, nullable=False)
    status = db.Column(TINYINT(4, unsigned=True), default=0)
    user_type = db.Column(TINYINT(4, unsigned=True), default=0)

    def __init__(self, openid, nickname=None, realname=None,
                 classname=None, sex=None, province=None, city=None,
                 country=None, headimgurl=None, regtime=None, status=None, user_type=None):
        self.openid = openid
        self.nickname = nickname
        self.realname = realname
        self.classname = classname
        self.sex = sex
        self.province = province
        self.city = city
        self.country = country
        self.headimgurl = headimgurl
        self.regtime = regtime
        self.status = status
        self.user_type = user_type

    def __repr__(self):
        return '<openid %r>' % self.openid

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
