# vista/dashboard_view.py

import flet as ft
from vista.admin_dashboard import admin_dashboard
from vista.trabajador_dashboard import trabajador_dashboard
from vista.cliente_dashboard import cliente_dashboard

def dashboard_view(page: ft.Page, usuario):
    rol = usuario.rol

    def logout(e):
        # Implementar la lógica de cierre de sesión
        page.session.clear()
        page.clean()
        from vista.login_view import login_view
        login_view(page)

    # Navbar común para todos los roles
    nav_bar = ft.Row(
        [
            ft.ElevatedButton("Cerrar Sesión", on_click=logout)
        ],
        alignment=ft.MainAxisAlignment.END,
        spacing=10
    )

    # Layout inicial del dashboard
    page.add(nav_bar)

    # Redirigir según el rol
    if rol == "administrador":
        admin_dashboard(page, usuario)
    elif rol == "trabajador":
        trabajador_dashboard(page, usuario)
    elif rol == "cliente":
        cliente_dashboard(page, usuario)
    else:
        page.dialog = ft.AlertDialog(title=ft.Text("Rol desconocido"))
        page.dialog.open = True
        page.update()
