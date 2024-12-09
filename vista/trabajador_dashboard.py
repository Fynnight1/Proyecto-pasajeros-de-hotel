# vista/trabajador_dashboard.py

import flet as ft
from controlador.usuario_controller import UsuarioController
from controlador.reserva_controller import ReservaController
from controlador.habitacion_controller import HabitacionController
from controlador.hotel_controller import HotelController

def trabajador_dashboard(page: ft.Page, usuario):
    reserva_controller = ReservaController()
    habitacion_controller = HabitacionController()
    hotel_controller = HotelController()
    usuario_controller = UsuarioController()

    # Crear una sección de contenido dinámica
    content = ft.Container()

    def navigate_to(view_func):
        """Actualiza la sección de contenido con la vista correspondiente."""
        content.content = view_func(page)
        page.update()

    # Funciones para mostrar las diferentes vistas
    def crear_reserva(e):
        navigate_to(crear_reserva_view)

    def editar_reserva(e):
        navigate_to(editar_reserva_view)

    def cancelar_reserva(e):
        navigate_to(cancelar_reserva_view)

    def ver_hoteles(e):
        navigate_to(ver_hoteles_view)

    def ver_habitaciones(e):
        navigate_to(ver_habitaciones_view)

    # Vistas para Trabajador
    def crear_reserva_view(page: ft.Page):
        dialog = ft.AlertDialog(
            title=ft.Text("Crear Reserva"),
            content=crear_reserva_form(),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Crear", on_click=lambda e: crear_reserva_action(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def editar_reserva_view(page: ft.Page):
        reservas = reserva_controller.obtener_reservas()
        if not reservas:
            page.snack_bar = ft.SnackBar(ft.Text("No hay reservas para editar"))
            page.snack_bar.open = True
            page.update()
            return

        reserva_dropdown = ft.Dropdown(
            label="Seleccionar Reserva",
            options=[ft.dropdown.Option(f"ID {r.id} - Cliente {r.cliente_id}") for r in reservas],
            value=None
        )

        fecha_ingreso_field = ft.DatePicker(label="Nueva Fecha de Ingreso")
        fecha_salida_field = ft.DatePicker(label="Nueva Fecha de Salida")

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Reserva"),
            content=ft.Column([
                reserva_dropdown,
                fecha_ingreso_field,
                fecha_salida_field
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Guardar", on_click=lambda e: editar_reserva_action(dialog, reserva_dropdown.value))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def cancelar_reserva_view(page: ft.Page):
        reservas = reserva_controller.obtener_reservas()
        if not reservas:
            page.snack_bar = ft.SnackBar(ft.Text("No hay reservas para cancelar"))
            page.snack_bar.open = True
            page.update()
            return

        reserva_dropdown = ft.Dropdown(
            label="Seleccionar Reserva",
            options=[ft.dropdown.Option(f"ID {r.id} - Cliente {r.cliente_id}") for r in reservas],
            value=None
        )

        dialog = ft.AlertDialog(
            title=ft.Text("Cancelar Reserva"),
            content=ft.Column([
                reserva_dropdown
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Cancelar Reserva", on_click=lambda e: cancelar_reserva_action(dialog, reserva_dropdown.value))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def ver_hoteles_view(page: ft.Page):
        hoteles = hotel_controller.obtener_hoteles()
        hoteles_list = ft.Column(scroll="auto")
        hoteles_list.controls.append(
            ft.Row([
                ft.Text("ID", weight="bold", width=50),
                ft.Text("Nombre", weight="bold", width=150),
                ft.Text("Dirección", weight="bold", width=200),
                ft.Text("Teléfono", weight="bold", width=100),
            ])
        )
        for hotel in hoteles:
            hoteles_list.controls.append(
                ft.Row([
                    ft.Text(str(hotel.id), width=50),
                    ft.Text(hotel.nombre, width=150),
                    ft.Text(hotel.direccion, width=200),
                    ft.Text(hotel.telefono, width=100),
                ])
            )

        return ft.Column([
            ft.Text("Hoteles Disponibles", style="headlineMedium"),
            hoteles_list
        ], scroll="auto")

    def ver_habitaciones_view(page: ft.Page):
        habitaciones = habitacion_controller.obtener_habitaciones_disponibles()
        habitaciones_list = ft.Column(scroll="auto")
        habitaciones_list.controls.append(
            ft.Row([
                ft.Text("ID", weight="bold", width=50),
                ft.Text("Número", weight="bold", width=100),
                ft.Text("Piso", weight="bold", width=50),
                ft.Text("Estado", weight="bold", width=150),
                ft.Text("Hotel", weight="bold", width=100),
            ])
        )
        for h in habitaciones:
            hotel = hotel_controller.obtener_hotel_por_id(h.hotel_id)
            hotel_nombre = hotel.nombre if hotel else "N/A"
            habitaciones_list.controls.append(
                ft.Row([
                    ft.Text(str(h.id), width=50),
                    ft.Text(str(h.numero), width=100),
                    ft.Text(str(h.piso), width=50),
                    ft.Text(h.estado, width=150),
                    ft.Text(hotel_nombre, width=100),
                ])
            )

        return ft.Column([
            ft.Text("Habitaciones Disponibles", style="headlineMedium"),
            habitaciones_list
        ], scroll="auto")

    def crear_reserva_form():
        global cliente_dropdown, habitacion_dropdown, fecha_ingreso_field, fecha_salida_field

        # Obtener clientes activos
        clientes = usuario_controller.obtener_usuarios()
        clientes = [c for c in clientes if c.rol == "cliente" and c.activo]
        cliente_dropdown = ft.Dropdown(
            label="Cliente",
            options=[ft.dropdown.Option(f"{c.id} - {c.nombre}") for c in clientes],
            value=None
        )

        # Obtener habitaciones disponibles
        habitaciones = habitacion_controller.obtener_habitaciones_disponibles()
        habitacion_dropdown = ft.Dropdown(
            label="Habitación",
            options=[ft.dropdown.Option(f"{h.id} - N°{h.numero} ({h.hotel.nombre})") for h in habitaciones],
            value=None
        )

        fecha_ingreso_field = ft.DatePicker(label="Fecha de Ingreso")
        fecha_salida_field = ft.DatePicker(label="Fecha de Salida")

        form = ft.Column([
            cliente_dropdown,
            habitacion_dropdown,
            fecha_ingreso_field,
            fecha_salida_field
        ])

        return form

    def crear_reserva_action(dialog):
        cliente_value = cliente_dropdown.value.split(" - ")[0] if cliente_dropdown.value else None
        habitacion_value = habitacion_dropdown.value.split(" - ")[0] if habitacion_dropdown.value else None
        fecha_ingreso = fecha_ingreso_field.value
        fecha_salida = fecha_salida_field.value

        if not cliente_value or not habitacion_value or not fecha_ingreso or not fecha_salida:
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
            reserva_controller.crear_reserva(int(cliente_value), int(habitacion_value), int(usuario.id), fecha_ingreso, fecha_salida)
            page.snack_bar = ft.SnackBar(ft.Text("Reserva creada exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            # Opcional: refrescar la vista de reservas
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al crear reserva"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: dialog.close())]
            )
            page.dialog.open = True
            page.update()

    def editar_reserva_action(dialog, reserva_id):
        fecha_ingreso = fecha_ingreso_field.value
        fecha_salida = fecha_salida_field.value

        if not fecha_ingreso or not fecha_salida:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todas las fechas"))
            page.snack_bar.open = True
            page.update()
            return

        if fecha_salida <= fecha_ingreso:
            page.snack_bar = ft.SnackBar(ft.Text("La fecha de salida debe ser posterior a la de ingreso"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            reserva_controller.actualizar_reserva(reserva_id, fecha_ingreso=fecha_ingreso, fecha_salida=fecha_salida)
            page.snack_bar = ft.SnackBar(ft.Text("Reserva actualizada exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            gestionar_reservas_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al actualizar reserva"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: dialog.close())]
            )
            page.dialog.open = True
            page.update()

    def cancelar_reserva_action(dialog, reserva_id):
        try:
            reserva_controller.eliminar_reserva(reserva_id)
            page.snack_bar = ft.SnackBar(ft.Text("Reserva cancelada exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            gestionar_reservas_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al cancelar reserva"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: dialog.close())]
            )
            page.dialog.open = True
            page.update()

    def crear_editar_reserva_form(reserva=None):
        """Crea el formulario para crear o editar una reserva."""
        global cliente_dropdown, habitacion_dropdown, trabajador_dropdown, fecha_ingreso_field, fecha_salida_field

        # Obtener clientes activos
        clientes = usuario_controller.obtener_usuarios()
        clientes = [c for c in clientes if c.rol == "cliente" and c.activo]
        cliente_dropdown = ft.Dropdown(
            label="Cliente",
            options=[ft.dropdown.Option(f"{c.id} - {c.nombre}") for c in clientes],
            value=f"{reserva.cliente_id} - {reserva.cliente.nombre}" if reserva else None
        )

        # Obtener habitaciones disponibles
        habitaciones = habitacion_controller.obtener_habitaciones_disponibles()
        habitacion_dropdown = ft.Dropdown(
            label="Habitación",
            options=[ft.dropdown.Option(f"{h.id} - N°{h.numero} ({h.hotel.nombre})") for h in habitaciones],
            value=f"{reserva.habitacion_id} - N°{reserva.habitacion.numero}" if reserva else None
        )

        # Obtener trabajadores activos
        trabajadores = usuario_controller.obtener_usuarios()
        trabajadores = [t for t in trabajadores if t.rol == "trabajador" and t.activo]
        trabajador_dropdown = ft.Dropdown(
            label="Trabajador",
            options=[ft.dropdown.Option(f"{t.id} - {t.nombre}") for t in trabajadores],
            value=f"{reserva.trabajador_id} - {reserva.trabajador.nombre}" if reserva else None
        )

        fecha_ingreso_field = ft.DatePicker(label="Fecha de Ingreso", value=reserva.fecha_ingreso if reserva else None)
        fecha_salida_field = ft.DatePicker(label="Fecha de Salida", value=reserva.fecha_salida if reserva else None)

        form = ft.Column([
            cliente_dropdown,
            habitacion_dropdown,
            trabajador_dropdown,
            fecha_ingreso_field,
            fecha_salida_field
        ])

        return form

    def gestionar_reservas_view(page: ft.Page):
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
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, rid=r.id: abrir_editar_reserva(rid)),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, rid=r.id: eliminar_reserva(rid))
                    ], width=150)
                ])
            )
        
        def abrir_editar_reserva(reserva_id):
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
                    ft.ElevatedButton("Guardar", on_click=lambda e: editar_reserva_action(dialog, reserva_id))
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

        def eliminar_reserva(reserva_id):
            if reserva_controller.eliminar_reserva(reserva_id):
                page.snack_bar = ft.SnackBar(ft.Text("Reserva eliminada exitosamente"))
                page.snack_bar.open = True
                page.update()
                gestionar_reservas_view(page)
            else:
                page.dialog = ft.AlertDialog(title=ft.Text("Error al eliminar reserva"))
                page.dialog.open = True
                page.update()

        # Layout principal del dashboard con barra de navegación y contenido dinámico
        nav_bar = ft.Row(
            [
                ft.ElevatedButton("Crear Reserva", on_click=crear_reserva),
                ft.ElevatedButton("Editar Reserva", on_click=editar_reserva),
                ft.ElevatedButton("Cancelar Reserva", on_click=cancelar_reserva),
                ft.ElevatedButton("Ver Hoteles", on_click=ver_hoteles),
                ft.ElevatedButton("Ver Habitaciones Disponibles", on_click=ver_habitaciones),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        # Layout principal del dashboard con barra de navegación y contenido dinámico
        page.add(
            ft.Column(
                [
                    ft.Text(f"Bienvenido, {usuario.nombre} (Trabajador)", style="headlineLarge"),
                    nav_bar,
                    ft.Divider(),
                    content
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=20
            )
        )

        # Cargar una vista por defecto al iniciar el dashboard
        ver_hoteles_view(page)
