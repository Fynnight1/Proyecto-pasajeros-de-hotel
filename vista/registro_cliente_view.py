# vista/registro_cliente_view.py

import flet as ft
from controlador.usuario_controller import UsuarioController

def registro_cliente_view(page: ft.Page):
    controller = UsuarioController()

    def on_register(e):
        nombre = nombre_field.value
        rut = rut_field.value
        direccion = direccion_field.value
        telefono = telefono_field.value
        username = username_field.value
        password = password_field.value

        if not nombre or not rut or not username or not password:
            page.dialog = ft.AlertDialog(title=ft.Text("Los campos Nombre, RUT, Usuario y Contraseña son obligatorios"))
            page.dialog.open = True
            page.update()
            return

        try:
            controller.crear_usuario(nombre, rut, direccion, telefono, username, password, 'cliente')
            page.snack_bar = ft.SnackBar(ft.Text("Registro exitoso. Puedes iniciar sesión ahora."))
            page.snack_bar.open = True
            page.update()
            # Limpiar campos
            nombre_field.value = ""
            rut_field.value = ""
            direccion_field.value = ""
            telefono_field.value = ""
            username_field.value = ""
            password_field.value = ""
        except Exception as ex:
            page.dialog = ft.AlertDialog(title=ft.Text(f"Error al registrar: {str(ex)}"))
            page.dialog.open = True
            page.update()

    # Campos de entrada
    nombre_field = ft.TextField(label="Nombre")
    rut_field = ft.TextField(label="RUT")
    direccion_field = ft.TextField(label="Dirección")
    telefono_field = ft.TextField(label="Teléfono")
    username_field = ft.TextField(label="Usuario")
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)

    # Botón de registro
    register_button = ft.ElevatedButton(text="Registrar", on_click=on_register)

    # Botón para volver al login
    back_button = ft.TextButton(text="Volver al Login", on_click=lambda e: volver_login())

    def volver_login():
        page.clean()
        from vista.login_view import login_view
        login_view(page)

    # Layout sin alineación en el Text
    page.add(
        ft.Column(
            [
                ft.Text("Registro de Cliente", style="headlineMedium"),
                nombre_field,
                rut_field,
                direccion_field,
                telefono_field,
                username_field,
                password_field,
                register_button,
                back_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
