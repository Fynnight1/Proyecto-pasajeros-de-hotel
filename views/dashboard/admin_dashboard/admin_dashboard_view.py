# views/dashboard/admin_dashboard/admin_dashboard_view.py

import flet as ft  # type: ignore
from views.shared.navbar import get_navbar
from controllers.hotel_controller import HotelController
from controllers.user_controller import UserController
from controllers.room_controller import RoomController
from controllers.reservation_controller import ReservationController
from views.shared.logout_button import logout_button  # Importa el botón de logout

def admin_dashboard(page: ft.Page, usuario):
    page.views.clear()

    def go_hoteles(e):
        from views.dashboard.admin_dashboard.hotel.hotel_views import hotel_list_view
        page.views.append(hotel_list_view(page))
        page.go("/admin/hoteles")
        page.update()

    def go_habitaciones(e):
        from views.dashboard.admin_dashboard.habitacion.habitacion_views import habitacion_list_view
        page.views.append(habitacion_list_view(page))
        page.go("/admin/habitaciones")
        page.update()

    def go_reservas(e):
        from views.dashboard.admin_dashboard.reserva.reserva_views import reserva_list_view
        page.views.append(reserva_list_view(page))
        page.go("/admin/reservas")
        page.update()

    def go_usuarios(e):
        from views.dashboard.admin_dashboard.usuario.usuario_views import usuario_list_view
        page.views.append(usuario_list_view(page))
        page.go("/admin/usuarios")
        page.update()

    nav = get_navbar([
        ft.ElevatedButton("Gestionar Hoteles", on_click=go_hoteles),
        ft.ElevatedButton("Gestionar Habitaciones", on_click=go_habitaciones),
        ft.ElevatedButton("Gestionar Reservas", on_click=go_reservas),
        ft.ElevatedButton("Gestionar Usuarios", on_click=go_usuarios),
        logout_button(page)  # Aquí se agrega el botón de logout compartido
    ])

    main_view = ft.View(
        "/admin",
        controls=[
            ft.Column(
                [
                    ft.Text(f"Bienvenido administrador: {usuario.name}", style="headlineMedium"),
                    nav
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    )

    page.views.append(main_view)
    page.go("/admin")
    page.update()
