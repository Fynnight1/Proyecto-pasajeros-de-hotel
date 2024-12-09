# vista/cliente_dashboard.py

import flet as ft
from controlador.reserva_controller import ReservaController
from controlador.habitacion_controller import HabitacionController
from controlador.hotel_controller import HotelController
from controlador.usuario_controller import UsuarioController

def cliente_dashboard(page: ft.Page, usuario):
    reserva_controller = ReservaController()
    habitacion_controller = HabitacionController()
    hotel_controller = HotelController()
    usuario_controller = UsuarioController()

    cliente_id = usuario.id

    # Crear una sección de contenido dinámica
    content = ft.Container()

    def navigate_to(view_func):
        """Actualiza la sección de contenido con la vista correspondiente."""
        content.content = view_func(page)
        page.update()

    # Funciones para mostrar las diferentes vistas
    def crear_reserva(e):
        navigate_to(crear_reserva_view)

    def ver_reservas(e):
        navigate_to(ver_reservas_view)

    def elegir_hotel_view(page: ft.Page):
        hoteles = hotel_controller.obtener_hoteles()
        hoteles_list = ft.Column(scroll="auto")
        hoteles_list.controls.append(
            ft.Row([
                ft.Text("ID", weight="bold", width=50),
                ft.Text("Nombre", weight="bold", width=150),
                ft.Text("Dirección", weight="bold", width=200),
                ft.Text("Teléfono", weight="bold", width=100),
                ft.Text("Acciones", weight="bold", width=150)
            ])
        )
        for hotel in hoteles:
            hoteles_list.controls.append(
                ft.Row([
                    ft.Text(str(hotel.id), width=50),
                    ft.Text(hotel.nombre, width=150),
                    ft.Text(hotel.direccion, width=200),
                    ft.Text(hotel.telefono, width=100),
                    ft.Row([
                        ft.IconButton(ft.icons.VISIBILITY, on_click=lambda e, hid=hotel.id: ver_habitaciones_hotel(hid)),
                    ], width=150)
                ])
            )
        
        return ft.Column([
            ft.Text("Hoteles Disponibles", style="headlineMedium"),
            hoteles_list
        ], scroll="auto")

    def ver_habitaciones_hotel(hotel_id):
        habitaciones = habitacion_controller.obtener_habitaciones_por_hotel(hotel_id)
        habitaciones_disponibles = [h for h in habitaciones if h.estado.lower() == "disponible"]

        habitaciones_list = ft.Column(scroll="auto")
        habitaciones_list.controls.append(
            ft.Row([
                ft.Text("ID", weight="bold", width=50),
                ft.Text("Número", weight="bold", width=100),
                ft.Text("Piso", weight="bold", width=50),
                ft.Text("Estado", weight="bold", width=150),
                ft.Text("Acciones", weight="bold", width=150)
            ])
        )
        for h in habitaciones_disponibles:
            habitaciones_list.controls.append(
                ft.Row([
                    ft.Text(str(h.id), width=50),
                    ft.Text(str(h.numero), width=100),
                    ft.Text(str(h.piso), width=50),
                    ft.Text(h.estado, width=150),
                    ft.Row([
                        ft.IconButton(ft.icons.ADD, on_click=lambda e, hid=h.id: seleccionar_habitacion(hid)),
                    ], width=150)
                ])
            )
        
        def seleccionar_habitacion(habitacion_id):
            # Implementar la lógica para seleccionar una habitación para la reserva
            habitacion = habitacion_controller.obtener_habitacion_por_id(habitacion_id)
            if not habitacion:
                page.snack_bar = ft.SnackBar(ft.Text("Habitación no encontrada"))
                page.snack_bar.open = True
                page.update()
                return

            dialog = ft.AlertDialog(
                title=ft.Text(f"Seleccionar Habitación ID: {habitacion_id}"),
                content=crear_reserva_form(habitacion_id),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                    ft.ElevatedButton("Crear Reserva", on_click=lambda e: crear_reserva_action(dialog, habitacion_id))
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

        return ft.Column([
            ft.Text("Habitaciones Disponibles", style="headlineMedium"),
            habitaciones_list
        ], scroll="auto")

    def crear_reserva_view(page: ft.Page):
        navigate_to(elegir_hotel_view)

    def ver_reservas_view(page: ft.Page):
        reservas = reserva_controller.obtener_reservas_por_cliente(cliente_id)
        reservas_list = ft.Column(scroll="auto")
        reservas_list.controls.append(
            ft.Row([
                ft.Text("ID", weight="bold", width=50),
                ft.Text("Habitación ID", weight="bold", width=100),
                ft.Text("Trabajador ID", weight="bold", width=100),
                ft.Text("Ingreso", weight="bold", width=100),
                ft.Text("Salida", weight="bold", width=100),
                ft.Text("Acciones", weight="bold", width=150)
            ])
        )
        for r in reservas:
            reservas_list.controls.append(
                ft.Row([
                    ft.Text(str(r.id), width=50),
                    ft.Text(str(r.habitacion_id), width=100),
                    ft.Text(str(r.trabajador_id), width=100),
                    ft.Text(str(r.fecha_ingreso), width=100),
                    ft.Text(str(r.fecha_salida), width=100),
                    ft.Row([
                        ft.IconButton(ft.icons.VISIBILITY, on_click=lambda e, rid=r.id: ver_detalle_reserva(rid)),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, rid=r.id: cancelar_reserva(rid))
                    ], width=150)
                ])
            )
        
        def ver_detalle_reserva(reserva_id):
            reserva = reserva_controller.obtener_reserva_por_id(reserva_id)
            if not reserva:
                page.snack_bar = ft.SnackBar(ft.Text("Reserva no encontrada"))
                page.snack_bar.open = True
                page.update()
                return

            dialog = ft.AlertDialog(
                title=ft.Text(f"Detalles de Reserva ID: {reserva_id}"),
                content=ft.Column([
                    ft.Text(f"Cliente ID: {reserva.cliente_id}"),
                    ft.Text(f"Habitación ID: {reserva.habitacion_id}"),
                    ft.Text(f"Trabajador ID: {reserva.trabajador_id}"),
                    ft.Text(f"Fecha de Ingreso: {reserva.fecha_ingreso}"),
                    ft.Text(f"Fecha de Salida: {reserva.fecha_salida}"),
                ]),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: dialog.close())],
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

        def cancelar_reserva(reserva_id):
            if reserva_controller.eliminar_reserva(reserva_id):
                page.snack_bar = ft.SnackBar(ft.Text("Reserva cancelada exitosamente"))
                page.snack_bar.open = True
                page.update()
                ver_reservas_view(page)
            else:
                page.dialog = ft.AlertDialog(title=ft.Text("Error al cancelar reserva"))
                page.dialog.open = True
                page.update()

        def crear_reserva_form(habitacion_id):
            global fecha_ingreso_field, fecha_salida_field
            fecha_ingreso_field = ft.DatePicker(label="Fecha de Ingreso")
            fecha_salida_field = ft.DatePicker(label="Fecha de Salida")

            form = ft.Column([
                fecha_ingreso_field,
                fecha_salida_field
            ])

            return form

        def crear_reserva_action(dialog, habitacion_id):
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
                reserva_controller.crear_reserva(cliente_id, habitacion_id, usuario.id, fecha_ingreso, fecha_salida)
                page.snack_bar = ft.SnackBar(ft.Text("Reserva creada exitosamente"))
                page.snack_bar.open = True
                dialog.close()
                page.update()
            except Exception as ex:
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Error al crear reserva"),
                    content=ft.Text(str(ex)),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())]
                )
                page.dialog.open = True
                page.update()

        def crear_reserva_form(habitacion_id=None):
            global fecha_ingreso_field, fecha_salida_field
            fecha_ingreso_field = ft.DatePicker(label="Fecha de Ingreso")
            fecha_salida_field = ft.DatePicker(label="Fecha de Salida")

            form = ft.Column([
                fecha_ingreso_field,
                fecha_salida_field
            ])

            return form

        # Botones para las acciones del cliente
        buttons = [
            ft.ElevatedButton("Crear Reserva", on_click=crear_reserva),
            ft.ElevatedButton("Ver Mis Reservas", on_click=ver_reservas),
            ft.ElevatedButton("Elegir Hotel", on_click=elegir_hotel_view),
        ]

        # Barra de navegación del cliente
        nav_bar = ft.Row(
            buttons,
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        # Layout principal del dashboard del cliente con barra de navegación y contenido dinámico
        page.add(
            ft.Column(
                [
                    ft.Text(f"Bienvenido, {usuario.nombre} (Cliente)", style="headlineLarge"),
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
        elegir_hotel_view(page)
