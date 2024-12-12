# views/client_dashboard/client_dashboard_view.py

import flet as ft  # type: ignore
from views.shared.navbar import get_navbar
from views.shared.logout_button import logout_button

def client_dashboard(page: ft.Page, usuario):
    page.views.clear()

    def ir_reservas(e):
        from views.dashboard.client_dashboard.reserva.reserva_views import reserva_list_cliente_view
        page.views.append(reserva_list_cliente_view(page, usuario))
        page.go("/client/reservas")
        page.update()

    nav = get_navbar([
        ft.ElevatedButton("Mis Reservas", on_click=ir_reservas),
        logout_button(page)  # Agregamos el botón de logout
    ])

    main_view = ft.View(
        "/client",
        controls=[
            ft.Column(
                [
                    ft.Text(f"Bienvenido cliente: {usuario.name}", style="headlineMedium"),
                    nav
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    )

    page.views.append(main_view)
    page.go("/client")
    page.update()
