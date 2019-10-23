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
from flask import g, current_app

from flask.cli import with_appcontext 

import click
import os
import shutil

engine = create_engine(current_app.config['DATABASE_ENGINE'], encoding='utf-8')
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(session)

Model = declarative_base(name='Model')
Model.query = db_session.query_property()

from web.db.datamodels import *

@click.command('drop-db')
@with_appcontext
def dropDatabaseCommand():
    """Clear the existing data."""
    Model.metadata.drop_all(bind=engine)
    try:
        shutil.rmtree('/share/data')
    except:
        pass
    click.echo('drop the database.')

def registerDropDatabase(app):
    app.cli.add_command(dropDatabaseCommand)

@click.command('init-db')
@with_appcontext
def initDatabaseCommand():
    """Create new tables."""
    Model.metadata.create_all(bind=engine)
    try:
        os.mkdir('/share/data')
    except:
        pass
    click.echo('Initialized the database.')

def registerInitDatabase(app):
    app.cli.add_command(initDatabaseCommand)
