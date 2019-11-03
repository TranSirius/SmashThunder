from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index

from flask import current_app as app
from flask.cli import with_appcontext 
import click

es = Elasticsearch(['localhost'], timeout = 3600)

@click.command('drop-index')
@with_appcontext
def dropIndexCommand():
    if es.indices.exists(index = app.config['ELASTIC_SEARCH_INDEX']):
        es.indices.delete(app.config['ELASTIC_SEARCH_INDEX'])
    print("Drop Index Finished")

def registerDropIndex(app):
    app.cli.add_command(dropIndexCommand)


@click.command('init-index')
@with_appcontext
def initIndexCommand():
    if not es.indices.exists(index = app.config['ELASTIC_SEARCH_INDEX']):
        elasticsearch_index = Index(
            app.config['ELASTIC_SEARCH_INDEX']
        )
        elasticsearch_index.settings(
            number_of_shards=1,
            number_of_replicas=0
        )

        from web.index.doctype import User
        elasticsearch_index.document(User)

        from web.index.doctype import Photo
        elasticsearch_index.document(Photo)

        elasticsearch_index.create(using = es)
        print("Init Index Finished!")


        new_user = User(
            user_name = "测试"
        )
        res = new_user.save(using = es)
        print(res)
        search = User.search(using = es)
        res = search.count()
        print(res)

    else:
        print("Index Exists!")

def registerInitIndex(app):
    app.cli.add_command(initIndexCommand)