from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3, bcrypt
from app.utils.db import DB_NAME

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET'])
def home():
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT contrasena, rol FROM usuarios WHERE usuario = ?", (usuario.upper(),))
        registro = cursor.fetchone()
        conn.close()

        if registro and bcrypt.checkpw(contrasena.encode('utf-8'), registro[0]):
            session['usuario'] = usuario.upper()
            session['rol'] = registro[1]
            flash('Inicio de sesión exitoso', 'info')

            return redirect(url_for('admin.panel') if registro[1] == 'admin' else url_for('formulario.formulario'))
        else:
            flash('Credenciales incorrectas', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if 'usuario' not in session or session['rol'] != 'admin':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        usuario = request.form['usuario'].upper()
        contrasena = request.form['contrasena']
        rol = request.form['rol']
        hashed = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            conn.close()
            flash('El usuario ya existe.', 'warning')
            return redirect(url_for('auth.registrar_usuario'))

        cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol) VALUES (?, ?, ?)", (usuario, hashed, rol))
        conn.commit()
        conn.close()

        flash('Usuario registrado correctamente', 'success')
        return redirect(url_for('admin.panel'))

    return render_template('registrar_usuario.html')