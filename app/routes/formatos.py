from flask import Blueprint, render_template, request, redirect, session, flash, url_for
import os
from werkzeug.utils import secure_filename
from app.utils.helpers import allowed_file
from app.utils.db import db
from app.models import Archivo

bp = Blueprint('formatos', __name__)

@bp.route('/formatos', methods=['GET', 'POST'])
def formatos():
    if 'usuario' not in session:
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('auth.login'))

    archivos = Archivo.query.order_by(Archivo.fecha_subida.desc()).all()

    return render_template('index.html', archivos=archivos, usuario=session['usuario'], es_admin=(session['rol'] == 'admin'))

@bp.route('/upload', methods=['POST'])
def upload():
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('No autorizado.', 'danger')
        return redirect(url_for('auth.login'))

    file = request.files.get('file')
    nombre_formato = request.form.get('nombre_formato')
    area = request.form.get('area')

    if not file or not nombre_formato or not area:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('formatos.formatos'))

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join('static/uploads', filename)
        file.save(path)

        nuevo_archivo = Archivo(
            filename=filename,
            nombre_formato=nombre_formato,
            area=area
        )
        db.session.add(nuevo_archivo)
        db.session.commit()

        flash('Archivo subido correctamente.')
    else:
        flash('Tipo de archivo no permitido.')

    return redirect(url_for('formatos.formatos'))
