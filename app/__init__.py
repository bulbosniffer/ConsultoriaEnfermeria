from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'clave_secreta_segura'
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from .utils.db import crear_base_datos
    crear_base_datos()

    from .routes import auth, admin, formulario, formatos
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(formulario.bp)
    app.register_blueprint(formatos.bp)

    return app