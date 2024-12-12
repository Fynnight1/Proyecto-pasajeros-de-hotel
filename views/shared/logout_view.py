import flet as ft # type: ignore
from views.login_view import login_view

def logout_view(page: ft.Page):
    def on_confirm(e):
        page.session.clear()
        page.views.clear()
        page.clean()

        # Volver a mostrar el login
        login_view(page)
        
        # Ir a la ruta principal (opcional, si es que usas rutas)
        page.go("/")
        page.update()

    def on_cancel(e):
        # Volver a la vista anterior
        if len(page.views) > 1:
            page.views.pop()
            page.update()
        else:
            # Si no hay vista anterior, volvemos al login
            page.clean()
            login_view(page)
            page.go("/")
            page.update()

    texto = ft.Text("¿Desea cerrar sesión?", style="headlineSmall")
    boton_si = ft.ElevatedButton("Sí", on_click=on_confirm, color=ft.colors.WHITE, bgcolor=ft.colors.RED)
    boton_no = ft.ElevatedButton("No", on_click=on_cancel)

    return ft.View(
        "/logout",
        controls=[
            ft.Column(
                [
                    texto,
                    ft.Row([boton_si, boton_no], alignment=ft.MainAxisAlignment.CENTER)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    )
