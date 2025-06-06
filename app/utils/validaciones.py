from datetime import datetime

def campos_validos(form):
    campos_obligatorios = ['unidad_salud', 'fecha', 'hora_inicio', 'hora_termino', 'edad']

    for campo in campos_obligatorios:
        valor = form.get(campo, '').strip()
        if valor == '':
            return False, campo

    try:
        edad = int(form.get('edad', '').strip())
        if edad <= 0:
            return False, 'edad (valor no válido)'
    except ValueError:
        return False, 'edad (no numérico)'

    try:
        fecha = datetime.strptime(form.get('fecha', '').strip(), '%Y-%m-%d')
        if fecha > datetime.now():
            return False, 'fecha (futura)'
    except ValueError:
        return False, 'fecha (formato inválido)'

    try:
        inicio = datetime.strptime(form.get('hora_inicio', ''), '%H:%M')
        fin = datetime.strptime(form.get('hora_termino', ''), '%H:%M')
        if inicio >= fin:
            return False, 'hora_inicio (debe ser anterior a hora_termino)'
    except ValueError:
        return False, 'hora_inicio o hora_termino (formato inválido)'

    return True, None

