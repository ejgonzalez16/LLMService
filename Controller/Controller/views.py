import pdb
from tokenize import String

from django.shortcuts import render
from django.http import JsonResponse

from Model.PreferenciasDTO import PreferenciasDTO
from Service.PromptService import obtenerRespuestaPrompt
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from Service import PreferenciasService as preferenciasService

# Create your views here.

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prompt(request):
    mensaje = request.GET.get("mensaje")
    if mensaje:
        respuesta = obtenerRespuestaPrompt(mensaje)
        return JsonResponse(respuesta, safe=False, status=200)
    else:
        return JsonResponse({"error": "Debe enviar un parámetro 'mensaje'"}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def insertarPreferencias(request):
    pdb.set_trace()
    idUsuario = request.data.get("idUsuario")
    preferencias = request.data.get("prescripciones")
    if idUsuario and preferencias:
        preferenciasDTO = PreferenciasDTO(idUsuario, preferencias)
        data = preferenciasService.insertarPreferencias(preferenciasDTO.idUsuario, preferenciasDTO.preferencias)
        if data == "Controller":
            return JsonResponse("No se pudo hacer la consulta al LLM correctamente", safe=False, status=500)
        if data == "":
            return JsonResponse("internal server error", safe=False, status=500)
        return JsonResponse(data, safe=False, status=200)

    else:
        return JsonResponse({"error": "Debe enviar dos parámetros 'idUsuario' y 'prescripciones'"}, status=400)