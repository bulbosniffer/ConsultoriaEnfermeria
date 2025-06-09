from flask import Blueprint, render_template, request, redirect, session, flash, url_for, send_file
from app.utils.validaciones import campos_validos
from app.models import RegistroAdultoMayor
from app.utils.db import db
from ..utils.exportador import generar_excel
from datetime import datetime, date

bp = Blueprint('formulario', __name__)

def get_str(form, key):
    return form.get(key, '').strip()

def get_int(form, key):
    try:
        return int(form.get(key, 0))
    except:
        return 0

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

        try:
            fecha_obj = datetime.strptime(get_str(request.form, 'fecha'), '%Y-%m-%d').date()

            nuevo_registro = RegistroAdultoMayor(
                unidad_salud = get_str(request.form, 'unidad_salud'),
                entidad_federativa = get_str(request.form, 'entidad_federativa'),
                clues = get_str(request.form, 'clues'),
                localidad = get_str(request.form, 'localidad'),
                servicio = get_str(request.form, 'servicio'),
                personal_enfermeria = get_str(request.form, 'personal_enfermeria'),
                fecha = fecha_obj,
                hora_inicio = get_str(request.form, 'hora_inicio'),
                hora_termino = get_str(request.form, 'hora_termino'),
                nombre_jefe_fam = get_str(request.form, 'nombre_jefe_fam'),
                paciente = get_str(request.form, 'paciente'),
                fecha_nacimiento = get_str(request.form, 'fecha_nacimiento'),
                domicilio = get_str(request.form, 'domicilio'),
                edad = get_int(request.form, 'edad'),
                sexo = get_str(request.form, 'sexo'),
                indigena = get_str(request.form, 'indigena'),
                migrante = get_str(request.form, 'migrante'),
                nivel_atencion = get_str(request.form, 'nivel_atencion'),
                consulta_enfermeria = get_str(request.form, 'consulta_enfermeria'),
                consultoria_otorgada = get_str(request.form, 'consultoria_otorgada'),
                prescripcion_medicamentos = get_str(request.form, 'prescripcion_medicamentos'),
                DG_plan_cuidados = get_str(request.form, 'DG_plan_cuidados'),
                DG_GRUPOS_EDAD = get_str(request.form, 'DG_GRUPOS_EDAD'),
                INSTITUCION_PROCEDENCIA = get_str(request.form, 'INSTITUCION_PROCEDENCIA'),
                CONSEJERIA_PF = get_str(request.form, 'CONSEJERIA_PF'),
                PF_GRUPOS_EDAD = get_str(request.form, 'PF_GRUPOS_EDAD'),
                PF_SUBSECUENTE = get_str(request.form, 'PF_SUBSECUENTE'),
                PF_METODO = get_str(request.form, 'PF_METODO'),
                VI_EMB_grupo_edad = get_str(request.form, 'VI_EMB_grupo_edad'),
                VI_EMB_TRIMESTRE_GESTACIONAL = get_str(request.form, 'VI_EMB_TRIMESTRE_GESTACIONAL'),
                VI_EMB_ACCIONES_IRREDUCTIBLES = get_str(request.form, 'VI_EMB_ACCIONES_IRREDUCTIBLES'),
                observaciones = get_str(request.form, 'observaciones'),
                DETECCION_TAMIZ = get_str(request.form, 'DETECCION_TAMIZ'),
                diagnostico_nutricional = get_str(request.form, 'diagnostico_nutricional'),
                SALUD_GINECO_DETECCION = get_str(request.form, 'SALUD_GINECO_DETECCION'),
                EDA_SOBRES_DE_HIDRATACION_ORAL_ENTREGADOS = get_str(request.form, 'EDA_SOBRES_DE_HIDRATACION_ORAL_ENTREGADOS'),
                EDA_MADRES_CAPACITADAS_MANEJO = get_str(request.form, 'EDA_MADRES_CAPACITADAS_MANEJO'),
                IRA_MADRES_CAPACITADAS_MANEJO = get_str(request.form, 'IRA_MADRES_CAPACITADAS_MANEJO'),
                grupo_riesgo = get_str(request.form, 'grupo_riesgo'),
                DETECCION_ENFERMEDADES_CRONICAS = get_str(request.form, 'DETECCION_ENFERMEDADES_CRONICAS'),
                DIABETES_MELLITUS = get_str(request.form, 'DIABETES_MELLITUS'),
                DISLIPIDEMIA = get_str(request.form, 'DISLIPIDEMIA'),
                hipertension = get_str(request.form, 'hipertension'),
                REVISION_INTEGRAL_PIEL_MIEMBROS_INFERIORES = get_str(request.form, 'REVISION_INTEGRAL_PIEL_MIEMBROS_INFERIORES'),
                DIABETICOS_INFORMADOS_CUIDADOS_PIES = get_str(request.form, 'DIABETICOS_INFORMADOS_CUIDADOS_PIES'),
                vacunacion = get_str(request.form, 'vacunacion'),
                PROMOCION_SALUD = get_str(request.form, 'PROMOCION_SALUD'),
                DERIVACION = get_str(request.form, 'DERIVACION'),
                ACTIVIDADES_ASISTENCIALES = get_str(request.form, 'ACTIVIDADES_ASISTENCIALES'),
                OBSERVACIONES_GENERALES = get_str(request.form, 'OBSERVACIONES_GENERALES'),
            )

            db.session.add(nuevo_registro)
            db.session.commit()
            flash('Registro guardado exitosamente.', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar: {e}', 'danger')

        return redirect(url_for('formulario.formulario'))

    # GET: mostrar registros del día y usuario
    usua = session['usuario']
    hoy = date.today()

    registros = RegistroAdultoMayor.query.filter_by(personal_enfermeria=usua, fecha=hoy).all()

    return render_template('formulario.html', registros=registros)

@bp.route('/exportar', methods=['GET'])
def exportar():
    if 'usuario' not in session:
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('auth.login'))

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    if not fecha_inicio or not fecha_fin:
        flash("Debes seleccionar un rango de fechas.", "warning")
        return redirect(url_for('formulario.formulario'))

    try:
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
    except Exception as e:
        flash(f'Error al exportar: {e}', 'danger')
        return redirect(url_for('formulario.formulario'))