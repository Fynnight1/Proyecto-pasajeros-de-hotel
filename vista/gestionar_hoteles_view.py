import flet as ft
from controlador.hotel_controller import HotelController
from controlador.habitacion_controller import HabitacionController

def gestionar_hoteles_view(page: ft.Page):
    hotel_controller = HotelController()
    habitacion_controller = HabitacionController()
    hoteles = hotel_controller.obtener_hoteles()

    hoteles_list = ft.Column(scroll="auto")
    hoteles_list.controls.append(
        ft.Row([
            ft.Text("ID", weight="bold"),
            ft.Text("Nombre", weight="bold"),
            ft.Text("Dirección", weight="bold"),
            ft.Text("Teléfono", weight="bold"),
            ft.Text("Habitaciones", weight="bold"),
            ft.Text("Acciones", weight="bold")
        ])
    )
    for hotel in hoteles:
        habitaciones = hotel.obtener_habitaciones()
        habitaciones_str = ", ".join([f"N° {h.numero} ({h.estado})" for h in habitaciones])
        hoteles_list.controls.append(
            ft.Row([
                ft.Text(str(hotel.id)),
                ft.Text(hotel.nombre),
                ft.Text(hotel.direccion),
                ft.Text(hotel.telefono),
                ft.Text(habitaciones_str if habitaciones_str else "N/A"),
                ft.Row([
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, hid=hotel.id: editar_hotel(hid)),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, hid=hotel.id: eliminar_hotel(hid))
                ])
            ])
        )
    
    def editar_hotel(hotel_id):
        # Implementar la lógica para editar un hotel y sus habitaciones
        pass

    def eliminar_hotel(hotel_id):
        if hotel_controller.eliminar_hotel(hotel_id):
            page.snack_bar = ft.SnackBar(ft.Text("Hotel eliminado exitosamente"))
            page.snack_bar.open = True
            page.update()
            gestionar_hoteles_view(page)
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("Error al eliminar hotel"))
            page.dialog.open = True
            page.update()

    # Botón para crear un nuevo hotel
    crear_hotel_button = ft.ElevatedButton("Crear Nuevo Hotel", on_click=crear_hotel_view)

    def crear_hotel_view(e):
        # Implementar la lógica para crear un nuevo hotel
        pass

    # Barra de navegación específica
    nav_bar = get_navbar([
        crear_hotel_button,
        ft.IconButton(ft.icons.BACKSPACE, on_click=lambda e: navigate_to_previous_view())
    ])

    page.add(
        ft.Column([
            ft.Text("Gestión de Hoteles", style="headlineMedium"),
            nav_bar,
            hoteles_list
        ], scroll="auto")
    )
