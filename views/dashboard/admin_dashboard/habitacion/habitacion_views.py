import flet as ft  # type: ignore
from controllers.room_controller import RoomController
from controllers.hotel_controller import HotelController
from views.shared.back_button import back_button

def habitacion_list_view(page: ft.Page):
    controller = RoomController()

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Número")),
            ft.DataColumn(ft.Text("Piso")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Hotel ID")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )

    def refrescar():
        tabla.rows.clear()
        habitaciones = controller.get_rooms()
        for hab in habitaciones:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(hab.id))),
                        ft.DataCell(ft.Text(str(hab.number))),
                        ft.DataCell(ft.Text(str(hab.floor))),
                        ft.DataCell(ft.Text(hab.status)),
                        ft.DataCell(ft.Text(str(hab.hotel_id))),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, hid=hab.id: editar(hid)),
                                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, hid=hab.id: eliminar(hid))
                            ])
                        )
                    ]
                )
            )
        page.update()

    def crear(e):
        page.views.append(habitacion_create_view(page))
        page.go("/admin/habitaciones/crear")
        page.update()

    def editar(hid):
        page.views.append(habitacion_edit_view(page, hid))
        page.go("/admin/habitaciones/editar")
        page.update()

    def eliminar(hid):
        controller.delete_room(hid)
        refrescar()

    refrescar()

    return ft.View(
        "/admin/habitaciones",
        [
            back_button(page),
            ft.Text("Listado de Habitaciones", style="titleLarge"),
            ft.ElevatedButton("Crear Habitación", on_click=crear),
            tabla
        ]
    )

def habitacion_create_view(page: ft.Page):
    controller = RoomController()
    hotel_controller = HotelController()
    hoteles = hotel_controller.get_hotels()

    # Crear opciones para el Dropdown
    hotel_opciones = [ft.dropdown.Option(text=h.name, key=str(h.id)) for h in hoteles]

    numero = ft.TextField(label="Número")
    piso = ft.TextField(label="Piso")
    estado = ft.TextField(label="Estado", value="Available")
    hotel_id = ft.Dropdown(label="Hotel", options=hotel_opciones)

    def guardar(e):
        controller.create_room(numero.value, int(piso.value), estado.value, int(hotel_id.value))  # hotel_id.value devuelve key como str
        page.views.pop()  # Volvemos a la lista
        # Refrescar la vista anterior
        page.views[-1] = habitacion_list_view(page)
        page.update()

    return ft.View(
        "/admin/habitaciones/crear",
        [
            back_button(page),
            ft.Text("Crear Habitación", style="titleLarge"),
            numero,
            piso,
            estado,
            hotel_id,
            ft.ElevatedButton("Guardar", on_click=guardar)
        ]
    )

def habitacion_edit_view(page: ft.Page, habitacion_id):
    controller = RoomController()
    hotel_controller = HotelController()
    hab = controller.get_room_by_id(habitacion_id)
    if not hab:
        return ft.View("/admin/habitaciones/editar", [ft.Text("Habitación no encontrada")])

    hoteles = hotel_controller.get_hotels()
    hotel_opciones = [ft.dropdown.Option(text=h.name, key=str(h.id)) for h in hoteles]

    numero = ft.TextField(label="Número", value=str(hab.number))
    piso = ft.TextField(label="Piso", value=str(hab.floor))
    estado = ft.TextField(label="Estado", value=hab.status)
    hotel_id = ft.Dropdown(label="Hotel", options=hotel_opciones, value=str(hab.hotel_id))

    def actualizar(e):
        controller.update_room(habitacion_id, number=numero.value, floor=int(piso.value), status=estado.value, hotel_id=int(hotel_id.value))
        page.views.pop()
        page.views[-1] = habitacion_list_view(page)
        page.update()

    return ft.View(
        "/admin/habitaciones/editar",
        [
            back_button(page),
            ft.Text("Editar Habitación", style="titleLarge"),
            numero,
            piso,
            estado,
            hotel_id,
            ft.ElevatedButton("Actualizar", on_click=actualizar)
        ]
    )
