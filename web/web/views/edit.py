from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

from web.db import databases
from web.db.datamodels import User, Album, Photo, Folder, Post
from web.views.auth import loginRequest

from web.index import doctype
from elasticsearch_dsl import Search

import shutil
import os
import time
import datetime

mod = Blueprint('edit', __name__, url_prefix = '/edit')

@mod.route('/album/rename', methods = ['POST'])
@loginRequest
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
@loginRequest
def albumDelete():
    ret = dict()
    user_id = g.user_id
    db_session_instance = databases.db_session()
    try:
        album_title = request.json['albumTitle']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    user = db_session_instance.query(User).filter(User.ID == user_id).first()
    if user is None:
        ret['status'] = 'User does not exist or you should login first!'
        return ret
    user_name = user.user_name

    try:
        shutil.rmtree(app.config['USER_DATA'] + 'data/' + user_name + '/img/' + album_title)
    except:
        pass

    # Delete Photos in the Album from ElasticSeach
    photos = db_session_instance\
        .query(Photo).join(Album)\
        .filter(Album.user_ID == user_id).filter(Album.album_title == album_title)\
        .all()
    from web.index.esclient import es
    for p in photos:
        photo_index_doc = doctype.Photo.get(id = p.ID, using = es)
        photo_index_doc.delete(using = es)
    ################################################

    db_session_instance.query(Album).filter(Album.user_ID == user_id).filter(Album.album_title == album_title).delete()
    db_session_instance.commit()

    last_album = db_session_instance.query(Album).filter(Album.user_ID == user_id).first()
    if last_album is None:
        dtime = datetime.datetime.now()
        unix_time = time.mktime(dtime.timetuple()) * 1000
        Album.generateAlbum(user_name, 'MyPhoto', create_time = unix_time)

    ret['status'] = 'ok'
    return ret

@mod.route('/img/rename', methods = ['POST'])
@loginRequest
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
    img = db_session.query(Photo).filter(Photo.album_ID == album_id).filter(Photo.photo_title == img_title).first()
    img.photo_title = new_title
    db_session.commit()

    # rename img in ElasticSearch
    from web.index.esclient import es
    img_id = img.ID
    img_index = doctype.Photo(meta = {'id':img_id}, photo_name = img.photo_title)
    img_index.save(using = es)
    #############################

    ret['status'] = 'ok'
    return ret

@mod.route('/img/delete', methods = ['POST'])
@loginRequest
def imgDelete():
    ret = dict()
    user_id = g.user_id
    db_session_instance = databases.db_session()

    try:
        album_title = request.json['albumTitle']
        img_title = request.json['imgTitle']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    user = db_session_instance.query(User).filter(User.ID == user_id).first()
    if user is None:
        ret['status'] = 'User does not exist!'
        return ret
    user_name = user.user_name

    album = db_session_instance.query(Album).filter(Album.user_ID == user_id).filter(Album.album_title == album_title).first()
    if album is None:
        ret['status'] = 'Album does not exist!'
        return ret
    album_id =album.ID

    try:
        os.remove(app.config['USER_DATA'] + 'data/' + user_name + '/img/' + album_title + '/' + img_title)
    except:
        pass

    # Delete Photos from ElasticSearch
    p = db_session_instance.query(Photo).filter(Photo.album_ID == album_id).filter(Photo.photo_title == img_title).first()
    from web.index.esclient import es
    photo_index_doc = doctype.Photo.get(id = p.ID, using = es)
    photo_index_doc.delete(using = es)
    #################################

    db_session_instance.query(Photo).filter(Photo.album_ID == album_id).filter(Photo.photo_title == img_title).delete()

    db_session_instance.commit()
    ret['status'] = 'ok'
    return ret

@mod.route('/folder/rename', methods = ['POST'])
@loginRequest
def folderRename():
    ret = dict()
    try:
        old_folder_name = request.json['old']
        new_folder_name = request.json['new']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    db_session_instance = databases.db_session()
    folder = db_session_instance\
        .query(Folder)\
        .filter(Folder.user_ID == g.user_id).filter(Folder.folder_title == old_folder_name)\
        .first()
    if folder is None:
        ret['status'] = 'Folder Not Exist!'
        return ret

    # Update the folder information for those post in the folder
    posts = db_session_instance\
        .query(Post).join(Folder)\
        .filter(Folder.user_ID == g.user_id).filter(Folder.folder_title == old_folder_name)\
        .all()
    from web.index.esclient import es
    for p in posts:
        post_index_doc = doctype.Post(meta = {'id': p.ID}, post_title = p.post_title, post_content = p.post_content, folder_name = new_folder_name)
        post_index_doc.save(using=es)
    ########################################

    folder.folder_title = new_folder_name
    db_session_instance.commit()
    ret['status'] = 'ok'
    return ret

@mod.route('/folder/delete', methods = ['POST'])
@loginRequest
def folderDelete():
    ret = dict()
    db_session_instance = databases.db_session()
    try:
        delete_folder_title = request.json['title']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    folder = db_session_instance\
        .query(Folder)\
        .filter(Folder.user_ID == g.user_id).filter(Folder.folder_title == delete_folder_title)\
        .first()

    posts = db_session_instance\
        .query(Post).join(Folder)\
        .filter(Folder.ID == folder.ID)\
        .all()
    
    from web.index.esclient import es
    for p in posts:
        post_index_doc = doctype.Post.get(id = p.ID, using = es)
        post_index_doc.delete(using = es)
    
    db_session_instance\
        .query(Folder)\
        .filter(Folder.user_ID == g.user_id).filter(Folder.folder_title == delete_folder_title)\
        .delete()
    db_session_instance.commit()
    ret['status'] = 'ok'
    return ret

@mod.route('/post/publish', methods = ['POST'])
@loginRequest
def editPostPublish():
    ret = dict()
    try:
        publish_folder = request.json['folder']
        publish_post = request.json['title']
        publish_status = request.json['publish']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    db_session_instance = databases.db_session()

    post = db_session_instance\
        .query(Post).join(Folder)\
        .filter(Folder.user_ID == g.user_id).filter(Folder.folder_title == publish_folder).filter(Post.post_title == publish_post)\
        .first()
    if post is None:
        ret['status'] = 'Post Not Exist!'
        return ret
    post.is_published = publish_status
    db_session_instance.commit()

    ret['status'] = 'ok'
    return ret

@mod.route('/post/rename', methods = ['POST'])
@loginRequest
def editPostRename():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        rename_folder = request.json['folder']
        old_name = request.json['title']
        new_name = request.json['newTitle']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    post = db_session_instance\
        .query(Post).join(Folder)\
        .filter(Folder.user_ID == g.user_id).filter(Folder.folder_title == rename_folder).filter(Post.post_title == old_name)\
        .first()

    if post is None:
        ret['status'] = 'Post Not Exist!'
        return ret

    from web.index.esclient import es
    post_index_doc = doctype.Post(meta = {'id': post.ID}, post_title = new_name, post_content = post.post_content, folder_name = rename_folder)
    post_index_doc.save(using = es)

    post.post_title = new_name
    db_session_instance.commit()

    ret['status'] = 'ok'
    return ret

@mod.route('/post/delete', methods = ['POST'])
@loginRequest
def editPostDelete():
    ret = dict()
    db_session_instance = databases.db_session()
    try:
        folder = request.json['folder']
        title = request.json['title']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    post = db_session_instance\
        .query(Post).join(Folder)\
        .filter(Folder.user_ID == g.user_id).filter(Folder.folder_title == folder).filter(Post.post_title == title)\
        .first()
    
    if post is None:
        ret['status'] = 'Post Not Exist!'
        return ret

    from web.index.esclient import es
    post_index_doc = doctype.Post.get(id = post.ID, using = es)
    post_index_doc.delete()

    db_session_instance\
        .query(Post).join(Folder)\
        .filter(Folder.user_ID == g.user_id).filter(Folder.folder_title == folder).filter(Post.post_title == title)\
        .delete()
    db_session_instance.commit()


    ret['status'] = 'ok'
    return ret