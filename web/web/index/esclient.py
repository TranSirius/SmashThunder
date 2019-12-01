from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index

from flask import current_app as app
from flask.cli import with_appcontext 
import click

es = Elasticsearch(['localhost'], timeout = 3600)

@click.command('drop-index')
@with_appcontext
def dropIndexCommand():
    # if es.indices.exists(index = app.config['ELASTIC_SEARCH_INDEX']):
    #     es.indices.delete(app.config['ELASTIC_SEARCH_INDEX'])
    indices = app.config['ELASTIC_SEARCH_INDEX']
    for index in indices:
        try:
            ind = indices[index]
            es.indices.delete(ind)
        except:
            print("Index " + ind + " not found")
    print("Drop Index Finished")

def registerDropIndex(app):
    app.cli.add_command(dropIndexCommand)


@click.command('init-index')
@with_appcontext
def initIndexCommand():
    from web.index.doctype import Photo
    
    photo_document = Photo.get(id = 1, using = es)

    # for index in indices:
    #     index = Index(index)

    # if not es.indices.exists(index = app.config['ELASTIC_SEARCH_INDEX']):
    #     elasticsearch_index = Index(
    #         app.config['ELASTIC_SEARCH_INDEX']
    #     )
    #     elasticsearch_index.settings(
    #         number_of_shards=1,
    #         number_of_replicas=0
    #     )

    #     from web.index.doctype import User
    #     elasticsearch_index.document(User)

    #     from web.index.doctype import Photo
    #     elasticsearch_index.document(Photo)

    #     elasticsearch_index.create(using = es)
    #     print("Init Index Finished!")


    #     new_user = User(
    #         meta={'id': 42},
    #         user_name = "测试"
    #     )
    #     res = new_user.save(using = es)
    #     new_user = User(
    #         meta={'id': 41},
    #         user_name = "王警晖"
    #     )
    #     res = new_user.save(using = es)

    #     user = User.get(id=41, using=es)
    #     print(user)

    # else:
    #     print("Index Exists!")

def registerInitIndex(app):
    app.cli.add_command(initIndexCommand)