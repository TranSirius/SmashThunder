from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request

from web.db import databases
from web.db.datamodels import User, Album, Photo, MainPage, Comment, Post, Folder, Follow
from web.logic.geter import GetPhotos
from web.logic.geter import GetFolderDetail
from web.logic.geter import GetPost
from web.logic.geter import GetFolder
from web.logic.geter import GetStar
from web.views.auth import loginRequest

mod = Blueprint('get', __name__, url_prefix = '/get')

@mod.route('/album', methods = ['POST'])
def album():
    ret = dict()
    db_session = databases.db_session()
    user_name = request.json['username']
    request_user = db_session.query(User).filter(User.user_name == user_name).first()

    if request_user == None:
        ret['status'] = 'User Does Not Exist!'
        return ret
        
    request_user_id = request_user.ID
    request_user_name = request_user.user_name
    target_album = None
    if 'target' in request.json:
        target_album = request.json['target']

    geter = GetPhotos()
    try:
        ret_album = geter(user_name = request_user_name, album_name = target_album)
        ret['albums'] = ret_album
    except:
        ret['status'] = "Something wrong"
    else:
        ret['status'] = 'ok'
        return ret

@mod.route('/post', methods = ['POST'])
def getPost():
    ret = dict()
    try:
        user_name = request.json['username']
        folder_name = request.json['folder']
        post_name = request.json['postTitle']
    except:
        ret['status'] = 'Requesting Format Error!'
        return ret

    geter = GetPost()
    post = geter(user_name, folder_name, post_name)
    if post is None:
        ret['status'] = 'Post Not Exist!'
    else:
        ret = post
        ret['status'] = 'ok'
        return ret



@mod.route('/post/foldersDetail', methods = ['POST'])
def postFolderDetail():
    user_id = g.user_id
    ret = dict()
    geter = GetFolderDetail()
    ret['folders'] = geter(user_id)
    ret['status'] = 'ok'
    return ret

@mod.route('/post/folders', methods = ['POST'])
@loginRequest
def postFolders():
    user_id = g.user_id
    ret = dict()
    geter = GetFolder()
    ret['folders'] = geter(user_id)
    ret['status'] = 'ok'
    return ret

@mod.route('/mainpage', methods = ['POST'])
def getMainPage():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        user_name = request.json['username']
    except:
        ret['status'] = 'Requesting Format Error!'
        return ret

    qry = db_session_instance\
        .query(MainPage, Folder.folder_title).join(User, User.ID == MainPage.user_id).join(Post)\
        .filter(User.user_name == user_name).filter(Post.folder_ID == Folder.ID)\
        .first()

    if qry is None:
        ret['status'] = 'ok'
        ret['exist'] = False
        return ret

    main_page, main_page_folder = qry

    ret['exist'] = True
    geter = GetPost()
    return_post = geter.getByPostID(post_id = main_page.post_id)
    if return_post is None:
        ret['status'] = 'Main Page Not Exist! Data Consistency Error!'
        return ret

    ret['post'] = return_post
    ret['post']['folder'] = main_page_folder
    ret['status'] = 'ok'
    return ret

@mod.route('/star', methods = ['POST'])
def getStar():
    ret = dict()

    try:
        username = request.json['username']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    ret['stars'] = GetStar()()
    ret['status'] = 'ok'
    return ret


@mod.route('/follow', methods = ['POST'])
def getFollow():
    ret = dict()
    db_session_instance = databases.db_session()
    try:
        username = request.json['username']
    except:
        ret['status'] = 'Request Format Error!'
        return ret
    
    user = db_session_instance\
        .query(User)\
        .filter(User.user_name == username)\
        .first()

    follower, _ = db_session_instance\
        .query(User.user_name, Follow)\
        .filter(Follow.followee_id == user.ID).filter(Follow.follower_id == User.ID)\
        .all()
    
    follower_list = [f.user_name for f in follower]

    followee, _ = db_session_instance\
        .query(User.user_name, Follow)\
        .filter(Follow.follower_id == user.ID).filter(Follow.followee_id == User.ID)\
        .all()
    
    followee_list = [f.user_name for f in followee]

    ret['followings'] = followee_list
    ret['followers'] = follower_list
    ret['status'] = 'ok'
    return ret

@mod.route('/news', methods = ['POST'])
def getNew():
    ret = dict()
    db_session_instance = databases.db_session()
    try:
        target = request.json['target']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    posts = []
    if target == 'news':
        news = db_session_instance\
            .query(Post.create_time, Post.description, Post.cover_album, Post.cover_photo, Post.post_title ,User.user_name, Folder.folder_title)\
            .filter(User.ID == Folder.user_ID).filter(Post.folder_ID == Folder.ID)\
            .limit(20)\
            .all()
        for create_time, description, cover_album, cover_photo, title, username, folder_title in news:
            single_news = dict()
            single_news['title'] = title
            single_news['author'] = username
            single_news['description'] = description
            single_news['coverAlbum'] = cover_album
            single_news['coverImage'] = cover_photo
            single_news['time'] = create_time
            single_news['folder'] = folder_title
            posts.append(single_news)

    elif target == 'friendsActivities':
        if g.user_id is None:
            ret['status'] = 'Please Login First!'
            return ret

        news = db_session_instance\
            .query(
                Post.create_time, 
                Post.description, 
                Post.cover_album, 
                Post.cover_photo, 
                Post.post_title ,
                User.user_name, 
                Folder.folder_title,
                ).join(
                 Follow,
                 User.ID == Follow.followee_id
                )\
            .filter(User.ID == Folder.user_ID).filter(Post.folder_ID == Folder.ID).filter(Follow.follower_id == g.user_id)\
            .limit(20)\
            .all()
        
        for create_time, description, cover_album, cover_photo, title, username, folder_title in news:
            single_news = dict()
            single_news['title'] = title
            single_news['author'] = username
            single_news['description'] = description
            single_news['coverAlbum'] = cover_album
            single_news['coverImage'] = cover_photo
            single_news['time'] = create_time
            single_news['folder'] = folder_title
            posts.append(single_news)

    else:
        ret['status'] = 'Request Format Error! target error!'
        return ret

    ret['status'] = 'ok'
    ret['posts'] = posts
    return ret

@mod.route('/posts', methods = ['POST'])
@loginRequest
def getUsersPosts():
    ret = dict()
    try:
        username = request.json['username']
    except:
        ret['status'] = 'Request Format Error!'
        return ret
    ret['folders'] = GetFolderDetail().getPosts(username)
    ret['status'] = 'ok'
    return ret