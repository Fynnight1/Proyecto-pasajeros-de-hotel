# main.py

import flet as ft # type: ignore
from views.login_view import login_view
from models.database import Database

def main(page: ft.Page):
    page.title = "Sistema de Reserva de Hoteles"
    page.window.height = 700
    page.window.width = 1200

    # Inicializar la conexión a la base de datos
    Database.initialize(
        user="postgres",           # Reemplaza con tu usuario de PostgreSQL
        password="Fynnight",      # Reemplaza con tu contraseña de PostgreSQL
        host="localhost",
        port="5432",
        database="hotel_reservation_db"
    )

    # Mostrar la vista de login al inicio
    login_view(page)

    def on_close(e):
        Database.close_all_connections()

    page.on_close = on_close

ft.app(target=main)
