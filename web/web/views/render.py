import pypandoc as pdc

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request

from web.db import databases
from web.db.datamodels import Post, Folder, User

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

mod = Blueprint('render', __name__, url_prefix = '/render')

@mod.route('/', methods = ['POST'])
def renderPost():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        username = request.json['username']
        folder = request.json['folder']
        post = request.json['post']
        target_format = request.json['format']
    except:
        ret['status'] = 'Requesting Format Error!'
        return ret

    down_post = db_session_instance\
        .query(Post).join(Folder).join(User)\
        .filter(User.user_name == username).filter(Folder.folder_title == folder).filter(Post.post_title == post)\
        .first()
    if down_post is None:
        ret['status'] = 'Post Not Exist!'
        return ret

    source_format = down_post.document_format
    source_content = down_post.post_content

    pdc.convert_text(
        source = source_content,
        to = 'docx',
        format = target_format,
        outputfile = '/share/render/' + post + '.docx'
    )

    ret['status'] = 'ok'
    return ret