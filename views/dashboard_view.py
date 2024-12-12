# views/dashboard_view.py

import flet as ft  # type: ignore

def dashboard_view(page: ft.Page, user):
    role = user.role

    def logout(e):
        page.session.clear()
        page.clean()
        # Importar login_view aquí localmente para evitar ciclo
        from views.login_view import login_view
        login_view(page)

    # Common Navbar for all roles
    nav_bar = ft.Row(
        [
            ft.ElevatedButton("Logout", on_click=logout)
        ],
        alignment=ft.MainAxisAlignment.END,
        spacing=10
    )

    page.add(nav_bar)

    # Importamos las vistas según el rol localmente
    if role == "administrator":
        from views.dashboard.admin_dashboard.admin_dashboard_view import admin_dashboard
        admin_dashboard(page, user)
    elif role == "worker":
        from views.dashboard.worker_dashboard.worker_dashboard_view import worker_dashboard
        worker_dashboard(page, user)
    elif role == "client":
        from views.dashboard.client_dashboard.client_dashboard_view import client_dashboard
        client_dashboard(page, user)
    else:
        page.dialog = ft.AlertDialog(title=ft.Text("Unknown Role"))
        page.dialog.open = True
        page.update()
