from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

from web.db import databases
from web.db.datamodels import User, Album, Photo

import shutil
import os

mod = Blueprint('edit', __name__, url_prefix = '/edit')

@mod.route('/album/rename', methods = ['POST'])
def albumRename():
    ret = dict()
    user_id = g.user_id
    db_session = databases.db_session()

    try:
        album_title = request.json['albumTitle']
        new_title = request.json['newTitle']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    user = db_session.query(User).filter_by(ID = user_id).first()
    if user is None:
        ret['status'] = 'User does not exist or you should login first!'
        return ret
    user_name = user.user_name

    album = db_session.query(Album).filter(Album.user_ID == user_id).filter(album_title == album_title)
    if album is None:
        ret['status'] = 'Album does not exist!'
        return ret

    os.rename(  app.config['USER_DATA'] + 'data/' + user_name + '/img/' + album_title, 
                app.config['USER_DATA'] + 'data/' + user_name + '/img/' + new_title)
    db_session.query(Album).filter_by(user_ID = user_id).filter_by(album_title = album_title).update({'album_title': new_title})
    
    db_session.commit()
    ret['status'] = 'ok'
    return ret

@mod.route('/album/delete', methods = ['POST'])
def albumDelete():
    ret = dict()
    user_id = g.user_id
    db_session = databases.db_session()
    try:
        album_title = request.json['albumTitle']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    user = db_session.query(User).filter(User.ID == user_id).first()
    if user is None:
        ret['status'] = 'User does not exist or you should login first!'
        return ret
    user_name = user.user_name

    try:
        shutil.rmtree(app.config['USER_DATA'] + 'data/' + user_name + '/img/' + album_title)
    except:
        pass
    db_session.query(Album).filter(Album.user_ID == user_id).filter(Album.album_title == album_title).delete()
    db_session.commit()

    last_album = db_session.query(Album).filter(Album.user_ID == user_id).first()

    if last_album is None:
        Album.generateAlbum(user_name, 'My Photo')

    ret['status'] = 'ok'
    return ret

@mod.route('/img/rename', methods = ['POST'])
def imgRename():
    ret = dict()
    user_id = g.user_id
    db_session = databases.db_session()
    try:
        album_title = request.json['albumTitle']
        img_title = request.json['imgTitle']
        new_title = request.json['newTitle']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    user = db_session.query(User).filter(User.ID == user_id).first()
    if user is None:
        ret['status'] = 'User does not exist or you should login first!'
        return ret
    user_name = user.user_name

    album = db_session.query(Album).filter(Album.user_ID == user_id).filter(Album.album_title == album_title).first()
    if album is None:
        ret['status'] = 'Album does not exist!'
        return ret
    album_id =album.ID

    photo = db_session.query(Photo).filter(Photo.album_ID == album_id).filter(Photo.photo_title == img_title).first()
    if photo is None:
        ret['status'] = 'Photo does not exist!'
        return ret

    os.rename(  app.config['USER_DATA'] + 'data/' + user_name + '/img/' + album_title + '/' + img_title,
                app.config['USER_DATA'] + 'data/' + user_name + '/img/' + album_title + '/' + new_title) 
    db_session.query(Photo).filter(Photo.album_ID == album_id).filter(Photo.photo_title == img_title).update({'photo_title': new_title})

    db_session.commit()
    ret['status'] = 'ok'
    return ret

@mod.route('/img/delete', methods = ['POST'])
def imgDelete():
    ret = dict()
    user_id = g.user_id
    db_session = databases.db_session()

    try:
        album_title = request.json['albumTitle']
        img_title = request.json['imgTitle']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    user = db_session.query(User).filter(User.ID == user_id).first()
    if user is None:
        ret['status'] = 'User does not exist!'
        return ret
    user_name = user.user_name

    album = db_session.query(Album).filter(Album.user_ID == user_id).filter(Album.album_title == album_title).first()
    if album is None:
        ret['status'] = 'Album does not exist!'
        return ret
    album_id =album.ID

    try:
        os.remove(app.config['USER_DATA'] + 'data/' + user_name + '/img/' + album_title + '/' + img_title)
    except:
        pass
    db_session.query(Photo).filter(Photo.album_ID == album_id).filter(Photo.photo_title == img_title).delete()

    db_session.commit()
    ret['status'] = 'ok'
    return ret