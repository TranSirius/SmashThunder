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
from web.db.datamodels import User, Album, Photo, Post, Folder, Comment, MainPage, Star, Follow, Report

from web.index import doctype

from web.views.auth import loginRequest, adminRequest
from web.logic.utils import CurrentTime, UUID


mod = Blueprint('submit', __name__, url_prefix = '/submit')

@mod.route('/img', methods = ['POST'])
@loginRequest
def uploadPic():
    ret = dict()
    db_session_instance = databases.db_session()
    query_res = db_session_instance.query(User).filter(User.ID == g.user_id).first()
    
    user_name = query_res.user_name
    pic_dir = app.config['USER_DATA'] + 'data/' + user_name + '/img/'

    img_list = request.files.getlist('files')

    unix_time = CurrentTime()()
    album_title = request.form.get('albumTitle')

    album = db_session_instance.query(Album).filter(Album.user_ID == g.user_id).filter(Album.album_title == album_title).first()
    if album is None:
        album = Album.generateAlbum(user_name, album_title, unix_time)
        # album = db_session_instance.query(Album).filter(Album.user_ID == g.user_id).filter(Album.album_title == album_title).first()

    for img in img_list:
        old_record = db_session_instance.query(Photo).filter(Photo.photo_title == img.filename).filter(Photo.album_ID == album.ID).first()
        if old_record is None:
            new_id = UUID()()
            new_img = Photo(ID = new_id, album_ID = album.ID, photo_title = img.filename, create_time = unix_time)
            db_session_instance.add(new_img)
        else:
            old_record.create_time = unix_time
        img.save(app.config['USER_DATA'] + 'data/' + user_name + '/img/' + album_title + '/' + img.filename)
    db_session_instance.commit()

    from web.index.esclient import es
    for img in img_list:
        img = db_session_instance.query(Photo).filter(Photo.album_ID == album.ID).filter(Photo.photo_title == img.filename).first()
        img_id = img.ID
        img_index = doctype.Photo(meta = {'id':img_id}, photo_name = img.photo_title)
        img_index.save(using = es)

    ret['status'] = 'ok'
    return ret
    

@mod.route('/post', methods = ['POST'])
@loginRequest
def uploadPost():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        post_title = request.json['title']
        folder_title = request.json['folder']
        post_format = request.json['format']
        post_content = request.json['content']
        is_published = request.json['published']
    except KeyError:
        ret['status'] = "KeyError!"
        return ret
    
    description = request.json['description'] if 'description' in request.json else None
    cover_album = request.json['coverAlbum'] if 'coverAlbum' in request.json else None
    cover_photo = request.json['coverImage'] if 'coverImage' in request.json else None

    unix_time = CurrentTime()()

    folder = db_session_instance\
        .query(Folder).join(User)\
        .filter(User.ID == g.user_id).filter(Folder.folder_title == folder_title)\
        .first()

    if folder is None:
        folder = Folder(user_ID = g.user_id, folder_title = folder_title, create_time = unix_time)
        db_session_instance.add(folder)
        db_session_instance.commit()

    old_post = db_session_instance.query(Post).filter(Post.post_title == post_title).filter(Post.folder_ID == folder.ID).first()
    if old_post is None:
        post_id = UUID()()
        new_post = Post(
            ID = post_id, 
            folder_ID = folder.ID, 
            post_title = post_title, 
            create_time = unix_time, 
            document_format = post_format, 
            post_content = post_content, 
            is_published = is_published, 
            description = description, 
            cover_album = cover_album, 
            cover_photo = cover_photo
        )
        db_session_instance.merge(new_post)
    else:
        old_post.post_content = post_content
        old_post.create_time = unix_time
        old_post.is_published = is_published
        old_post.description = str(description)
        old_post.cover_album = str(cover_album)
        old_post.cover_photo = str(cover_photo)
        old_post.document_format = str(post_format)
        
        post_id = old_post.ID
    db_session_instance.commit()

    from web.index.esclient import es
    post_index = doctype.Post(meta={'id':post_id}, post_title = post_title, post_content = post_content, folder_name = folder_title)
    post_index.save(using = es)
    ret['status'] = 'ok'
    return ret

@mod.route('/mainpage', methods = ['POST'])
@loginRequest
def submitMainPage():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        folder = request.json['folder']
        title = request.json['title']
    except KeyError:
        ret['status'] = "KeyError!"
        return ret

    post = db_session_instance\
        .query(Post).join(Folder)\
        .filter(Folder.user_ID == g.user_id).filter(Folder.folder_title == folder).filter(Post.post_title == title)\
        .first()

    mainpage = MainPage(user_id = g.user_id, post_id = post.ID)
    db_session_instance.merge(mainpage)
    db_session_instance.commit()

    ret['status'] = 'ok'
    return ret

@mod.route('/comment', methods = ['POST'])
@loginRequest
def uploadComment():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        author_name = request.json['username']
        folder_name = request.json['folder']
        post_title = request.json['post']
        comment = request.json['comment']
    except KeyError:
        ret['status'] = "KeyError!"
        return ret

    post = db_session_instance\
        .query(Post).join(Folder).join(User)\
        .filter(Folder.folder_title == folder_name).filter(Post.post_title == post_title).filter(User.user_name == author_name)\
        .first()
    if post is None:
        ret['status'] = 'Post Not Exist!'
        return ret

    post_id = post.ID
    user_id = g.user_id
    unix_time = CurrentTime()()
    comment_id = UUID()()

    new_comment = Comment(ID = comment_id, user_id = user_id, post_id = post_id, content = comment, create_time = unix_time)
    db_session_instance.add(new_comment)
    db_session_instance.commit()

    from web.index.esclient import es
    comment_index = doctype.Comment(meta={'id':post_id}, content = comment)
    comment_index.save(using=es)

    ret['status'] = 'ok'
    return ret


@mod.route('/star', methods = ['POST'])
@loginRequest
def submitStar():
    ret = dict()
    db_session_instance = databases.db_session()
    print(request.json)
    try:
        user = request.json['username']
        folder = request.json['folder']
        title = request.json['post']
        star_flag = request.json['star']
    except:
        ret['status'] = "Request Format Error!"
        return ret

    post = db_session_instance\
        .query(Post).join(Folder).join(User)\
        .filter(User.user_name == user).filter(Folder.folder_title == folder).filter(Post.post_title == title)\
        .first()

    if star_flag:
        star = Star(user_id = g.user_id, post_id = post.ID)
        db_session_instance.merge(star)
        db_session_instance.commit()
        ret['status'] = 'ok'
    else:
        db_session_instance\
            .query(Star)\
            .filter(Star.user_id == g.user_id).filter(Star.post_id == post.ID)\
            .delete()
        db_session_instance.commit()
        ret['status'] = 'ok'
    return ret

@mod.route('/follow', methods = ['POST'])
@loginRequest
def followAPI():
    ret = dict()
    db_session_instance = databases.db_session()
    try:
        follow_flag = request.json['follow']
        follow_target = request.json['target']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    followee_id = db_session_instance\
        .query(User)\
        .filter(User.user_name == follow_target)\
        .first()\
        .ID
    follower_id = g.user_id
    if followee_id == follower_id:
        ret['status'] = 'You Cannot Follow Yourself!'
        return ret

    if follow_flag:
        follow = Follow(follower_id = follower_id, followee_id = followee_id)
        db_session_instance.merge(follow)
        db_session_instance.commit()
        ret['status'] = 'ok'
        return ret
    else:
        follow = db_session_instance\
            .query(Follow)\
            .filter(Follow.followee_id == followee_id).filter(Follow.follower_id == follower_id)\
            .delete()
        db_session_instance.commit()
        ret['status'] = 'ok'
        return ret

@mod.route('/report', methods = ['POST'])
@loginRequest
def submitReport():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        reporter = request.json['reporter']
        target = request.json['target']
        reason = request.json['reason']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    report = Report(reporter_id = g.user_id, description = str(reason), target = target)
    db_session_instance.add(report)
    db_session_instance.commit()

    ret['status'] = 'ok'
    return ret

@mod.route('/dismiss', methods = ['POST'])
@loginRequest
@adminRequest
def submitDismiss():
    ret = dict()
    try:
        target = request.json['target']
    except:
        ret['status'] = 'Request Format Error'
        return ret

    db_session_instance = databases.db_session()
    report = db_session_instance\
        .query(Report)\
        .filter(Report.ID == int(target))\
        .first()
    report.seen = True
    db_session_instance.commit()
    ret['status'] = 'ok'
    return ret

@mod.route('/ban', methods = ['POST'])
@loginRequest
@adminRequest
def submitBan():
    ret = dict()
    try:
        report = request.json['report']
        target = request.json['target']
    except:
        ret['status'] = 'Request Format Error'
        return ret
    
    db_session_instance = databases.db_session()
    report = db_session_instance\
        .query(Report)\
        .filter(Report.ID == int(report))\
        .first()
    report.seen = True

    user = db_session_instance\
        .query(User)\
        .filter(User.user_name == target)\
        .first()
    user.ban = True
    
    db_session_instance.commit()
    ret['status'] = 'ok'
    return ret