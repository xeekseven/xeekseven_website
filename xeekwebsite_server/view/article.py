from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from xeekwebsite_server.db import get_db

import json
import uuid
import datetime
from xeekwebsite_server.util import execption_handle
from xeekwebsite_server.LogFactory import LogInfo

bp = Blueprint('article', __name__, url_prefix='/article')


@bp.route('/index/<string:id>')
@bp.route('/<string:id>')
@execption_handle
def index(id):
    print("Get id %s" % id)
    db = get_db()
    sql = "SELECT * FROM article  inner join article_content where article.article_id == article_content.article_id and  article.article_id = '%s' order by article_index;" % id
    result = db.execute(sql)
    article_list = {}
    content_list = []
    articles = result.fetchall()
    for item in articles:
        content_list.append(json.loads(str(item['article_value']).replace('\'','\"')))
    
    article_list['introduction'] = articles[0]['article_introduction']
    article_list['view_count'] = articles[0]['article_view_count']
    article_list['scan_count'] = articles[0]['article_scan_count']
    article_list['content_list'] = content_list
    
    return render_template('article/index.html',article_list=article_list)

@bp.route('/markdown/<string:id>')
@execption_handle
def markdown(id):
    sql = 'SELECT * FROM article_markdown WHERE markdown_id = ?'
    LogInfo().logger.info('查询markdown:%s,id:%s' % (sql,id))
    markdown = {}
    result = get_db().execute(sql,(id,)).fetchone()
    markdown['markdown_id'] = result['markdown_id']
    markdown['content'] = result['content']
    markdown['title'] = result['title']
    markdown['tag'] = result['tag']
    return render_template('article/markdown.html',markdown=markdown)

@bp.route('/edit/<string:id>')
@bp.route('/edit/')
@login_required
@execption_handle
def edit(id=None):
    article = {
        'content':''
    }
    if id != '0' or id == None:
        db=get_db()
        sql = 'SELECT * FROM article_markdown WHERE markdown_id=?'
        article_tuple = db.execute(sql,(id,)).fetchone()
        LogInfo().logger.info('接收到ID为:%s,sql:%s' % (id,sql))
        article['markdown_id'] = article_tuple['markdown_id']
        article['content'] = article_tuple['content']
        article['title'] = article_tuple['title']
        article['tag'] = article_tuple['tag']
    return render_template('article/edit.html',article=article)

@bp.route('/publish',methods=['POST'])
@execption_handle
def publish():
    data = request.get_data(as_text=True)
    json_re = json.loads(data)
    db = get_db()
    uid = uuid.uuid1()
    is_exist = db.execute('SELECT 1 FROM article_markdown WHERE markdown_id = ?',(json_re['markdown_id'],)).fetchone()
    if is_exist == None:
        
        db.execute(
            'INSERT INTO article_markdown (id, markdown_id, author_id,title,content,create_time,modefied_time,tag)'
            ' VALUES (null, ?, ?, ?, ?, ?, ?, ?)',
            (json_re['markdown_id']+str(uid),json_re['author_id'],json_re['title'],json_re['content'].replace('\n','\\n').strip('"'),
            datetime.datetime.now().strftime('%Y-%m-%d'),
            datetime.datetime.now().strftime('%Y-%m-%d'),json_re['tag'])     
        )
        db.commit()
        LogInfo().logger.info('/article/publish => 新增数据')
    else:
        db.execute(
            'UPDATE article_markdown SET content = ? WHERE markdown_id = ?',
            (json_re['content'].replace('\n','\\n').strip('"'),json_re['markdown_id'])
        )
        db.execute(
            'UPDATE article_markdown SET title = ? WHERE markdown_id = ?',
            (json_re['title'].strip('"'),json_re['markdown_id'])
        )
        db.execute(
            'UPDATE article_markdown SET tag = ? WHERE markdown_id = ?',
            (json_re['tag'].strip('"'),json_re['markdown_id'])
        )
        db.commit()
        LogInfo().logger.info('/article/publish => 更新数据%s' % json_re['markdown_id'])
    
    return json.dumps({'status':'success'})

@bp.route('/delete/<string:id>', methods=['GET'])
@execption_handle
@login_required
def delete(id):
    db=get_db()
    is_markdown_exist = db.execute('SELECT 1 FROM article_markdown WHERE markdown_id = ?',(id,)).fetchone()
    is_artice_exist = db.execute('SELECT 1 FROM article WHERE article_id = ?',(id,)).fetchone()
    if is_markdown_exist == None and is_artice_exist == None:
        LogInfo().logger.info('查不到要删除的Markdown或者article ID:%s')
        return json.dumps({'status':'查不到要删除的Markdown或者article'})

    elif is_markdown_exist != None:
        LogInfo().logger.info('删除的Markdown ID:%s')
        sql = 'DELETE FROM article_markdown WHERE markdown_id = ? '
        db.execute(sql,(id,))
        db.commit()
        return json.dumps({'status':'markdown delete success!'})
    else:
        LogInfo().logger.info('删除的article ID:%s')
        sql1 = 'DELETE FROM article_content WHERE article_id = ? '
        sql2 = 'DELETE FROM article WHERE article_id = ? '
        db.execute(sql1,(id,))
        db.execute(sql2,(id,))
        db.commit()
        return json.dumps({'status':'article delete success!'})