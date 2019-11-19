from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request

from web.db import databases
from web.db.datamodels import User, Album, Photo, MainPage, Comment
from web.logic.geter import GetPhotos
from web.logic.geter import GetFolderDetail
from web.logic.geter import GetPost
from web.logic.geter import GetFolder
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

    main_page = db_session_instance\
        .query(MainPage).join(User)\
        .filter(User.user_name == user_name)\
        .first()

    if main_page is None:
        ret['status'] = 'ok'
        ret['exist'] = False
        return ret
    ret['exist'] = True
    geter = GetPost()
    return_post = geter.getByPostID(post_id = main_page.post_id)
    if post is None:
        ret['status'] = 'Main Page Not Exist! Data Consistency Error!'
        return ret

    ret['post'] = return_post
    ret['status'] = 'ok'
    return ret