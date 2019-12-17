from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

from web.db import databases
from web.db.datamodels import User, Album, Photo, MainPage, Comment, Post, Folder, Follow, Report
from web.logic.geter import GetPhotos
from web.logic.geter import GetFolderDetail
from web.logic.geter import GetPost
from web.logic.geter import GetFolder
from web.logic.geter import GetStar
from web.views.auth import loginRequest, adminRequest

from web.index import doctype
from web.index import esclient

mod = Blueprint('admin', __name__, url_prefix = '/admin')


@mod.route('/comment/delete/author', methods = ['POST'])
@loginRequest
def deleteComment():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        comment_id = request.json['id']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    comment = db_session_instance\
        .query(Comment).join(Post).join(Folder).join(User)\
        .filter(User.ID == g.user_id).filter(Comment.ID == comment_id)\
        .first()

    if comment is None:
        ret['status'] = 'You are not Allowed to Delete this Comment'
        return ret
    
    from web.index.esclient import es
    try:
        comment_index_doc = doctype.Comment.get(id = comment.ID, using = es)
        comment_index_doc.delete(using = es)
    except:
        pass

    # db_session_instance\
    #     .query(Comment).join(Post).join(Folder).join(User)\
    #     .filter(User.ID == g.user_id).filter(Comment.ID == comment_id)\
    #     .delete()

    db_session_instance.delete(comment)
    db_session_instance.commit()
    ret['status'] = 'ok'
    return ret