from flask import Blueprint, current_app, render_template, request, redirect, send_from_directory, session, flash, url_for
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
        flash('Todos los campos son obligatorios.', 'warning')
        return redirect(url_for('formatos.formatos'))

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # 🔧 Ruta absoluta y segura
        upload_folder = os.path.abspath(os.path.join(current_app.root_path, '..', 'static', 'uploads'))
        os.makedirs(upload_folder, exist_ok=True)
        path = os.path.join(upload_folder, filename)
        file.save(path)
        
        #upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        #os.makedirs(upload_folder, exist_ok=True)  # crea la carpeta si no existe

        #path = os.path.join(upload_folder, filename)
        #file.save(path)

        nuevo_archivo = Archivo(
            filename=filename,
            nombre_formato=nombre_formato,
            area=area
        )
        db.session.add(nuevo_archivo)
        db.session.commit()

        flash('Archivo subido correctamente.', 'success')
    else:
        flash('Tipo de archivo no permitido.', 'danger')

    return redirect(url_for('formatos.formatos'))

@bp.route('/download/<filename>')
def download_file(filename):
    """Handle file download"""
    if 'usuario' not in session:
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('auth.login'))

    try:
        # Asegura el nombre del archivo
        filename = secure_filename(filename)
        
        # Ruta absoluta del directorio de subida
        #upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        upload_folder = os.path.abspath(os.path.join(current_app.root_path, '..', 'static', 'uploads'))
        file_path = os.path.join(upload_folder, filename)

        # Verifica si está en la base de datos
        archivo = Archivo.query.filter_by(filename=filename).first()
        if not archivo:
            flash('Archivo no encontrado en la base de datos.', 'warning')
            return redirect(url_for('formatos.formatos'))

        # Verifica si existe físicamente
        print("📁 Ruta absoluta buscada:", file_path)
        if not os.path.exists(file_path):
            flash('Archivo no disponible en el servidor.', 'warning')
            return redirect(url_for('formatos.formatos'))

        return send_from_directory(upload_folder, filename, as_attachment=True)

    except Exception as e:
        current_app.logger.error(f"Error downloading file {filename}: {str(e)}")
        flash('Error al descargar el archivo.', 'danger')
        return redirect(url_for('formatos.formatos'))

@bp.route('/delete/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    """Handle file deletion"""
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('No autorizado.', 'danger')
        return redirect(url_for('auth.login'))

    try:
        # Find file in database
        archivo = Archivo.query.get(file_id)
        
        if not archivo:
            flash('Archivo no encontrado.', 'warning')
            return redirect(url_for('formatos.formatos'))

        # Delete physical file
        upload_folder = os.path.abspath(os.path.join(current_app.root_path, '..', 'static', 'uploads'))
        file_path = os.path.join(upload_folder, archivo.filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete from database
        db.session.delete(archivo)
        db.session.commit()
        
        flash('Archivo eliminado correctamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting file {file_id}: {str(e)}")
        flash('Error al eliminar el archivo.', 'danger')

    return redirect(url_for('formatos.formatos'))

@bp.route('/files')
def list_files():
    """List all files (admin only)"""
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('No autorizado.', 'danger')
        return redirect(url_for('auth.login'))
    
    try:
        archivos = Archivo.query.all()
        return render_template('files/list.html', archivos=archivos)
    except Exception as e:
        current_app.logger.error(f"Error listing files: {str(e)}")
        flash('Error al cargar la lista de archivos.', 'danger')
        return redirect(url_for('formatos.formatos'))

# Additional utility routes
@bp.route('/file/<int:file_id>/info')
def file_info(file_id):
    """Get file information"""
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('No autorizado.', 'danger')
        return redirect(url_for('auth.login'))
    
    archivo = Archivo.query.get_or_404(file_id)
    upload_folder = os.path.abspath(os.path.join(current_app.root_path, '..', 'static', 'uploads'))
    file_path = os.path.join(upload_folder, archivo.filename)
    
    file_stats = {
        'exists': os.path.exists(file_path),
        'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
        'modified': os.path.getmtime(file_path) if os.path.exists(file_path) else None
    }
    
    return render_template('files/info.html', archivo=archivo, file_stats=file_stats)