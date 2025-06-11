
from flask import Blueprint, redirect, render_template, session, url_for, flash

bp = Blueprint('tutorial', __name__)

@bp.route('/tutorial')
def tutorial():
    if 'usuario' not in session:
        flash('Inicia sesión para acceder al tutorial.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('tutorial.html')
