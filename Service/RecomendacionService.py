import requests
from Model import globals

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

    if globals.estadisticas_ejercicios_json.__sizeof__() != 0:
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
    Quiero que actúes como un **entrenador personal experto**.

    Da una **recomendación de entrenamiento breve, natural y motivadora**, 
    sin mencionar análisis, información previa ni calentamientos.

    🚫 **Prohibido** usar frases como:
    - "Basado en la información..."
    - "Según los datos..."
    - "Con base en la información que me has proporcionado..."
    - "¿Trabajamos juntos...?"
    - "Podemos trabajar juntos..."
    - "Te ayudaré personalmente..."
    - "Sigamos entrenando juntos..."
    - "Te acompañaré en el proceso..."

    La recomendación debe centrarse **únicamente en el consejo práctico y profesional**, 
    como si estuvieras hablando directamente con el deportista.

    Debe basarse en:
    - El tipo de rango
    - El peso actual
    - Las repeticiones correctas e incorrectas

    Tono: profesional, empático y motivador.
    
    📏 **Extensión esperada**: La respuesta debe tener maximo 256 tokens.  
    Debe ser un texto fluido, natural y sin cortarse abruptamente

    Ejemplo de tono:
    "Buen trabajo con las repeticiones. Ajusta un poco el peso para mantener una ejecución perfecta y evitar fatiga. Enfócate en mantener un rango de movimiento constante."
    """
    print(prompt)

    mensaje = [{"role": "user", "content": prompt}]
    payload = {
        "model": "Goosedev/luna",
        "messages": mensaje,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 256  # límite de tokens reducido
        }
    }

    resp = requests.post(f"http://10.101.137.253:11434/api/chat", json=payload)
    print(resp.json()['message']['content'])
    return resp.json()['message']['content']