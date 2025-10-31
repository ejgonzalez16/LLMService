import ast
import requests
from Repository import UsuarioRepository as usuarioRepository
from Model import globals
import json

def verificarUsuario(idUsuario):
    resultado = usuarioRepository.verificarIdUsuario(idUsuario)
    return resultado

def obtenerRecomendacion(idUsuario):
    globals.obtenerPreferenciasUsuario(idUsuario)
    prompt = f"""
    Tengo una base de datos con información de ejercicios y desempeño físico del usuario.

    A continuación te presento los datos relevantes en formato JSON:

    - **Ejercicios disponibles**:
    {globals.ejercicios_json}

    - **Tipos de rango de movimiento**:
    {globals.tiposRango_json}

    - **Articulaciones evaluadas**:
    {globals.articulaciones_json}

    - **Preferencias del usuario en tipos de rango para cada ejercicio**:
    {globals.preferencias_json}
    """

    if globals.estadisticas_ejercicios_json != '[]':
        prompt += f"""
        En la última semana, el usuario **ha realizado los siguientes ejercicios**:
        {globals.estadisticas_ejercicios_json}

        Y el rendimiento de sus articulaciones fue el siguiente:
        {globals.estadisticas_articulaciones_json}
        """
    else:
        prompt += """
        En la última semana, el usuario **no ha realizado ningún ejercicio**.
        """

    prompt += """
    Genera una respuesta en formato JSON **válido** (sin texto adicional antes ni después).

    El JSON debe tener exactamente esta estructura:
    {
      "recomendacionGeneral": "texto explicativo de alrededor de 50 tokens, minimo 35 tokens, con saltos de línea escapados (usa \\n, no los pongas directos)",
      "ejercicioRecomendado": {
        "explicación": "explicación clara y breve (máximo 3 líneas) sobre por qué se recomienda ese ejercicio, también con \\n escapados",
        "nombre": "nombre exacto del ejercicio, debe coincidir exactamente con uno del catálogo de ejercicios proporcionado",
        "idEjercicio": número entero que corresponda al id exacto del ejercicio en el catálogo
      }
    }

    ⚠️ Instrucciones obligatorias:
    - Usa **solo** comillas dobles (`"`).
    - Escapa correctamente los saltos de línea como `\\n`.
    - **No incluyas texto fuera del JSON** (ni comentarios, ni texto adicional).
    - **No uses comillas simples** en ningún lugar.
    - El JSON debe ser **100 % válido y cargable con `json.loads()`** sin errores.
    - El ejercicio recomendado **debe existir en el catálogo oficial de ejercicios**.
    - La recomendación **debe basarse exclusivamente en el desempeño del usuario en la última semana**, tomando en cuenta:
      - Su frecuencia y tipo de ejercicios realizados.
      - Su rendimiento por articulación.
      - Sus preferencias en tipos de rango de movimiento.
      - Recomendar al usuario centrarse más en la técnica de los ejercicios que el peso que levanta, enfocandose en maxmizar el porcentaje repeticiones correctas.
      - Peso levantado.
      - Las áreas que requieren mejora o refuerzo.

    🧠 Detalles de redacción:
    - **Háblale directamente al usuario en segunda persona** como si fueras su entrenador personal.
    - Usa un tono **cercano, motivador y profesional**.
    - Divide las ideas con saltos de línea (`\\n\\n`) para separar logros, técnica, control de articulaciones, errores y motivación.
    - Evita frases impersonales como “el usuario ha hecho” o “se recomienda”. En su lugar, di “has hecho”, “deberías”, “te recomiendo”, “mantén”.
    - No menciones que el texto está en formato JSON ni hagas referencias al formato en la respuesta.

    📏 Restricciones:
    - La “recomendacionGeneral” NO PUEDE SUPERAR LOS **50 tokens**.
    - En "recomendaciónGeneral" **no** menciones el mismo ejercicio que aparece en "ejercicioRecomendado".
    - “ejercicioRecomendado” debe complementar la recomendación con una explicación breve y clara (máximo 3 líneas).

    📦 Entrega únicamente el JSON final, sin ```json ni ``` al inicio o al final.
    """
    print(prompt)

    response = globals.client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct:fireworks-ai",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=300,
        temperature=0.3
    )

    #mensaje = [{"role": "user", "content": prompt}]
    #payload = {
    #    "model": "Goosedev/luna",
    #    "messages": mensaje,
    #    "stream": False,
    #    "options": {
    #        "temperature": 0.3,
    #        "num_predict": 700  # límite de tokens reducido
    #    }
    #}

    #resp = requests.post(f"http://{globals.ip}:11434/api/chat", json=payload)

    #print(response.json()['message']['content'])
    print(response.choices[0].message.content)
    try:
        #data = json.loads(response.json()['message']['content'])
        data = json.loads(response.choices[0].message.content)
    except (TypeError, ValueError) as e:
        return "PreferenciasController"

    return data