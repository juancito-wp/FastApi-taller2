import requests
from django.shortcuts import render

API_URL = "http://127.0.0.1:8000"

def catalogo(request):
    productos = []
    error = None
    try:
        response = requests.get(f"{API_URL}/productos/")
        if response.status_code == 200:
            productos = response.json()
        else:
            error = f"Error al cargar productos (Código {response.status_code})"
    except Exception:
        error = "No se pudo conectar con la API de FastAPI. Asegúrate de que esté corriendo."

    return render(request, "catalogo.html", {"productos": productos, "error": error})