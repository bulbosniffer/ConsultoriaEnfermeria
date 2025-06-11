from flask import Blueprint, render_template, redirect, session, url_for
from app.models import Archivo

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    # Consulta con SQLAlchemy ordenando por fecha_subida descendente
    archivos = Archivo.query.order_by(Archivo.fecha_subida.desc()).all()

    return render_template('index.html', archivos=archivos, usuario=session['usuario'], es_admin=(session.get('rol') == 'admin'))
