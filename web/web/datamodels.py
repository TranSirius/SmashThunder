from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import event

from web.databases import Model

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

    def __eq__(self, other):
        return type(self) is type(other) and self.ID == other.ID

    def __ne__(self, other):
        return not self.__eq__(other)

class Album(Model):
    __tablename__ = 'Album'

    ID = Column('ID', Integer, primary_key = True, autoincrement = True)
    user_ID = Column('UserID', Integer, ForeignKey('User.ID',ondelete = 'CASCADE', onupdate = 'CASCADE'))
    album_title = Column('AlbumTitle', String(200), nullable = False)
    create_time = Column('CreateTime', Integer, nullable = False)

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

    ID = Column('ID', Integer, primary_key = True, autoincrement = True)
    album_ID = Column('AlbumID', Integer, ForeignKey('Album.ID', ondelete = 'CASCADE', onupdate = 'CASCADE'))
    photo_title = Column('PhotoTitle', String(200), nullable = True)
    create_time = Column('CreateTime', Integer, nullable = False)

    def __str__(self):
        return '%s(ID=%r, AlbumID=%r, PhotoTitle=%r, CreateTime=%r)' % (
            self.__class__.__name__,
            self.ID,
            self.album_ID,
            self.photo_title,
            self.create_time
        )