from Model.PreferenciasUsuario import PreferenciasUsuario
from Repository import PreferenciasUsuarioRepository as preferenciasUsuarioRepository
import requests
import json
from Model import globals
from datetime import datetime

def insertarPreferencias(idUsuario, prescripciones):
    prompt = (
         f"A partir del estado físico: '{prescripciones}', "
         f"asigna un 'idTipoRango' de {globals.tiposRango_json} "
         f"a TODOS los {globals.ejercicios_json.__sizeof__()} ejercicios en {globals.ejercicios_json}. "
         f"Ten en cuenta lo siguiente: "
         f"- Mientras más grande sea el valor de 'idTipoRango', más difícil o exigente es el ejercicio. "
         f"- Si el estado físico indica dolor o problema en alguna articulación o musculo involucrada en un ejercicio, "
         f"debes asignarle un 'idTipoRango' más bajo (más fácil/seguro). "
         f"Responde SOLO con un JSON válido, sin etiquetas, sin comentarios y sin explicaciones. "
         f"Formato esperado: "
         f"[{{\"idTipoRango\": <int>, \"idEjercicio\": <int>}}, ...] "
         f"Asegúrate de incluir TODOS los ejercicios."
     )
    print(prompt)

    mensaje = [{"role": "user", "content": prompt}]
    payload = {
        "model": "Goosedev/luna",
        "messages": mensaje,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 512  # suficiente para toda la lista JSON
        }
    }

    resp = requests.post(f"http://ollama:11434/api/chat", json=payload)
    print(resp.json()['message']['content'])

    try:
        data = json.loads(resp.json()['message']['content'])
    except (TypeError, ValueError) as e:
        return "LLM"

    preferencias_list = [
        PreferenciasUsuario(
            idUsuario=idUsuario,
            idTipoRango=item["idTipoRango"],
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # fecha de hoy en formato YYYY-MM-DD
            esActiva=1,
            idEjercicio=item["idEjercicio"]
        )
        for item in data
    ]

    resultado = preferenciasUsuarioRepository.insertarPreferencias(preferencias_list)
    if resultado:
        return data
    return ""
