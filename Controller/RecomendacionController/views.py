from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
import Service.RecomendacionService as recomendacionService

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtenerRecomendacion(request, idUsuario: str):
    if idUsuario:
        if(recomendacionService.verificarUsuario(idUsuario) == False):
            return JsonResponse({"error": "Ese idUsuario no existe"}, safe=False, status=400)
        data = recomendacionService.obtenerRecomendacion(idUsuario)
        if data == "PreferenciasController":
            return JsonResponse("No se pudo hacer la consulta al LLM correctamente", safe=False, status=500)
        if data == "":
            return JsonResponse("internal server error", safe=False, status=500)
        return JsonResponse(data, safe=False, status=200)
    else:
        return JsonResponse({"error": "Debe enviar el parámetro 'idUsuario'"}, status=400)