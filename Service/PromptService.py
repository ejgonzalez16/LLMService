import Model.globals as globals
import requests


def obtenerRespuestaPrompt(request):
    resp = globals.deepseek.chat.completions.create(
     model="deepseek/deepseek-r1:free",
     messages=[{"role": "user", "content": request}]
    )
    #messages = [{"role": "user", "content": request}]
    #payload = {"model": "gpt-oss:20b", "messages": messages, "stream": False}
    #resp = requests.post(f"http://localhost:11434/api/chat", json=payload)
    #data = resp.json()
    #return data["message"]["content"]
    return resp.choices[0].message.content