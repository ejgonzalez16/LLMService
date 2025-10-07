from django.db import connection
from Model.EstadisticasArticulacionUsuario import EstadisticasArticulacionUsuario


def getEstadisticasArticulacion(idUsuario):
    sql = """
                    SELECT es.repeticionescorrectas, es.idarticulacion, es.idestadisticaejercicio
                    FROM estadisticasejerciciousuario e 
                    JOIN preferenciasusuario p on p.id = e.idpreferenciausuario
                    JOIN estadisticasarticulacionusuario es on e.id = es.idestadisticaejercicio
                    WHERE p.idUsuario = %s AND e.fecha >= CURRENT_DATE - INTERVAL 7 DAY
                    """
    valores = (idUsuario,)
    with connection.cursor() as cur:
        cur.execute(sql, valores)
        filas = cur.fetchall()

    if not filas:
        return ""

    estadisticasArticulacion = [EstadisticasArticulacionUsuario(repeticionesCorrectas=f[0], idArticulacion=f[1], idEstadisticaEjercicio=f[2]) for f in filas]
    return estadisticasArticulacion