from django.db import connection

def verificarIdUsuario(idUsuario):
    sql = """
        SELECT id
        FROM usuarios
        WHERE id = %s
        """
    valores = (idUsuario,)
    with connection.cursor() as cur:
        cur.execute(sql, valores)
        filas = cur.fetchall()

    if not filas:
        return False
    return True