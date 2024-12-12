# views/register_client_view.py

import flet as ft  # type: ignore
from controllers.user_controller import UserController

def register_client_view(page: ft.Page):
    controller = UserController()

    def on_register(e):
        name = name_field.value
        rut = rut_field.value
        address = address_field.value
        phone = phone_field.value
        username = username_field.value
        password = password_field.value

        if not name or not rut or not username or not password:
            page.dialog = ft.AlertDialog(title=ft.Text("Name, RUT, Username, and Password are required fields"))
            page.dialog.open = True
            page.update()
            return

        try:
            controller.create_user(name, rut, address, phone, username, password, 'client')
            page.snack_bar = ft.SnackBar(ft.Text("Registration successful. You can now log in."))
            page.snack_bar.open = True
            page.update()
            # Clear fields
            name_field.value = ""
            rut_field.value = ""
            address_field.value = ""
            phone_field.value = ""
            username_field.value = ""
            password_field.value = ""
        except Exception as ex:
            page.dialog = ft.AlertDialog(title=ft.Text(f"Registration Error: {str(ex)}"))
            page.dialog.open = True
            page.update()

    # Input Fields
    name_field = ft.TextField(label="Name")
    rut_field = ft.TextField(label="RUT")
    address_field = ft.TextField(label="Address")
    phone_field = ft.TextField(label="Phone")
    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True)

    # Register Button
    register_button = ft.ElevatedButton(text="Register", on_click=on_register)

    # Back to Login Button
    back_button = ft.TextButton(text="Back to Login", on_click=lambda e: back_to_login())

    def back_to_login():
        page.clean()
        from views.login_view import login_view
        login_view(page)

    # Layout without Text alignment
    page.add(
        ft.Column(
            [
                ft.Text("Client Registration", style="headlineMedium"),
                name_field,
                rut_field,
                address_field,
                phone_field,
                username_field,
                password_field,
                register_button,
                back_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
