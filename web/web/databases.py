from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import event

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref
from sqlalchemy.orm import relation

from sqlalchemy.ext.declarative import declarative_base


from werkzeug import cached_property
from werkzeug import http_date

from flask import url_for
from flask import Markup
from flask import g

from flask.cli import with_appcontext 

import click

engine = create_engine('mysql+mysqldb://test:test@localhost/test')
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(session)

Model = declarative_base(name='Model')
Model.query = db_session.query_property()

class User(Model):
    __tablename__ = 'Users'

    ID = Column('ID', Integer, primary_key = True, autoincrement = True)
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

@click.command('drop-db')
@with_appcontext
def dropDatabaseCommand():
    """Clear the existing data."""
    Model.metadata.drop_all(bind=engine)
    click.echo('drop the database.')

def registerDropDatabase(app):
    app.cli.add_command(dropDatabaseCommand)

@click.command('init-db')
@with_appcontext
def initDatabaseCommand():
    """Create new tables."""
    Model.metadata.create_all(bind=engine)
    click.echo('Initialized the database.')

def registerInitDatabase(app):
    app.cli.add_command(initDatabaseCommand)
