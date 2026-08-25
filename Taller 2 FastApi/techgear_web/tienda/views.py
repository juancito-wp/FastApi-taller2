import requests
from django.shortcuts import render, redirect

API_URL = "http://127.0.0.1:8000"

def catalogo(request):
    productos = []
    error = request.GET.get('error')
    mensaje_exito = request.GET.get('exito')
    
    try:
        response = requests.get(f"{API_URL}/productos/")
        if response.status_code == 200:
            productos = response.json()
        else:
            error = "Error al obtener el inventario."
    except Exception:
        error = "No se pudo conectar con el microservicio de FastAPI."

    return render(request, "catalogo.html", {
        "productos": productos, 
        "error": error,
        "mensaje_exito": mensaje_exito
    })

def crear_pedido(request):
    if request.method == "POST":
        producto_id = str(request.POST.get("producto_id")).strip()
        email = str(request.POST.get("email_cliente")).strip()
        cantidad = int(request.POST.get("cantidad"))
        
        # Extraer usuario del correo (parte antes del @) para cumplir min_length=2
        nombre_usuario = email.split('@')[0] if '@' in email else "Cliente"
        if len(nombre_usuario) < 2:
            nombre_usuario = "Cliente"

        # Estructura JSON exacta que exige tu PedidoCreate
        payload = {
            "usuario": nombre_usuario,
            "correo": email,
            "productos": [
                {
                    "producto_id": producto_id,
                    "cantidad": cantidad
                }
            ]
        }

        try:
            response = requests.post(f"{API_URL}/pedidos/", json=payload)
            if response.status_code in [200, 201]:
                return redirect('/?exito=¡Pedido realizado con éxito!')
            else:
                print("Detalle de error FastAPI:", response.status_code, response.text)
                return redirect(f'/?error=Error en el pedido (Código {response.status_code})')
        except Exception as e:
            return redirect(f'/?error=Error de conexión: {str(e)}')

    return redirect('catalogo')