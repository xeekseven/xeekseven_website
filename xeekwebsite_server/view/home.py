from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from xeekwebsite_server.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

import datetime
from xeekwebsite_server.util import execption_handle

bp = Blueprint('home', __name__,url_prefix='/home')

@bp.route('/index')
@bp.route('/')
@execption_handle
def index():
    arcList = get_article_list()
    return render_template('home/index.html',arcList=arcList)

def get_article_list():
    arcList=[]
    article_sql = 'select * from article as ar inner join author as au where ar.author_id=au.author_id order by ar.article_modefiedtime limit 0,12'
    markdown_sql = 'SELECT * FROM article_markdown AS am INNER JOIN author AS au WHERE am.author_id = au.author_id ORDER BY am.create_time limit 0,12'
    db = get_db()
    articles = db.execute(article_sql).fetchall()
    markdowns = db.execute(markdown_sql).fetchall()
    for arc in articles:
        item = { 
            'id':arc['article_id'],
            'modefiedtime':arc['article_modefiedtime'],
            'tag':arc['article_tag'],
            'imgpath':arc['article_imgpath'],
            'title':arc['article_title'],
            'subtitle':arc['article_subtitle']
        }
        arcList.append(item)
    for mkitem in markdowns:
        item = {
            'id':mkitem['markdown_id'],
            'modefiedtime':mkitem['modefied_time'],
            'tag':mkitem['tag'],
            'imgpath':'static/img/mkdown.jpg',
            'title':mkitem['title'],
            'subtitle':'markdown need not subtitle'
        }
        arcList.append(item)
    return arcList



@bp.route('/<int:id>/delete', methods=('POST',))
@execption_handle
@login_required
def delete(id):
   
    return redirect(url_for('home.index'))