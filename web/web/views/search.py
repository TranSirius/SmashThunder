from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

import sqlalchemy
import elasticsearch as es

from web.db import databases
from web.db import datamodels
from web.db.datamodels import User, Album, Photo

from web.index import esclient
from web.index import doctype

import os
import time
import datetime

mod = Blueprint('search', __name__, url_prefix = '/search')

@mod.route('/user', methods = ['POST'])
def searchUser():
    ret = dict()
    try:
        user_name = request.json['keyword']
    except:
        ret['status'] = 'You Cannot Search for Empty'
        return ret

    search_engine = doctype.User.search(using = esclient.es)
    search_result = search_engine.query("match", user_name = user_name)
    search_result = search_result.execute().to_dict()
    _shards = search_result['_shards']
    total = _shards['total']
    hits = search_result['hits']['hits']
    
    users = [{'username': str(hit['_source']['user_name'])} for hit in hits]

    ret['total'] = total
    ret['username'] = users
    ret['scroll_id'] = 'not implemented yet'

    ret['status'] = 'ok'
    return ret

@mod.route('/img', methods = ['POST'])
def searchImg():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        keyword = request.json['keyword']
    except:
        ret['status'] = 'You Cannot Search for Empty'
        return ret

    search_engine = doctype.Photo.search(using = esclient.es)
    search_result = search_engine.query("match", photo_name = keyword)
    search_result = search_result.execute().to_dict()

    _shards = search_result['_shards']
    total = _shards['total']
    hits = search_result['hits']['hits']

    photos = []
    for hit in hits:
        photo = dict()
        photo['ID'] = hit['_id']
        photo['photoname'] = hit['_source']['photo_name']
        photo['user'] = db_session_instance\
            .query(datamodels.User).join(datamodels.Album).join(datamodels.Photo)\
            .filter(datamodels.Photo.ID == photo['ID'])\
            .first().user_name
        photo['album'] = db_session_instance\
            .query(datamodels.Album).join(datamodels.Photo)\
            .filter(datamodels.Photo.ID == photo['ID'])\
            .first().album_title
        photos.append(photo)

    ret['total'] = total
    ret['photo'] = photos
    ret['scroll_id'] = 'not implemented yet'

    ret['status'] = 'ok'
    return ret

@mod.route('post', methods = ['POST'])
def searchPost():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        keyword = request.json['keyword']
    except:
        ret['status'] = 'You Cannot Search for Empty'
        return ret

    search_engine = doctype.Post.search(using = esclient.es)
    search_result = search_engine.query("multi_match", query = keyword, fields = ['post_title', 'post_content', 'folder_name'])
    search_result = search_result.execute().to_dict()

    _shards = search_result['_shards']
    total = _shards['total']
    hits = search_result['hits']['hits']
    
    # posts = [{'title': str(hit['_source']['post_title']), 'content': str(hit['_source']['post_content']), 'folder': str(hit['_source']['folder_name'])} for hit in hits]
    posts = []
    for hit in hits:
        source = hit['_source']
        post_id = hit['_id']
        user = db_session_instance\
            .query(datamodels.User).join(datamodels.Folder).join(datamodels.Post)\
            .filter(datamodels.Post.ID == post_id)\
            .first()
        user = user.user_name
        post = dict()
        post['title'] = source['post_title']
        post['content'] = source['post_content']
        post['folder'] = source['folder_name']
        post['author'] = user
        posts.append(post)

    ret['total'] = total
    ret['posts'] = posts
    ret['scroll_id'] = 'not implemented yet'

    ret['status'] = 'ok'
    return ret