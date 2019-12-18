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

@mod.route('', methods = ['POST'])
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

    if target_format not in ['docx', 'pdf']:
        target_format = 'pdf'

    down_post = db_session_instance\
        .query(Post).join(Folder).join(User)\
        .filter(User.user_name == username).filter(Folder.folder_title == folder).filter(Post.post_title == post)\
        .first()
    if down_post is None:
        ret['status'] = 'Post Not Exist!'
        return ret

    source_format = down_post.document_format
    source_content = down_post.post_content

    import re
    source_content = re.sub('[!]\[(.+)\][(](.+)[)]', '![\g<1>](http://localhost/data/ceshiceshi/img/\g<2>)', source_content)


    if target_format == 'pdf' and source_format == 'md':
        try:
            pdc.convert_text(
                source = source_content,
                to = 'pdf',
                format = source_format,
                outputfile = '/share/render/' + post + '.pdf',
                extra_args = ('--pdf-engine=xelatex', '--template=/share/render/template/template.latex',)
            )
        except:
            ret['status'] = 'Something wrong during the conversion, standard latex syntax is required!'
            return ret
        ret['filename'] = post + '.pdf'

    elif target_format == 'pdf' and source_format == 'tex':
        try:
            pdc.convert_text(
                source = source_content,
                to = 'pdf',
                format = source_format,
                outputfile = '/share/render/' + post + '.pdf',
                extra_args = ('--pdf-engine=xelatex',)
            )
        except:
            ret['status'] = 'Something wrong during the conversion, standard latex syntax is required!'
            return ret
        ret['filename'] = post + '.pdf'

    else:
        try:
            pdc.convert_text(
                source = source_content,
                to = 'docx',
                format = source_format,
                outputfile = '/share/render/' + post + '.docx'
            )
        except:
            ret['status'] = 'Something wrong during the conversion'
            return ret
        ret['filename'] = post + '.docx'


    ret['status'] = 'ok'
    return ret