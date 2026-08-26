from django import forms


class PedidoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        min_length=2,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Tu nombre", "required": True}),
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "tu@correo.com", "required": True}),
    )
    cantidad = forms.IntegerField(
        label="Cantidad",
        min_value=1,
        widget=forms.NumberInput(attrs={"min": 1, "required": True}),
    )
