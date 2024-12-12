# views/cliente_dashboard/reserva/reserva_views.py

import flet as ft  # type: ignore
from controllers.reservation_controller import ReservationController
from controllers.room_controller import RoomController
from views.shared.back_button import back_button

def reserva_list_cliente_view(page: ft.Page, usuario):
    r_controller = ReservationController()
    reservations = r_controller.get_reservations_by_client(usuario.id)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Habitación ID")),
            ft.DataColumn(ft.Text("Trabajador ID")),
            ft.DataColumn(ft.Text("Fecha Ingreso")),
            ft.DataColumn(ft.Text("Fecha Salida")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )

    def refrescar():
        tabla.rows.clear()
        reservas = r_controller.get_reservations_by_client(usuario.id)
        for r in reservas:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(r.id))),
                        ft.DataCell(ft.Text(str(r.room_id))),
                        ft.DataCell(ft.Text(str(r.worker_id))),
                        ft.DataCell(ft.Text(str(r.check_in_date))),
                        ft.DataCell(ft.Text(str(r.check_out_date))),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, rid=r.id: cancelar(rid))
                            ])
                        )
                    ]
                )
            )
        page.update()

    def crear(e):
        page.views.append(reserva_create_cliente_view(page, usuario))
        page.go("/client/reservas/crear")
        page.update()

    def cancelar(rid):
        r_controller.delete_reservation(rid)
        refrescar()

    refrescar()

    return ft.View(
        "/client/reservas",
        [
            back_button(page),
            ft.Text("Mis Reservas (Cliente)", style="titleLarge"),
            ft.ElevatedButton("Crear Reserva", on_click=crear),
            tabla
        ]
    )

def reserva_create_cliente_view(page: ft.Page, usuario):
    r_controller = ReservationController()
    room_controller = RoomController()

    # Asumimos que el cliente elige una habitación "Available"
    available_rooms = room_controller.get_available_rooms()
    room_opciones = [ft.dropdown.Option(text=f"Num:{r.number}", key=str(r.id)) for r in available_rooms]

    # El trabajador se asigna automáticamente o el cliente no tiene control sobre el trabajador,
    # asumamos que el cliente no lo elige.
    # Podríamos tener un dropdown vacío o asignar un worker_id por defecto si tienes lógica en el servidor.

    # Por simplicidad no pedimos worker_id (asumimos que el servidor lo asigna, o hay un default)
    # Si necesitas que el cliente elija un trabajador, deberás agregar las opciones correspondientes.

    habitacion_dd = ft.Dropdown(label="Habitación", options=room_opciones)
    fecha_ingreso = ft.TextField(label="Fecha Ingreso (YYYY-MM-DD)")
    fecha_salida = ft.TextField(label="Fecha Salida (YYYY-MM-DD)")

    def guardar(e):
        # Asignar un worker_id por defecto, por ejemplo 2, o busca lógica en tu modelo
        # Aquí pondremos worker_id=2 como ejemplo
        worker_id = 2  
        r_controller.create_reservation(usuario.id, int(habitacion_dd.value), worker_id, fecha_ingreso.value, fecha_salida.value)
        page.views.pop()
        page.views[-1] = reserva_list_cliente_view(page, usuario)
        page.update()

    return ft.View(
        "/client/reservas/crear",
        [
            back_button(page),
            ft.Text("Crear Reserva (Cliente)", style="titleLarge"),
            habitacion_dd,
            fecha_ingreso,
            fecha_salida,
            ft.ElevatedButton("Guardar", on_click=guardar)
        ]
    )
