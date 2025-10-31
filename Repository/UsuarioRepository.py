from django.db import connection

def verificarIdUsuario(idUsuario):
    sql = """
        SELECT idUsuario
        FROM usuarios
        WHERE idUsuario = %s
        """
    valores = (idUsuario,)
    with connection.cursor() as cur:
        cur.execute(sql, valores)
        filas = cur.fetchall()

    if not filas:
        return False
    return True