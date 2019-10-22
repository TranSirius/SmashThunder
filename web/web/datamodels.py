from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import event

from web.databases import Model

class User(Model):
    __tablename__ = 'Users'

    ID = Column('ID', Integer, primary_key = True, autoincrement = True)
    # super_admin, admin, user
    user_type = Column('user_type', String(50), nullable = False, default = 'user')
    user_name = Column('user_name', String(200), unique = True, nullable = True)
    pass_word = Column('pass_word', String(100), nullable = False)

    def __str__(self):
        return '%s(ID=%r, user_type=%r, user_name=%r, pass_word=%r)' % (
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
