from flask import Blueprint, render_template, session, redirect, url_for, flash, request
import sqlite3
from app.utils.db import DB_NAME
import bcrypt

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

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        nuevo_rol = request.form['rol']
        nueva_contra = request.form.get('contrasena')
        if nueva_contra:
            hashed = bcrypt.hashpw(nueva_contra.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("UPDATE usuarios SET rol = ?, contrasena = ? WHERE id = ?", (nuevo_rol, hashed, usuario_id))
        else:
            cursor.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (nuevo_rol, usuario_id))
        conn.commit()
        conn.close()
        flash('Usuario actualizado.', 'success')
        return redirect(url_for('admin.lista_usuarios'))

    usuario = cursor.execute("SELECT id, usuario, rol FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    conn.close()
    if not usuario:
        flash('Usuario no encontrado.', 'warning')
        return redirect(url_for('admin.lista_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@bp.route('/admin/eliminar_usuario/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (session['usuario'],))
    usuario_actual = cursor.fetchone()

    if usuario_actual and usuario_id == usuario_actual[0]:
        conn.close()
        flash('No puedes eliminar tu propio usuario.', 'warning')
        return redirect(url_for('admin.lista_usuarios'))

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()
    conn.close()

    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('admin.lista_usuarios'))


@bp.route('/admin/usuarios')
def lista_usuarios():
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))

    conn = sqlite3.connect(DB_NAME)
    usuarios = conn.execute("SELECT id, usuario, rol FROM usuarios ORDER BY id").fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios)

def obtener_id_usuario_actual():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (session['usuario'],))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None
