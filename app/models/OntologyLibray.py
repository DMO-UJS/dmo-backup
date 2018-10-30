from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db=SQLAlchemy()


class Ontolo_sets(db.Model):
    OLid=Column(Integer, primary_key=True, autoincrement=True)
    OLname =Column(String(50), nullable=False)
    LRtime =Column(DateTime(), default=datetime.now)
    state =Column(Boolean, default=False)


    def set_attrs(self,attrs_dict):
        for key,value in attrs_dict.items():
            if  hasattr(self,key) and  key !='id':
                setattr(self,key,value)


class Ontolo_relats(db.Model):
    ORid=Column(Integer, primary_key=True,autoincrement=True)
    ORname =Column(String(50), nullable=False)
    Des1=Column(String(20))
    Des2 = Column(String(20))
    LRtime =Column(DateTime(), default=datetime.now)
    ontolo_sets = relationship('Ontolo_sets')
    F_OLid=Column(Integer,ForeignKey('ontolo_sets.OLid'))


    def set_attrs(self,attrs_dict):
        for key,value in attrs_dict.items():
            if  hasattr(self,key) and  key !='id':
                setattr(self,key,value)
