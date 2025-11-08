import json
import sys
from Repository import TiposRangoRepository as tiposRangoRepository
from openai import OpenAI
from Repository import EjerciciosRepository as ejerciciosRepository
from Repository import ArticulacionesRepository as articulacionesRepository
from Repository import PreferenciasUsuarioRepository as preferenciasRepository
from huggingface_hub import InferenceClient
from Repository import EstadisticasEjercicioUsuarioRepository as estadisticasEjercicioUsuarioRepository
from Repository import EstadisticasArticulacionUsuarioRepository as estadisticasArticulacionUsuarioRepository
from Repository import UsuarioRepository as usuarioRepository

HF_TOKEN = "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"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

modelo = "gpt-5-mini"
tiposRango_json = []
ejercicios_json = []
messages = []
preferencias_json = []
articulaciones_json = []
estadisticas_ejercicios_json = []
estadisticas_articulaciones_json = []
prescripciones  = ""
ip = "10.101.139.210"

def obtenerEjerciciosYRangos():
    global tiposRango_json
    global ejercicios_json
    tiposRango = tiposRangoRepository.getTiposRango()
    print(tiposRango)
    if not tiposRango:
        print("Error crítico: No se pudieron cargar los tipos de rango.")
        sys.exit(1)
    ejercicios = ejerciciosRepository.getEjercicios()
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

def obtenerPreferenciasUsuario(idUsuario):
    global preferencias_json
    global articulaciones_json
    global estadisticas_articulaciones_json
    global estadisticas_ejercicios_json
    global tiposRango_json
    global ejercicios_json
    global prescripciones
    tiposRango = tiposRangoRepository.getTiposRango()
    print(tiposRango)
    if not tiposRango:
        print("Error crítico: No se pudieron cargar los tipos de rango.")
        sys.exit(1)

    ejercicios = ejerciciosRepository.getEjercicios()
    print(ejercicios)
    if (ejercicios == "" or ejercicios == []):
        print("Error crítico: No se pudieron cargar los ejercicios.")
        sys.exit(1)

    preferencias = preferenciasRepository.getPreferencias(idUsuario)

    articulaciones = articulacionesRepository.getArticulaciones()
    if not articulaciones:
        print("Error crítico: No se pudieron cargar las articulaciones.")
        sys.exit(1)

    estadisticasEjercicioUsuario = estadisticasEjercicioUsuarioRepository.getEstadisticasEjercicios(idUsuario)

    estadisticasArticulacionUsuario = estadisticasArticulacionUsuarioRepository.getEstadisticasArticulacion(idUsuario)

    prescripciones =  usuarioRepository.obtenerPrescripciones(idUsuario)

    tiposRango_json = json.dumps(
        [{"idTipoRango": t.id, "nombre": t.nombre} for t in tiposRango],
        ensure_ascii=False
    )

    ejercicios_json = json.dumps(
        [{"idEjercicio": e.id, "nombre": e.nombre} for e in ejercicios],
        ensure_ascii=False
    )

    preferencias_json = json.dumps(
        [{"idTipoRango": p.idTipoRango, "nombre": p.idEjercicio} for p in preferencias],
        ensure_ascii=False
    )

    articulaciones_json = json.dumps(
        [{"idArticulacion": a.id, "nombre": a.nombre} for a in articulaciones],
        ensure_ascii=False
    )

    estadisticas_articulaciones_json = json.dumps(
        [{"idEstadisticaEjercicio": e.idEstadisticaEjercicio, "repeticionesCorrectas": e.repeticionesCorrectas, "idArticulacion": e.idArticulacion} for e in estadisticasArticulacionUsuario],
        ensure_ascii=False
    )

    estadisticas_ejercicios_json = json.dumps(
        [{"repeticionesCorrectas": e.peso, "idArticulacion": e.repeticionesRealizadas} for e in
         estadisticasEjercicioUsuario],
        ensure_ascii=False
    )

