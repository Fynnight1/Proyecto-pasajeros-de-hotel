import flet as ft  # type: ignore
from controllers.reservation_controller import ReservationController
from controllers.user_controller import UserController
from controllers.room_controller import RoomController
from views.shared.back_button import back_button

def reserva_list_view(page: ft.Page):
    controller = ReservationController()

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Cliente ID")),
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
        reservas = controller.get_reservations()
        for r in reservas:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(r.id))),
                        ft.DataCell(ft.Text(str(r.client_id))),
                        ft.DataCell(ft.Text(str(r.room_id))),
                        ft.DataCell(ft.Text(str(r.worker_id))),
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
        page.views.append(reserva_create_view(page))
        page.go("/admin/reservas/crear")
        page.update()

    def editar(reserva_id):
        page.views.append(reserva_edit_view(page, reserva_id))
        page.go("/admin/reservas/editar")
        page.update()

    def eliminar(reserva_id):
        controller.delete_reservation(reserva_id)
        refrescar()

    refrescar()

    return ft.View(
        "/admin/reservas",
        [
            back_button(page),
            ft.Text("Listado de Reservas", style="titleLarge"),
            ft.ElevatedButton("Crear Reserva", on_click=crear),
            tabla
        ]
    )

def reserva_create_view(page: ft.Page):
    r_controller = ReservationController()
    u_controller = UserController()
    h_controller = RoomController()

    usuarios = u_controller.get_users()
    clientes = [u for u in usuarios if u.role == 'client']
    trabajadores = [u for u in usuarios if u.role == 'worker']

    habs = h_controller.get_available_rooms()

    cliente_opciones = [ft.dropdown.Option(text=c.name, key=str(c.id)) for c in clientes]
    habitacion_opciones = [ft.dropdown.Option(text=f"Num:{h.number}", key=str(h.id)) for h in habs]
    trabajador_opciones = [ft.dropdown.Option(text=t.name, key=str(t.id)) for t in trabajadores]

    cliente_dd = ft.Dropdown(label="Cliente", options=cliente_opciones)
    habitacion_dd = ft.Dropdown(label="Habitación", options=habitacion_opciones)
    trabajador_dd = ft.Dropdown(label="Trabajador", options=trabajador_opciones)
    fecha_ingreso = ft.TextField(label="Fecha Ingreso (YYYY-MM-DD)")
    fecha_salida = ft.TextField(label="Fecha Salida (YYYY-MM-DD)")

    def guardar(e):
        r_controller.create_reservation(
            int(cliente_dd.value),
            int(habitacion_dd.value),
            int(trabajador_dd.value),
            fecha_ingreso.value,
            fecha_salida.value
        )
        page.views.pop()
        page.views[-1] = reserva_list_view(page)
        page.update()

    return ft.View(
        "/admin/reservas/crear",
        [
            back_button(page),
            ft.Text("Crear Reserva", style="titleLarge"),
            cliente_dd,
            habitacion_dd,
            trabajador_dd,
            fecha_ingreso,
            fecha_salida,
            ft.ElevatedButton("Guardar", on_click=guardar)
        ]
    )

def reserva_edit_view(page: ft.Page, reserva_id):
    r_controller = ReservationController()
    reserva = r_controller.get_reservation_by_id(reserva_id)
    if not reserva:
        return ft.View("/admin/reservas/editar", [ft.Text("Reserva no encontrada")])

    fecha_ingreso = ft.TextField(label="Fecha Ingreso (YYYY-MM-DD)", value=str(reserva.check_in_date))
    fecha_salida = ft.TextField(label="Fecha Salida (YYYY-MM-DD)", value=str(reserva.check_out_date))

    def actualizar(e):
        r_controller.update_reservation(reserva_id, check_in_date=fecha_ingreso.value, check_out_date=fecha_salida.value)
        page.views.pop()
        page.views[-1] = reserva_list_view(page)
        page.update()

    return ft.View(
        "/admin/reservas/editar",
        [
            back_button(page),
            ft.Text("Editar Reserva", style="titleLarge"),
            fecha_ingreso,
            fecha_salida,
            ft.ElevatedButton("Actualizar", on_click=actualizar)
        ]
    )
