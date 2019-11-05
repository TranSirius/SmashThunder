from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

import sqlalchemy

from web.db import databases
from web.db import datamodels
from web.db.datamodels import User, Album, Photo, Post, Folder

from web.index import doctype

from web.views.auth import loginRequest

import os
import time
import datetime
import uuid

mod = Blueprint('submit', __name__, url_prefix = '/submit')

@mod.route('/img', methods = ['POST'])
@loginRequest
def uploadPic():
    ret = dict()

    db_session = databases.db_session()
    query_res = db_session.query(User).filter(User.ID == g.user_id).first()
    
    user_name = query_res.user_name
    pic_dir = app.config['USER_DATA'] + 'data/' + user_name + '/img/'

    img_list = request.files.getlist('files')

    dtime = datetime.datetime.now()
    unix_time = time.mktime(dtime.timetuple()) * 1000
    album_title = request.form.get('albumTitle')

    album = db_session.query(Album).filter(Album.user_ID == g.user_id).filter(Album.album_title == album_title).first()
    if album is None:
        album = Album.generateAlbum(user_name, album_title, unix_time)
        # album = db_session.query(Album).filter(Album.user_ID == g.user_id).filter(Album.album_title == album_title).first()

    for img in img_list:
        old_record = db_session.query(Photo).filter(Photo.photo_title == img.filename).filter(Photo.album_ID == album.ID).first()
        if old_record is None:
            new_id = "".join(str(uuid.uuid1()).split("-")[:-1])
            new_img = Photo(ID = new_id, album_ID = album.ID, photo_title = img.filename, create_time = unix_time)
            db_session.add(new_img)
        else:
            old_record.create_time = unix_time
        img.save(app.config['USER_DATA'] + 'data/' + user_name + '/img/' + album_title + '/' + img.filename)
    db_session.commit()

    from web.index.esclient import es
    for img in img_list:
        img = db_session.query(Photo).filter(Photo.album_ID == album.ID).filter(Photo.photo_title == img.filename).first()
        img_id = img.ID
        img_index = doctype.Photo(meta = {'id':img_id}, photo_name = img.photo_title)
        img_index.save(using = es)

    ret['status'] = 'ok'
    return ret
    

@mod.route('/post', methods = ['POST'])
def uploadPost():
    ret = dict()
    db_session = databases.db_session()

    try:
        post_title = request.json['title']
        folder_title = request.json['folder']
        post_format = request.json['format']
        post_content = request.json['content']
    except KeyError:
        ret['status'] = "KeyError!"
        return ret
    
    dtime = datetime.datetime.now()
    unix_time = time.mktime(dtime.timetuple()) * 1000

    folder = db_session.query(User).join(Folder).filter(User.ID == g.user_id).filter(Folder.folder_title == folder_title).first()
    if folder is None:
        folder = Folder(user_ID = g.user_id, folder_title = folder_title, create_time = unix_time)
        db_session.add(folder)
        db_session.commit()
    
    old_post = db_session.query(Post).filter(Post.post_title == post_title).filter(Post.folder_ID == folder.ID).first()
    if old_post is None:
        post_id = "".join(str(uuid.uuid1()).split("-")[:-1])
        new_post = Post(ID = post_id, folder_title = folder_title, post_title = post_title, create_time = unix_time, document_format = post_format, post_content = post_content)
        db_session.add(new_post)
    else:
        old_post.post_content = post_content
        old_post.create_time = unix_time
        post_id = old_post.ID
    db_session.commit()

    from web.index.esclient import es
    post_index = doctype.Post(meta={'id':post_id}, post_title = post_title, post_content = post_content, folder_name = folder_title)

    ret['status'] = 'ok'
    return ret