import flet as ft
from controlador.administrador_controller import AdministradorController
from vista.cliente_view import cliente_view

def login_view(page: ft.Page):
    controller = AdministradorController()

    def iniciar_sesion(e):
        username = username_field.value
        password = password_field.value

        if controller.autenticar(username, password):
            page.clean()
            cliente_view(page)
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("Credenciales incorrectas"))
            page.dialog.open = True
            page.update()
    
    username_field = ft.TextField(label="Usuario")
    password_field = ft.TextField(label="Contraseña", password=True)
    boton_login = ft.ElevatedButton(text="Iniciar Sesión", on_click=iniciar_sesion)
    
    page.add(
        ft.Column([
            ft.Text("Inicio de Sesión", size=30, weight="bold"),
            username_field,
            password_field,
            boton_login
        ], alignment="center", horizontal_alignment="center")
    )