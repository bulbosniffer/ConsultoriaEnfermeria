from flask import Blueprint, render_template, redirect, session, url_for, flash
from app.utils.db import get_db_connection

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    archivos = conn.execute('SELECT * FROM archivos ORDER BY fecha_subida DESC').fetchall()
    conn.close()

    return render_template('index.html', archivos=archivos, usuario=session['usuario'], es_admin=(session.get('rol') == 'admin'))