# vista/login_view.py

import flet as ft
from controlador.usuario_controller import UsuarioController
from vista.dashboard_view import dashboard_view

def login_view(page: ft.Page):
    usuario_controller = UsuarioController()

    def on_login(e):
        username = username_field.value
        password = password_field.value

        usuario = usuario_controller.autenticar(username, password)
        if usuario:
            page.session.set("usuario_id", usuario.id)
            page.session.set("rol", usuario.rol)
            page.clean()
            dashboard_view(page, usuario)
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("Credenciales incorrectas"))
            page.dialog.open = True
            page.update()

    username_field = ft.TextField(label="Usuario")
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)

    login_button = ft.ElevatedButton(text="Iniciar Sesión", on_click=on_login)
    register_button = ft.TextButton(text="¿No tienes cuenta? Regístrate", on_click=lambda e: mostrar_registro())

    def mostrar_registro():
        page.clean()
        from vista.registro_cliente_view import registro_cliente_view
        registro_cliente_view(page)

    page.add(
        ft.Column(
            [
                ft.Text("Inicio de Sesión", style="headlineMedium"),
                username_field,
                password_field,
                login_button,
                register_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
