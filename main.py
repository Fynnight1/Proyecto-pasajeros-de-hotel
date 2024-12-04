import flet as ft
from vista.login_view import login_view

def main(page: ft.Page):
    page.title = "Sistema de Reserva de Hoteles"
    login_view(page)

ft.app(target=main)