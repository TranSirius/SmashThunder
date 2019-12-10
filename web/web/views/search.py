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

@mod.route('/user')
def searchUser():
    ret = dict()
    
    try:
        user_name = request.json['keyword']
    except:
        ret['status'] = 'You Cannot Search for Empty'
        return ret

    search_engine = doctype.User.search(using = esclient.es)
    search_result = search_engine.query("match", user_name = 'ceshiceshi_dalao')
    search_result = search_result.execute().to_dict()
    _shards = search_result['_shards']
    total = _shards['total']
    hits = search_result['hits']['hits']
    
    users = [str(hit['_source']['user_name']) for hit in hits]

    ret['total'] = total
    ret['username'] = users
    ret['scroll_id'] = 'not implemented yet'

    return ret

@mod.route('/img')
def searchImg():
    ret = dict()

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
        photos.append(photo)

    ret['total'] = total
    ret['photo'] = photos
    ret['scroll_id'] = 'not implemented yet'

    return ret

@mod.route('post')
def searchPost():
    ret = dict()

    try:
        keyword = request.json['keyword']
    except:
        ret['status'] = 'You Cannot Search for Empty'
        return ret

    search_engine = doctype.Post.search(using = esclient.es)
    search_result = search_engine.query("multi_match", query = keyword, fields = ['post_title', 'post_content'])
    search_result = search_result.execute().to_dict()

    _shards = search_result['_shards']
    total = _shards['total']
    hits = search_result['hits']['hits']
    
    posts = [{'title': str(hit['_source']['post_title']), 'content': str(hit['_source']['post_content'])} for hit in hits]

    ret['total'] = total
    ret['posts'] = posts
    ret['scroll_id'] = 'not implemented yet'
    return ret