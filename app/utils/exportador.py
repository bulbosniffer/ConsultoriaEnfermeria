import pandas as pd
import io
from datetime import datetime
from app.models import RegistroAdultoMayor  # Importa tu modelo SQLAlchemy
from app.utils.db import db  # Instancia SQLAlchemy

def generar_excel(fecha_inicio_str, fecha_fin_str):
    try:
        # Validar fechas
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")

        # Consulta con SQLAlchemy todos los registros
        registros = RegistroAdultoMayor.query.all()

        # Convertir registros SQLAlchemy a lista de diccionarios
        lista_dicts = [r.to_dict() for r in registros]  # Necesitas definir to_dict() en tu modelo

        # Crear DataFrame
        df = pd.DataFrame(lista_dicts)

        # Asegurarse que la columna 'fecha' sea datetime
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df = df.dropna(subset=['fecha'])

        # Filtrar por fecha
        df = df[(df['fecha'] >= fecha_inicio) & (df['fecha'] <= fecha_fin)]

        if df.empty:
            return None, "No hay registros en ese rango de fechas."

        # Agregar columnas día, mes, año
        fecha_index = df.columns.get_loc('fecha')
        df.insert(fecha_index, 'día', df['fecha'].dt.day)
        df.insert(fecha_index + 1, 'mes', df['fecha'].dt.month)
        df.insert(fecha_index + 2, 'año', df['fecha'].dt.year)

        # Concatenar información clave
        df['jefe_de_familia'] = (
            "Jf: " + df['nombre_jefe_fam'].fillna('') + " | " +
            "Pte: " + df['paciente'].fillna('') + " | " +
            "Fn: " + df['fecha_nacimiento'].fillna('') + " | " +
            "Dom: " + df['domicilio'].fillna('')
        )

        jefe_index = df.columns.get_loc('nombre_jefe_fam')
        df.insert(jefe_index,
            'NOMBRE DEL JEFE DE FAM, NOMBRE DEL PACIENTE , FECHA DE NACIMIENTO Y DOMICILIO',
            df['jefe_de_familia'])

        # Eliminar columnas innecesarias
        df.drop(columns=[
            'id', 'nombre_jefe_fam', 'paciente',
            'fecha_nacimiento', 'domicilio', 'fecha', 'jefe_de_familia'
        ], inplace=True)

        # Exportar a Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Registros', index=False)
        output.seek(0)

        nombre_archivo = f"registros_{fecha_inicio_str}_a_{fecha_fin_str}.xlsx"
        return output, nombre_archivo

    except Exception as e:
        return None, f"Error al generar el archivo: {str(e)}"
