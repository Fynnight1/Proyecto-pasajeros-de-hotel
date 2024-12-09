# main.py

import flet as ft
from vista.login_view import login_view
from modelo.database import Database

def main(page: ft.Page):
    page.title = "Sistema de Reserva de Hoteles"
    page.window.height = 700
    page.window.width = 1000

    # Inicializar la conexión a la base de datos
    Database.initialize(
        user="postgres",           # Reemplaza con tu usuario de PostgreSQL
        password="Admin1234",      # Reemplaza con tu contraseña de PostgreSQL
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
