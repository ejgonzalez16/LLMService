tiposRango_json = []
ejercicios_json = []
messages = []
import json
import sys
import requests
from Repository import TiposRangoRepository as tiposRangoRepository
from Repository import EjerciciosRepository as ejerciciosRepository


def obtenerEjerciciosYRangos():
    global tiposRango_json
    global ejercicios_json
    tiposRango = tiposRangoRepository.getTiposRango()
    print(tiposRango)
    if not tiposRango:
        print("Error crítico: No se pudieron cargar los tipos de rango.")
        sys.exit(1)
    ejercicios = ejerciciosRepository.getTiposRango()
    print(ejercicios)
    if (ejercicios == "" or ejercicios == []):
        print("Error crítico: No se pudieron cargar los ejercicios.")
        sys.exit(1)
    tiposRango_json = json.dumps(
        [{"idTipoRango": t.id, "nombre": t.nombre} for t in tiposRango],
        ensure_ascii=False
    )
    ejercicios_json = json.dumps(
        [{"idEjercicio": e.id, "nombre": e.nombre} for e in ejercicios],
        ensure_ascii=False
    )

