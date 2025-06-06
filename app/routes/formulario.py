from flask import Blueprint, render_template, request, redirect, session, flash, url_for,send_file
from app.utils.validaciones import campos_validos
from app.utils.db import DB_NAME
from ..utils.exportador import generar_excel
import sqlite3
from datetime import date

bp = Blueprint('formulario', __name__)


@bp.route('/formulario')
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
        try:
            data = (
                request.form.get('unidad_salud', ''),
                request.form.get('entidad_federativa', ''),
                request.form.get('clues', ''),
                request.form.get('localidad', ''),
                request.form.get('servicio', ''),
                request.form.get('personal_enfermeria', ''),
                request.form.get('fecha', ''),
                request.form.get('hora_inicio', ''),
                request.form.get('hora_termino', ''),
                request.form.get('nombre_jefe_fam', ''),
                request.form.get('paciente', ''),
                request.form.get('fecha_nacimiento', ''),
                request.form.get('domicilio', ''),
                int(request.form.get('edad', 0)),  # 0 por defecto; valida antes que sea > 0
                request.form.get('sexo', ''),
                request.form.get('indigena', ''),
                request.form.get('migrante', ''),
                request.form.get('nivel_atencion', ''),
                request.form.get('consulta_enfermeria', ''),
                request.form.get('consultoria_otorgada', ''),
                request.form.get('prescripcion_medicamentos', ''),
                request.form.get('DG_plan_cuidados', ''),
                request.form.get('DG_GRUPOS_EDAD', ''),
                request.form.get('INSTITUCION_PROCEDENCIA', ''),
                request.form.get('CONSEJERIA_PF', ''),
                request.form.get('PF_GRUPOS_EDAD', ''),
                request.form.get('PF_SUBSECUENTE', ''),
                request.form.get('PF_METODO', ''),
                request.form.get('VI_EMB_grupo_edad', ''),
                request.form.get('VI_EMB_TRIMESTRE_GESTACIONAL', ''),
                request.form.get('VI_EMB_ACCIONES_IRREDUCTIBLES', ''),
                request.form.get('observaciones',''),
                request.form.get('DETECCION_TAMIZ', ''),
                request.form.get('diagnostico_nutricional', ''),
                request.form.get('SALUD_GINECO_DETECCION', ''),
                request.form.get('EDA_SOBRES_DE_HIDRATACION_ORAL_ENTREGADOS', ''),
                request.form.get('EDA_MADRES_CAPACITADAS_MANEJO', ''),
                request.form.get('IRA_MADRES_CAPACITADAS_MANEJO', ''),
                request.form.get('grupo_riesgo', ''),
                request.form.get('DETECCION_ENFERMEDADES_CRONICAS', ''),
                request.form.get('DIABETES_MELLITUS', ''),
                request.form.get('DISLIPIDEMIA', ''),
                request.form.get('hipertension', ''),
                request.form.get('REVISION_INTEGRAL_PIEL_MIEMBROS_INFERIORES', ''),
                request.form.get('DIABETICOS_INFORMADOS_CUIDADOS_PIES', ''),
                request.form.get('vacunacion', ''),
                request.form.get('PROMOCION_SALUD', ''),
                request.form.get('DERIVACION', ''),
                request.form.get('ACTIVIDADES_ASISTENCIALES', ''),
                request.form.get('OBSERVACIONES_GENERALES', '')
            )

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''INSERT INTO registro_adultos_mayores (
                unidad_salud,
                entidad_federativa,
                clues,
                localidad,
                servicio,
                personal_enfermeria, 
                fecha,
                hora_inicio, 
                hora_termino,
                nombre_jefe_fam, 
                paciente,
                fecha_nacimiento, 
                domicilio,    
                edad,
                sexo,
                indigena,
                migrante,
                nivel_atencion,
                consulta_enfermeria,
                consultoria_otorgada,
                prescripcion_medicamentos, 
                DG_plan_cuidados, 
                DG_GRUPOS_EDAD,
                INSTITUCION_PROCEDENCIA,           
                CONSEJERIA_PF,
                PF_GRUPOS_EDAD,           
                PF_SUBSECUENTE,          
                PF_METODO,
                VI_EMB_grupo_edad,
                VI_EMB_TRIMESTRE_GESTACIONAL,
                VI_EMB_ACCIONES_IRREDUCTIBLES,
                observaciones,           
                DETECCION_TAMIZ,          
                diagnostico_nutricional,           
                SALUD_GINECO_DETECCION, 
                EDA_SOBRES_DE_HIDRATACION_ORAL_ENTREGADOS,
                EDA_MADRES_CAPACITADAS_MANEJO,
                IRA_MADRES_CAPACITADAS_MANEJO,
                grupo_riesgo,               
                DETECCION_ENFERMEDADES_CRONICAS,           
                DIABETES_MELLITUS,           
                DISLIPIDEMIA,            
                hipertension,       
                REVISION_INTEGRAL_PIEL_MIEMBROS_INFERIORES,
                DIABETICOS_INFORMADOS_CUIDADOS_PIES,
                vacunacion,           
                PROMOCION_SALUD,
                DERIVACION,           
                ACTIVIDADES_ASISTENCIALES,
                OBSERVACIONES_GENERALES
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
            print(len(data))                
            conn.commit()
            conn.close()
            flash('Registro guardado exitosamente.', 'success')
        except Exception as e:
            flash(f'Error al guardar: {e}', 'danger')
        return redirect(url_for('formulario.formulario'))
        #return redirect('/')
    usua = session['usuario']
    hoy = date.today().isoformat()  # formato YYYY-MM-DD
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT * FROM registro_adultos_mayores
        WHERE personal_enfermeria = ? AND fecha = ?
    """, (usua, hoy))
    registros = c.fetchall()
    conn.close()

    return render_template('formulario.html', registros=registros)
        
@bp.route('/exportar', methods=['GET'])
def exportar():
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            flash("Debes seleccionar un rango de fechas.", "warning")
            return redirect(url_for('formulario.formulario'))  # ajusta según tu formulario

        excel_output, mensaje = generar_excel(fecha_inicio, fecha_fin)

        if not excel_output:
            flash(mensaje, "danger")
            return redirect(url_for('formulario.formulario'))

        return send_file(
            excel_output,
            download_name=mensaje,
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    
   