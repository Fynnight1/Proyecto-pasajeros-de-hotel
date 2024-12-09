# vista/adminoptions/gestionar_hoteles_view.py

import flet as ft
from controlador.hotel_controller import HotelController

def gestionar_hoteles_view(page: ft.Page):
    hotel_controller = HotelController()
    hoteles = hotel_controller.obtener_hoteles()

    hoteles_list = ft.Column(scroll="auto")
    hoteles_list.controls.append(
        ft.Row([
            ft.Text("ID", weight="bold", width=50),
            ft.Text("Nombre", weight="bold", width=150),
            ft.Text("Dirección", weight="bold", width=200),
            ft.Text("Teléfono", weight="bold", width=100),
            ft.Text("Habitaciones", weight="bold", width=200),
            ft.Text("Acciones", weight="bold", width=150)
        ])
    )

    for hotel in hoteles:
        habitaciones = hotel.obtener_habitaciones()
        habitaciones_str = ", ".join([f"N° {h.numero} ({h.estado})" for h in habitaciones])
        hoteles_list.controls.append(
            ft.Row([
                ft.Text(str(hotel.id), width=50),
                ft.Text(hotel.nombre, width=150),
                ft.Text(hotel.direccion, width=200),
                ft.Text(hotel.telefono, width=100),
                ft.Text(habitaciones_str if habitaciones_str else "N/A", width=200),
                ft.Row([
                    ft.IconButton(
                        ft.icons.EDIT,
                        on_click=lambda e, hid=hotel.id: abrir_editar_hotel(page, hid)
                    ),
                    ft.IconButton(
                        ft.icons.DELETE,
                        on_click=lambda e, hid=hotel.id: eliminar_hotel(page, hid)
                    )
                ], width=150)
            ])
        )

    def abrir_crear_hotel(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Crear Nuevo Hotel"),
            content=crear_editar_hotel_form(),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Crear", on_click=lambda e: crear_hotel(page, dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def abrir_editar_hotel(page: ft.Page, hotel_id):
        hotel = hotel_controller.obtener_hotel_por_id(hotel_id)
        if not hotel:
            page.snack_bar = ft.SnackBar(ft.Text("Hotel no encontrado"))
            page.snack_bar.open = True
            page.update()
            return

        dialog = ft.AlertDialog(
            title=ft.Text(f"Editar Hotel ID: {hotel_id}"),
            content=crear_editar_hotel_form(hotel),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Guardar", on_click=lambda e: editar_hotel(page, dialog, hotel_id))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def crear_hotel(page: ft.Page, dialog: ft.AlertDialog):
        nombre = nombre_field.value
        direccion = direccion_field.value
        telefono = telefono_field.value

        if not nombre:
            page.snack_bar = ft.SnackBar(ft.Text("El campo Nombre es obligatorio"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            hotel_controller.crear_hotel(nombre, direccion, telefono)
            page.snack_bar = ft.SnackBar(ft.Text("Hotel creado exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            # Refrescar la lista de hoteles
            gestionar_hoteles_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al crear hotel"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())]
            )
            page.dialog.open = True
            page.update()

    def editar_hotel(page: ft.Page, dialog: ft.AlertDialog, hotel_id):
        nombre = nombre_field.value
        direccion = direccion_field.value
        telefono = telefono_field.value

        if not nombre:
            page.snack_bar = ft.SnackBar(ft.Text("El campo Nombre es obligatorio"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            hotel_controller.actualizar_hotel(hotel_id, nombre=nombre, direccion=direccion, telefono=telefono)
            page.snack_bar = ft.SnackBar(ft.Text("Hotel actualizado exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            # Refrescar la lista de hoteles
            gestionar_hoteles_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al actualizar hotel"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())]
            )
            page.dialog.open = True
            page.update()

    def eliminar_hotel(page: ft.Page, hotel_id):
        if hotel_controller.eliminar_hotel(hotel_id):
            page.snack_bar = ft.SnackBar(ft.Text("Hotel eliminado exitosamente"))
            page.snack_bar.open = True
            page.update()
            gestionar_hoteles_view(page)
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("Error al eliminar hotel"))
            page.dialog.open = True
            page.update()

    def crear_editar_hotel_form(hotel=None):
        """Crea el formulario para crear o editar un hotel."""
        nombre_field = ft.TextField(label="Nombre", value=hotel.nombre if hotel else "")
        direccion_field = ft.TextField(label="Dirección", value=hotel.direccion if hotel else "")
        telefono_field = ft.TextField(label="Teléfono", value=hotel.telefono if hotel else "")

        form = ft.Column([
            nombre_field,
            direccion_field,
            telefono_field
        ], spacing=10)

        return form

    # Botón para crear nuevo hotel
    crear_hotel_button = ft.ElevatedButton("Crear Nuevo Hotel", on_click=abrir_crear_hotel)

    # Añadimos el botón de crear hotel arriba de la lista
    hoteles_view = ft.Column([
        ft.Text("Gestión de Hoteles", style="headlineMedium"),
        crear_hotel_button,
        hoteles_list
    ], scroll="auto")

    return hoteles_view
