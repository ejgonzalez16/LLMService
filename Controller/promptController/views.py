from tokenize import String

from django.shortcuts import render
from django.http import JsonResponse

from Service.PromptService import obtenerRespuestaPrompt


# Create your views here.

def prompt(request):
    if request.method == "GET":
        mensaje = request.GET.get("mensaje")
        if mensaje:
            respuesta = obtenerRespuestaPrompt(mensaje)
            return JsonResponse(respuesta, safe=False, status=200)
        else:
            return JsonResponse({"error": "Debe enviar un parámetro 'mensaje'"}, status=400)
    return JsonResponse({"mensaje": "Use un método para un resultado"}, status=400)