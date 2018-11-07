import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('/')
def index():
    
    return redirect(url_for('home.index'))