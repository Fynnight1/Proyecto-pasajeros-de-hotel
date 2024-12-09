# vista/admin_dashboard.py

import flet as ft
from vista.adminoptions.gestionar_usuarios_view import gestionar_usuarios_view
from vista.adminoptions.gestionar_hoteles_view import gestionar_hoteles_view
from vista.adminoptions.gestionar_habitaciones_view import gestionar_habitaciones_view
from vista.adminoptions.gestionar_reservas_view import gestionar_reservas_view

def admin_dashboard(page: ft.Page, usuario):
    """
    Dashboard para usuarios con rol de administrador.
    
    Args:
        page (ft.Page): La página de Flet.
        usuario (Usuario): El objeto de usuario autenticado.
    """
    # Crear una sección de contenido dinámica
    content = ft.Container()

    def navigate_to(view_func):
        """Actualiza la sección de contenido con la vista correspondiente."""
        content.content = view_func(page)
        page.update()

    # Funciones para mostrar las diferentes vistas
    def mostrar_usuarios(e):
        navigate_to(gestionar_usuarios_view)

    def mostrar_hoteles(e):
        navigate_to(gestionar_hoteles_view)

    def mostrar_habitaciones(e):
        navigate_to(gestionar_habitaciones_view)

    def mostrar_reservas(e):
        navigate_to(gestionar_reservas_view)

    # Barra de navegación específica para el administrador
    nav_bar_admin = ft.Row(
        [
            ft.ElevatedButton("Gestionar Usuarios", on_click=mostrar_usuarios),
            ft.ElevatedButton("Gestionar Hoteles", on_click=mostrar_hoteles),
            ft.ElevatedButton("Gestionar Habitaciones", on_click=mostrar_habitaciones),
            ft.ElevatedButton("Gestionar Reservas", on_click=mostrar_reservas),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Layout principal del dashboard con barra de navegación y contenido dinámico
    page.add(
        ft.Column(
            [
                ft.Text(f"Bienvenido, {usuario.nombre} (Administrador)", style="headlineLarge"),
                nav_bar_admin,
                ft.Divider(),
                content
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=20
        )
    )

    # Cargar una vista por defecto al iniciar el dashboard
    mostrar_usuarios(None)
