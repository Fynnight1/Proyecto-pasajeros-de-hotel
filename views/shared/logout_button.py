# views/shared/logout_button.py
import flet as ft # type: ignore
from views.shared.logout_view import logout_view

def logout_button(page: ft.Page):
    def on_logout(e):
        # Mostrar la vista de confirmación de logout
        page.views.append(logout_view(page))
        page.go("/logout")
        page.update()
    return ft.ElevatedButton(
        "Cerrar Sesión", 
        on_click=on_logout, 
        color=ft.colors.WHITE, 
        bgcolor=ft.colors.RED
    )
