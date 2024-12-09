# vista/adminoptions/gestionar_habitaciones_view.py

import flet as ft
from controlador.habitacion_controller import HabitacionController
from controlador.hotel_controller import HotelController

def gestionar_habitaciones_view(page: ft.Page):
    """
    Vista para gestionar las habitaciones del hotel.
    
    Args:
        page (ft.Page): La página de Flet donde se renderizará la vista.
    """
    # Inicializar los controladores necesarios
    habitacion_controller = HabitacionController()
    hotel_controller = HotelController()

    # Obtener todas las habitaciones
    habitaciones = habitacion_controller.obtener_habitaciones()

    # Crear una lista para mostrar las habitaciones
    habitaciones_list = ft.Column(scroll="auto")
    habitaciones_list.controls.append(
        ft.Row([
            ft.Text("ID", weight="bold", width=50),
            ft.Text("Número", weight="bold", width=100),
            ft.Text("Piso", weight="bold", width=50),
            ft.Text("Estado", weight="bold", width=150),
            ft.Text("Hotel", weight="bold", width=150),
            ft.Text("Acciones", weight="bold", width=150)
        ])
    )

    # Agregar cada habitación a la lista
    for h in habitaciones:
        hotel = hotel_controller.obtener_hotel_por_id(h.hotel_id)
        hotel_nombre = hotel.nombre if hotel else "N/A"

        habitaciones_list.controls.append(
            ft.Row([
                ft.Text(str(h.id), width=50),
                ft.Text(str(h.numero), width=100),
                ft.Text(str(h.piso), width=50),
                ft.Text(h.estado, width=150),
                ft.Text(hotel_nombre, width=150),
                ft.Row([
                    ft.IconButton(
                        ft.icons.EDIT,
                        tooltip="Editar Habitación",
                        on_click=lambda e, hid=h.id: abrir_editar_habitacion(page, hid)
                    ),
                    ft.IconButton(
                        ft.icons.DELETE,
                        tooltip="Eliminar Habitación",
                        on_click=lambda e, hid=h.id: eliminar_habitacion(page, hid)
                    )
                ], width=150)
            ])
        )

    # Función para abrir el diálogo de creación de habitación
    def abrir_crear_habitacion(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Crear Nueva Habitación"),
            content=crear_editar_habitacion_form(),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Crear", on_click=lambda e: crear_habitacion(page, dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Función para abrir el diálogo de edición de habitación
    def abrir_editar_habitacion(page: ft.Page, habitacion_id):
        habitacion = habitacion_controller.obtener_habitacion_por_id(habitacion_id)
        if not habitacion:
            page.snack_bar = ft.SnackBar(ft.Text("Habitación no encontrada"))
            page.snack_bar.open = True
            page.update()
            return

        dialog = ft.AlertDialog(
            title=ft.Text(f"Editar Habitación ID: {habitacion_id}"),
            content=crear_editar_habitacion_form(habitacion),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Guardar", on_click=lambda e: editar_habitacion(page, dialog, habitacion_id))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Función para crear una nueva habitación
    def crear_habitacion(page: ft.Page, dialog: ft.AlertDialog):
        numero = numero_field.value
        piso = piso_field.value
        estado = estado_dropdown.value
        hotel_dropdown_value = hotel_dropdown.value

        # Validar campos obligatorios
        if not numero or not estado or not hotel_dropdown_value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos obligatorios"))
            page.snack_bar.open = True
            page.update()
            return

        # Obtener el ID del hotel seleccionado
        try:
            hotel_id = int(hotel_dropdown_value.split(" - ")[0])
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Selección de hotel inválida"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Crear la habitación en la base de datos
            habitacion_controller.crear_habitacion(numero, piso, estado, hotel_id)
            page.snack_bar = ft.SnackBar(ft.Text("Habitación creada exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            # Refrescar la lista de habitaciones
            gestionar_habitaciones_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al crear habitación"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())]
            )
            page.dialog.open = True
            page.update()

    # Función para editar una habitación existente
    def editar_habitacion(page: ft.Page, dialog: ft.AlertDialog, habitacion_id):
        numero = numero_field.value
        piso = piso_field.value
        estado = estado_dropdown.value
        hotel_dropdown_value = hotel_dropdown.value

        # Validar campos obligatorios
        if not numero or not estado or not hotel_dropdown_value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos obligatorios"))
            page.snack_bar.open = True
            page.update()
            return

        # Obtener el ID del hotel seleccionado
        try:
            hotel_id = int(hotel_dropdown_value.split(" - ")[0])
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Selección de hotel inválida"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Actualizar la habitación en la base de datos
            habitacion_controller.actualizar_habitacion(
                habitacion_id, numero=numero, piso=piso, estado=estado, hotel_id=hotel_id
            )
            page.snack_bar = ft.SnackBar(ft.Text("Habitación actualizada exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            # Refrescar la lista de habitaciones
            gestionar_habitaciones_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al actualizar habitación"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())]
            )
            page.dialog.open = True
            page.update()

    # Función para eliminar una habitación
    def eliminar_habitacion(page: ft.Page, habitacion_id):
        try:
            if habitacion_controller.eliminar_habitacion(habitacion_id):
                page.snack_bar = ft.SnackBar(ft.Text("Habitación eliminada exitosamente"))
                page.snack_bar.open = True
                page.update()
                # Refrescar la lista de habitaciones
                gestionar_habitaciones_view(page)
            else:
                page.dialog = ft.AlertDialog(title=ft.Text("Error al eliminar habitación"))
                page.dialog.open = True
                page.update()
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al eliminar habitación"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())]
            )
            page.dialog.open = True
            page.update()

    # Función para crear el formulario de creación/edición de habitación
    def crear_editar_habitacion_form(habitacion=None):
        """
        Crea el formulario para crear o editar una habitación.
        
        Args:
            habitacion (Habitacion, optional): La habitación a editar. Si es None, se crea una nueva.
        
        Returns:
            ft.Column: El formulario de Flet.
        """
        # Obtener la lista de hoteles para el dropdown
        hoteles = hotel_controller.obtener_hoteles()

        # Campos del formulario
        numero_field = ft.TextField(
            label="Número",
            value=str(habitacion.numero) if habitacion else "",
            width=200
        )
        piso_field = ft.TextField(
            label="Piso",
            value=str(habitacion.piso) if habitacion else "",
            width=200
        )
        estado_dropdown = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("Disponible"),
                ft.dropdown.Option("Ocupada"),
                ft.dropdown.Option("Mantenimiento"),
            ],
            value=habitacion.estado if habitacion else None,
            width=200
        )
        hotel_dropdown = ft.Dropdown(
            label="Hotel",
            options=[ft.dropdown.Option(f"{h.id} - {h.nombre}") for h in hoteles],
            value=f"{habitacion.hotel_id} - {hotel_controller.obtener_hotel_por_id(h.hotel_id).nombre}" if habitacion else None,
            width=400
        )

        # Crear el formulario
        form = ft.Column([
            numero_field,
            piso_field,
            estado_dropdown,
            hotel_dropdown
        ], spacing=10)

        return form

    # Botón para crear una nueva habitación
    crear_habitacion_button = ft.ElevatedButton(
        "Crear Nueva Habitación",
        icon=ft.icons.ADD,
        on_click=abrir_crear_habitacion
    )

    # Añadir el botón y la lista de habitaciones a la vista
    habitaciones_view = ft.Column([
        ft.Text("Gestión de Habitaciones", style="headlineMedium"),
        crear_habitacion_button,
        habitaciones_list
    ], scroll="auto")

    return habitaciones_view
