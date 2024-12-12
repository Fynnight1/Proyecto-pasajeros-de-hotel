# views/trabajador_dashboard/worker_dashboard_view.py

import flet as ft  # type: ignore
from views.shared.navbar import get_navbar
from views.shared.logout_button import logout_button

def worker_dashboard(page: ft.Page, usuario):
    page.views.clear()

    def go_reservas(e):
        from views.dashboard.worker_dashboard.reservation.reservation_views import reserva_list_trabajador_view
        page.views.append(reserva_list_trabajador_view(page, usuario))
        page.go("/worker/reservas")
        page.update()

    nav = get_navbar([
        ft.ElevatedButton("Gestionar Reservas", on_click=go_reservas),
        logout_button(page)  # Agregamos el botón de logout
    ])

    main_view = ft.View(
        "/worker",
        controls=[
            ft.Column(
                [
                    ft.Text(f"Bienvenido trabajador: {usuario.name}", style="headlineMedium"),
                    nav
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    )

    page.views.append(main_view)
    page.go("/worker")
    page.update()
