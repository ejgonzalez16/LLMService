from django.db import connection

from Model.PreferenciasUsuario import PreferenciasUsuario

def getPreferencias(idUsuario):
    sql = """
            SELECT *
            FROM preferenciasusuario
            WHERE idUsuario = %s AND esActiva = 1
            """
    valores = (idUsuario,)
    with connection.cursor() as cur:
        cur.execute(sql, valores)
        filas = cur.fetchall()

    if not filas:
        return ""

    preferencias = [PreferenciasUsuario(idTipoRango=f[2], idEjercicio=f[5]) for f in filas]
    return preferencias


def insertarPreferencias(preferencias_list):
    if not preferencias_list:
        print("La lista está vacía, no se puede insertar.")
        return False
    idUsuario = preferencias_list[0].idUsuario
    desactivarPreferencias(idUsuario)
    valores = [
        (p.idUsuario, p.idTipoRango, p.fecha, p.esActiva, p.idEjercicio)
        for p in preferencias_list
    ]
    sql = """
    INSERT INTO preferenciasusuario
    (idUsuario, idTipoRango, fecha, esActiva, idEjercicio)
    VALUES (%s, %s, %s, %s, %s)
    """

    with connection.cursor() as cur:
        cur.executemany(sql, valores)
        print(f"{cur.rowcount} registros insertados")
        if(cur.rowcount > 0):
            return True
        return False


def desactivarPreferencias(idUsuario):
    sql = """
    UPDATE preferenciasusuario
    SET esActiva = 0
    WHERE idUsuario = %s and esActiva = 1
    """
    with connection.cursor() as cur:
        cur.execute(sql, (idUsuario,))
        print(f"{cur.rowcount} registros actualizados a esActiva=0 para idUsuario={idUsuario}")
