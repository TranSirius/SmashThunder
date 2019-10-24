from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import event
from werkzeug.security import generate_password_hash

from web.db.databases import Model, db_session
from flask import current_app as app
from flask import g

import os
import time
import datetime

class User(Model):
    __tablename__ = 'User'

    ID = Column('ID', Integer, primary_key = True, autoincrement = True)
    # super_admin, admin, user
    user_type = Column('UserType', String(50), nullable = False, default = 'user')
    user_name = Column('UserName', String(200), unique = True, nullable = True)
    pass_word = Column('PassWord', String(100), nullable = False)

    def __str__(self):
        return '%s(ID=%r, UserType=%r, UserName=%r, PassWord=%r)' % (
            self.__class__.__name__,
            self.ID,
            self.user_type,
            self.user_name,
            self.pass_word
        )

    @classmethod
    def generateUser(cls, username, password):
        password = generate_password_hash(password)
        new_user = User(user_name = username, pass_word = password)
        db_session.add(new_user)
        db_session.commit()

        os.mkdir(app.config['USER_DATA'] + str(username))
        os.mkdir(app.config['USER_DATA'] + str(username) + '/img')
        os.mkdir(app.config['USER_DATA'] + str(username) + '/md')
        os.mkdir(app.config['USER_DATA'] + str(username) + '/html')

        new_user = db_session.query(User).filter_by(user_name = username).first()
        user_ID = new_user.ID
        g.user_id = user_ID

        Album.generateAlbum(username, 'My Photos')

    def __eq__(self, other):
        return type(self) is type(other) and self.ID == other.ID

    def __ne__(self, other):
        return not self.__eq__(other)




class Album(Model):
    __tablename__ = 'Album'

    ID = Column('ID', Integer, primary_key = True, autoincrement = True)
    user_ID = Column('UserID', Integer, ForeignKey('User.ID',ondelete = 'CASCADE', onupdate = 'CASCADE'))
    album_title = Column('AlbumTitle', String(200), nullable = False)
    create_time = Column('CreateTime', BigInteger, nullable = False, default = 0)

    @classmethod
    def generateAlbum(cls, user_name, album_title):
        try:
            os.mkdir(app.config['USER_DATA'] + user_name + '/img/' + album_title)
        except:
            pass
        dtime = datetime.datetime.now()
        unix_time = time.mktime(dtime.timetuple()) * 1000
        new_album = Album(user_ID = g.user_id, album_title = album_title, create_time = unix_time)
        db_session.add(new_album)
        db_session.commit()

    def __str__(self):
        return '%s(ID=%r, UserID=%r, AlbumTitle=%r, CreateTime=%r)' % (
            self.__class__.__name__,
            self.ID,
            self.user_ID,
            self.album_title,
            self.create_time
        )

class Photo(Model):
    __tablename__ = 'Photo'

    # ID = Column('ID', Integer, primary_key = True, autoincrement = True)
    album_ID = Column('AlbumID', Integer, ForeignKey('Album.ID', ondelete = 'CASCADE', onupdate = 'CASCADE'), primary_key = True)
    photo_title = Column('PhotoTitle', String(200), nullable = True, primary_key = True)
    create_time = Column('CreateTime', BigInteger, nullable = False)

    def __str__(self):
        return '%s(ID=%r, AlbumID=%r, PhotoTitle=%r, CreateTime=%r)' % (
            self.__class__.__name__,
            self.ID,
            self.album_ID,
            self.photo_title,
            self.create_time
        )