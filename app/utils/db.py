import os
import sqlite3
import bcrypt

DB_NAME = os.path.join(os.path.dirname(__file__), '..', 'tmp', 'salud_adulto.db')
os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)

def crear_base_datos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        contrasena BLOB NOT NULL,
        rol TEXT NOT NULL
    )''')
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        admin_pass = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt())
        user_pass = bcrypt.hashpw("abcd".encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol) VALUES (?, ?, ?)", ("ADMIN", admin_pass, "admin"))
        cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol) VALUES (?, ?, ?)", ("JUAN", user_pass, "usuario"))
        conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro_adultos_mayores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidad_salud TEXT,
            entidad_federativa TEXT,
            clues TEXT,
            localidad TEXT,
            servicio TEXT,
            personal_enfermeria TEXT,
            fecha TEXT,
            hora_inicio TEXT,
            hora_termino TEXT,
            nombre_jefe_fam TEXT,
            paciente TEXT,
            fecha_nacimiento TEXT,
            domicilio TEXT,           
            edad INTEGER,
            sexo TEXT,
            indigena TEXT,
            migrante TEXT,
            nivel_atencion TEXT,
            consulta_enfermeria TEXT,
            consultoria_otorgada TEXT,
            prescripcion_medicamentos TEXT,
            DG_plan_cuidados TEXT,
            DG_GRUPOS_EDAD TEXT,
            INSTITUCION_PROCEDENCIA TEXT,
            CONSEJERIA_PF TEXT,
            PF_GRUPOS_EDAD TEXT,
            PF_SUBSECUENTE TEXT,
            PF_METODO TEXT,
            VI_EMB_grupo_edad TEXT,
            VI_EMB_TRIMESTRE_GESTACIONAL TEXT,
            VI_EMB_ACCIONES_IRREDUCTIBLES TEXT,
            observaciones TEXT,
            DETECCION_TAMIZ TEXT,
            diagnostico_nutricional TEXT,
            SALUD_GINECO_DETECCION TEXT,
            EDA_SOBRES_DE_HIDRATACION_ORAL_ENTREGADOS TEXT,
            EDA_MADRES_CAPACITADAS_MANEJO TEXT,
            IRA_MADRES_CAPACITADAS_MANEJO TEXT,
            grupo_riesgo TEXT,
            DETECCION_ENFERMEDADES_CRONICAS TEXT,
            DIABETES_MELLITUS TEXT,
            DISLIPIDEMIA TEXT,
            hipertension TEXT,
            REVISION_INTEGRAL_PIEL_MIEMBROS_INFERIORES TEXT,
            DIABETICOS_INFORMADOS_CUIDADOS_PIES TEXT,
            vacunacion TEXT,
            PROMOCION_SALUD TEXT,
            DERIVACION TEXT,
            ACTIVIDADES_ASISTENCIALES TEXT,
            OBSERVACIONES_GENERALES TEXT
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            nombre_formato TEXT NOT NULL,
            area TEXT NOT NULL,
            fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
