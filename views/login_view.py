# views/login_view.py
import flet as ft # type: ignore
from controllers.user_controller import UserController

def login_view(page: ft.Page):
    user_controller = UserController()

    def on_login(e):
        username = username_field.value
        password = password_field.value

        user = user_controller.authenticate(username, password)
        if user:
            page.session.set("user_id", user.id)
            page.session.set("role", user.role)
            page.clean()  # Aquí sí lo usas al pasar al dashboard
            from views.dashboard_view import dashboard_view
            dashboard_view(page, user)
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("Incorrect Credentials"))
            page.dialog.open = True
            page.update()

    def show_registration(e):
        page.clean()
        from views.register_client_view import register_client_view
        register_client_view(page)

    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True)
    login_button = ft.ElevatedButton(text="Login", on_click=on_login)
    register_button = ft.TextButton(text="Don't have an account? Register", on_click=show_registration)

    # Agregar controles del login directamente
    page.add(
        ft.Column(
            [
                ft.Text("Login", style="headlineMedium"),
                username_field,
                password_field,
                login_button,
                register_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
