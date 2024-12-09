# vista/adminoptions/gestionar_reservas_view.py

import flet as ft
from controlador.reserva_controller import ReservaController
from controlador.habitacion_controller import HabitacionController
from controlador.hotel_controller import HotelController
from controlador.usuario_controller import UsuarioController

def gestionar_reservas_view(page: ft.Page):
    reserva_controller = ReservaController()
    habitacion_controller = HabitacionController()
    hotel_controller = HotelController()
    usuario_controller = UsuarioController()

    reservas = reserva_controller.obtener_reservas()
    reservas_list = ft.Column(scroll="auto")
    reservas_list.controls.append(
        ft.Row([
            ft.Text("ID", weight="bold", width=50),
            ft.Text("Cliente", weight="bold", width=150),
            ft.Text("Habitación", weight="bold", width=150),
            ft.Text("Trabajador", weight="bold", width=150),
            ft.Text("Ingreso", weight="bold", width=100),
            ft.Text("Salida", weight="bold", width=100),
            ft.Text("Acciones", weight="bold", width=150)
        ])
    )

    for r in reservas:
        cliente = usuario_controller.obtener_usuario_por_id(r.cliente_id)
        trabajador = usuario_controller.obtener_usuario_por_id(r.trabajador_id)
        habitacion = habitacion_controller.obtener_habitacion_por_id(r.habitacion_id)
        hotel = hotel_controller.obtener_hotel_por_id(habitacion.hotel_id) if habitacion else None
        cliente_nombre = cliente.nombre if cliente else "N/A"
        trabajador_nombre = trabajador.nombre if trabajador else "N/A"
        habitacion_info = f"N° {habitacion.numero} ({hotel.nombre if hotel else 'N/A'})" if habitacion else "N/A"

        reservas_list.controls.append(
            ft.Row([
                ft.Text(str(r.id), width=50),
                ft.Text(cliente_nombre, width=150),
                ft.Text(habitacion_info, width=150),
                ft.Text(trabajador_nombre, width=150),
                ft.Text(str(r.fecha_ingreso), width=100),
                ft.Text(str(r.fecha_salida), width=100),
                ft.Row([
                    ft.IconButton(
                        ft.icons.EDIT,
                        on_click=lambda e, rid=r.id: abrir_editar_reserva(page, rid)
                    ),
                    ft.IconButton(
                        ft.icons.DELETE,
                        on_click=lambda e, rid=r.id: eliminar_reserva(page, rid)
                    )
                ], width=150)
            ])
        )

    def abrir_crear_reserva(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Crear Nueva Reserva"),
            content=crear_editar_reserva_form(),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Crear", on_click=lambda e: crear_reserva(page, dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def abrir_editar_reserva(page: ft.Page, reserva_id):
        reserva = reserva_controller.obtener_reserva_por_id(reserva_id)
        if not reserva:
            page.snack_bar = ft.SnackBar(ft.Text("Reserva no encontrada"))
            page.snack_bar.open = True
            page.update()
            return

        dialog = ft.AlertDialog(
            title=ft.Text(f"Editar Reserva ID: {reserva_id}"),
            content=crear_editar_reserva_form(reserva),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Guardar", on_click=lambda e: editar_reserva(page, dialog, reserva_id))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def crear_reserva(page: ft.Page, dialog: ft.AlertDialog):
        cliente_value = cliente_dropdown.value.split(" - ")[0] if cliente_dropdown.value else None
        habitacion_value = habitacion_dropdown.value.split(" - ")[0] if habitacion_dropdown.value else None
        trabajador_value = trabajador_dropdown.value.split(" - ")[0] if trabajador_dropdown.value else None
        fecha_ingreso = fecha_ingreso_field.value
        fecha_salida = fecha_salida_field.value

        if not cliente_value or not habitacion_value or not trabajador_value or not fecha_ingreso or not fecha_salida:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            reserva_controller.crear_reserva(int(cliente_value), int(habitacion_value), int(trabajador_value), fecha_ingreso, fecha_salida)
            page.snack_bar = ft.SnackBar(ft.Text("Reserva creada exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            # Refrescar la lista de reservas
            gestionar_reservas_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al crear reserva"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: dialog.close())]
            )
            page.dialog.open = True
            page.update()

    def editar_reserva(page: ft.Page, dialog: ft.AlertDialog, reserva_id):
        cliente_value = cliente_dropdown.value.split(" - ")[0] if cliente_dropdown.value else None
        habitacion_value = habitacion_dropdown.value.split(" - ")[0] if habitacion_dropdown.value else None
        trabajador_value = trabajador_dropdown.value.split(" - ")[0] if trabajador_dropdown.value else None
        fecha_ingreso = fecha_ingreso_field.value
        fecha_salida = fecha_salida_field.value

        if not cliente_value or not habitacion_value or not trabajador_value or not fecha_ingreso or not fecha_salida:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos"))
            page.snack_bar.open = True
            page.update()
            return

        if fecha_salida <= fecha_ingreso:
            page.snack_bar = ft.SnackBar(ft.Text("La fecha de salida debe ser posterior a la de ingreso"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            reserva_controller.actualizar_reserva(
                reserva_id,
                cliente_id=int(cliente_value),
                habitacion_id=int(habitacion_value),
                trabajador_id=int(trabajador_value),
                fecha_ingreso=fecha_ingreso,
                fecha_salida=fecha_salida
            )
            page.snack_bar = ft.SnackBar(ft.Text("Reserva actualizada exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            # Refrescar la lista de reservas
            gestionar_reservas_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al actualizar reserva"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: dialog.close())]
            )
            page.dialog.open = True
            page.update()

    def eliminar_reserva(page: ft.Page, reserva_id):
        if reserva_controller.eliminar_reserva(reserva_id):
            page.snack_bar = ft.SnackBar(ft.Text("Reserva eliminada exitosamente"))
            page.snack_bar.open = True
            page.update()
            gestionar_reservas_view(page)
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("Error al eliminar reserva"))
            page.dialog.open = True
            page.update()

    def crear_editar_reserva_form(reserva=None):
        """Crea el formulario para crear o editar una reserva."""
        usuario_controller = UsuarioController()
        habitacion_controller = HabitacionController()
        hotel_controller = HotelController()

        # Obtener clientes activos
        clientes = usuario_controller.obtener_usuarios()
        clientes = [c for c in clientes if c.rol == "cliente" and c.activo]
        cliente_dropdown = ft.Dropdown(
            label="Cliente",
            options=[ft.dropdown.Option(f"{c.id} - {c.nombre}") for c in clientes],
            value=f"{reserva.cliente_id} - {usuario_controller.obtener_usuario_por_id(reserva.cliente_id).nombre}" if reserva else None
        )

        # Obtener habitaciones disponibles
        habitaciones = habitacion_controller.obtener_disponibles()
        habitacion_dropdown = ft.Dropdown(
            label="Habitación",
            options=[ft.dropdown.Option(f"{h.id} - N°{h.numero} ({hotel_controller.obtener_hotel_por_id(h.hotel_id).nombre})") for h in habitaciones],
            value=f"{reserva.habitacion_id} - N°{habitacion_controller.obtener_habitacion_por_id(reserva.habitacion_id).numero}" if reserva else None
        )

        # Obtener trabajadores activos
        trabajadores = usuario_controller.obtener_usuarios()
        trabajadores = [t for t in trabajadores if t.rol == "trabajador" and t.activo]
        trabajador_dropdown = ft.Dropdown(
            label="Trabajador",
            options=[ft.dropdown.Option(f"{t.id} - {t.nombre}") for t in trabajadores],
            value=f"{reserva.trabajador_id} - {usuario_controller.obtener_usuario_por_id(reserva.trabajador_id).nombre}" if reserva else None
        )

        fecha_ingreso_field = ft.DatePicker(label="Fecha de Ingreso", value=reserva.fecha_ingreso if reserva else None)
        fecha_salida_field = ft.DatePicker(label="Fecha de Salida", value=reserva.fecha_salida if reserva else None)

        form = ft.Column([
            cliente_dropdown,
            habitacion_dropdown,
            trabajador_dropdown,
            fecha_ingreso_field,
            fecha_salida_field
        ], spacing=10)

        return form

    # Botón para crear nueva reserva
    crear_reserva_button = ft.ElevatedButton("Crear Nueva Reserva", on_click=abrir_crear_reserva)

    # Añadimos el botón de crear reserva arriba de la lista
    reservas_view = ft.Column([
        ft.Text("Gestión de Reservas", style="headlineMedium"),
        crear_reserva_button,
        reservas_list
    ], scroll="auto")

    return reservas_view
