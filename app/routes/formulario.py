from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from app.utils.validaciones import campos_validos
from app.utils.db import DB_NAME
import sqlite3
from datetime import date

bp = Blueprint('formulario', __name__)

@bp.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if 'usuario' not in session:
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('auth.login'))

    if session['rol'] == 'admin':
        return redirect(url_for('admin.panel'))

    if request.method == 'POST':
        validado, campo = campos_validos(request.form)
        if not validado:
            flash(f"Completa el campo: {campo}", 'danger')
            return redirect(url_for('formulario.formulario'))

        # Lógica de guardado omitida por brevedad (igual a la que ya tienes)
        flash("Formulario guardado", 'success')
        return redirect(url_for('formulario.formulario'))

    conn = sqlite3.connect(DB_NAME)
    hoy = date.today().isoformat()
    registros = conn.execute("SELECT * FROM registro_adultos_mayores WHERE personal_enfermeria = ? AND fecha = ?", (session['usuario'], hoy)).fetchall()
    conn.close()
    return render_template('formulario.html', registros=registros)