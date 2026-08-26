import os

import requests
from django.shortcuts import render, redirect

from .forms import PedidoForm

API_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000").rstrip("/")

def catalogo(request):
    productos = []
    error = request.GET.get('error')
    mensaje_exito = request.GET.get('exito')
    
    try:
        response = requests.get(f"{API_URL}/productos/", timeout=5)
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


def resumen_pedidos(request):
    try:
        response = requests.get(f"{API_URL}/pedidos/resumen", timeout=5)
        if response.status_code == 200:
            resumen = response.json()
        else:
            resumen = []
            error = "No se pudo obtener el resumen de pedidos."
    except requests.RequestException:
        resumen = []
        error = "No se pudo conectar con el microservicio de FastAPI."

    return render(request, "resumen_pedidos.html", {
        "resumen": resumen,
        "error": locals().get("error"),
    })


def checkout(request, producto_id):
    try:
        response = requests.get(f"{API_URL}/productos/{producto_id}", timeout=5)
    except requests.RequestException:
        return render(request, "checkout.html", {
            "error": "No se pudo conectar con el microservicio de FastAPI.",
            "form": PedidoForm(),
        }, status=503)

    if response.status_code != 200:
        return render(request, "checkout.html", {
            "error": "El producto solicitado no está disponible.",
            "form": PedidoForm(),
        }, status=response.status_code)

    producto = response.json()
    form = PedidoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        payload = {
            "usuario": form.cleaned_data["nombre"],
            "correo": form.cleaned_data["correo"],
            "productos": [{"producto_id": producto_id, "cantidad": form.cleaned_data["cantidad"]}],
        }
        try:
            pedido_response = requests.post(f"{API_URL}/pedidos/", json=payload, timeout=5)
        except requests.RequestException:
            form.add_error(None, "No se pudo conectar con el microservicio de FastAPI.")
        else:
            if pedido_response.status_code in (200, 201):
                return render(request, "checkout.html", {
                    "producto": producto,
                    "form": PedidoForm(),
                    "pedido": pedido_response.json(),
                })
            try:
                detail = pedido_response.json().get("detail", "No se pudo crear el pedido.")
            except ValueError:
                detail = "No se pudo crear el pedido."
            form.add_error(None, detail)

    form.fields["cantidad"].widget.attrs["max"] = producto.get("stock", 0)
    return render(request, "checkout.html", {"producto": producto, "form": form})

def crear_pedido(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id", "").strip()
        email = request.POST.get("email_cliente", "").strip()
        try:
            cantidad = int(request.POST.get("cantidad", "0"))
        except (TypeError, ValueError):
            return redirect("/?error=La cantidad debe ser un número válido")

        if not producto_id or not email or cantidad < 1:
            return redirect("/?error=Completa los datos del pedido")
        
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
            response = requests.post(f"{API_URL}/pedidos/", json=payload, timeout=5)
            if response.status_code in [200, 201]:
                return redirect('/?exito=¡Pedido realizado con éxito!')
            else:
                print("Detalle de error FastAPI:", response.status_code, response.text)
                return redirect(f'/?error=Error en el pedido (Código {response.status_code})')
        except requests.RequestException:
            return redirect("/?error=No se pudo conectar con el microservicio de FastAPI")

    return redirect('catalogo')