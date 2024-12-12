# views/worker_dashboard/reservation/reservation_views.py

import flet as ft  # type: ignore
from controllers.reservation_controller import ReservationController
from controllers.user_controller import UserController
from controllers.room_controller import RoomController
from views.shared.back_button import back_button

def reserva_list_trabajador_view(page: ft.Page, usuario):
    r_controller = ReservationController()

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Cliente ID")),
            ft.DataColumn(ft.Text("Habitación ID")),
            ft.DataColumn(ft.Text("Fecha Ingreso")),
            ft.DataColumn(ft.Text("Fecha Salida")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )

    def refrescar():
        tabla.rows.clear()
        # Aquí puedes filtrar las reservas según alguna lógica para el trabajador
        reservas = r_controller.get_reservations()
        for r in reservas:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(r.id))),
                        ft.DataCell(ft.Text(str(r.client_id))),
                        ft.DataCell(ft.Text(str(r.room_id))),
                        ft.DataCell(ft.Text(str(r.check_in_date))),
                        ft.DataCell(ft.Text(str(r.check_out_date))),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, rid=r.id: editar(rid)),
                                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, rid=r.id: eliminar(rid))
                            ])
                        )
                    ]
                )
            )
        page.update()

    def crear(e):
        page.views.append(reserva_create_trabajador_view(page, usuario))
        page.go("/worker/reservas/crear")
        page.update()

    def editar(reserva_id):
        # Similar a admin, podrías crear una vista de edición
        # page.views.append(reserva_edit_trabajador_view(page, usuario, reserva_id))
        # page.go("/worker/reservas/editar")
        # page.update()
        pass

    def eliminar(reserva_id):
        r_controller.delete_reservation(reserva_id)
        refrescar()

    refrescar()

    return ft.View(
        "/worker/reservas",
        [
            back_button(page),
            ft.Text("Reservas (Trabajador)", style="titleLarge"),
            ft.ElevatedButton("Crear Reserva", on_click=crear),
            tabla
        ]
    )

def reserva_create_trabajador_view(page: ft.Page, usuario):
    r_controller = ReservationController()
    u_controller = UserController()
    h_controller = RoomController()

    usuarios = u_controller.get_users()
    clientes = [u for u in usuarios if u.role == 'client']
    habs = h_controller.get_available_rooms()

    cliente_opciones = [ft.dropdown.Option(text=c.name, key=str(c.id)) for c in clientes]
    habitacion_opciones = [ft.dropdown.Option(text=f"Num:{h.number}", key=str(h.id)) for h in habs]

    cliente_dd = ft.Dropdown(label="Cliente", options=cliente_opciones)
    habitacion_dd = ft.Dropdown(label="Habitación", options=habitacion_opciones)
    fecha_ingreso = ft.TextField(label="Fecha Ingreso (YYYY-MM-DD)")
    fecha_salida = ft.TextField(label="Fecha Salida (YYYY-MM-DD)")

    def guardar(e):
        # Asigna el worker_id = usuario.id, ya que el trabajador es quien crea la reserva
        r_controller.create_reservation(
            int(cliente_dd.value),
            int(habitacion_dd.value),
            usuario.id,
            fecha_ingreso.value,
            fecha_salida.value
        )
        page.views.pop()
        page.views[-1] = reserva_list_trabajador_view(page, usuario)
        page.update()

    return ft.View(
        "/worker/reservas/crear",
        [
            back_button(page),
            ft.Text("Crear Reserva (Trabajador)", style="titleLarge"),
            cliente_dd,
            habitacion_dd,
            fecha_ingreso,
            fecha_salida,
            ft.ElevatedButton("Guardar", on_click=guardar)
        ]
    )
