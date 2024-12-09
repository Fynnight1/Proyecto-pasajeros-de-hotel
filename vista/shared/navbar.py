import flet as ft

def get_navbar(botones):
    return ft.Row(
        botones,
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
