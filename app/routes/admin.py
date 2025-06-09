from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.models import Usuario
from app.utils.db import db
from werkzeug.security import generate_password_hash

bp = Blueprint('admin', __name__)

@bp.route('/admin')
def panel():
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('admin.html', usuario=session['usuario'])

@bp.route('/admin/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))

    if usuario_id == obtener_id_usuario_actual():
        flash('No puedes editar tu propio usuario desde aquí.', 'warning')
        return redirect(url_for('admin.lista_usuarios'))

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        flash('Usuario no encontrado.', 'warning')
        return redirect(url_for('admin.lista_usuarios'))

    if request.method == 'POST':
        nuevo_rol = request.form['rol']
        nueva_contra = request.form.get('contrasena')

        usuario.rol = nuevo_rol
        if nueva_contra:
            usuario.contrasena = generate_password_hash(nueva_contra).encode('utf-8')
        db.session.commit()

        flash('Usuario actualizado.', 'success')
        return redirect(url_for('admin.lista_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@bp.route('/admin/eliminar_usuario/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))

    usuario_actual = Usuario.query.filter_by(usuario=session['usuario']).first()
    if usuario_actual and usuario_id == usuario_actual.id:
        flash('No puedes eliminar tu propio usuario.', 'warning')
        return redirect(url_for('admin.lista_usuarios'))

    usuario = Usuario.query.get(usuario_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado correctamente.', 'success')
    else:
        flash('Usuario no encontrado.', 'warning')

    return redirect(url_for('admin.lista_usuarios'))

@bp.route('/admin/usuarios')
def lista_usuarios():
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))

    usuarios = Usuario.query.order_by(Usuario.id).all()
    return render_template('usuarios.html', usuarios=usuarios)

def obtener_id_usuario_actual():
    usuario = Usuario.query.filter_by(usuario=session['usuario']).first()
    return usuario.id if usuario else None
