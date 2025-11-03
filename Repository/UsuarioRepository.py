from django.db import connection

def verificarIdUsuario(idUsuario):
    sql = """
        SELECT idusuario
        FROM usuarios
        WHERE idusuario = %s
        """
    valores = (idUsuario,)
    with connection.cursor() as cur:
        cur.execute(sql, valores)
        filas = cur.fetchall()

    if not filas:
        return False
    return True