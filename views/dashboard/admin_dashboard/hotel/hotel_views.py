import flet as ft  # type: ignore
from controllers.hotel_controller import HotelController
from views.shared.back_button import back_button

def hotel_list_view(page: ft.Page):
    controller = HotelController()

    hoteles = controller.get_hotels()
    tabla_hoteles = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def refrescar():
        tabla_hoteles.rows.clear()
        for h in controller.get_hotels():
            tabla_hoteles.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(h.id))),
                        ft.DataCell(ft.Text(h.name)),
                        ft.DataCell(ft.Text(h.address)),
                        ft.DataCell(ft.Text(h.phone)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, hid=h.id: editar_hotel(hid)),
                                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, hid=h.id: eliminar_hotel(hid))
                            ])
                        )
                    ]
                )
            )
        page.update()

    def editar_hotel(hotel_id):
        page.views.append(hotel_edit_view(page, hotel_id))
        page.go("/admin/hoteles/editar")
        page.update()

    def eliminar_hotel(hotel_id):
        controller.delete_hotel(hotel_id)
        refrescar()

    def crear_hotel(e):
        page.views.append(hotel_create_view(page))
        page.go("/admin/hoteles/crear")
        page.update()

    refrescar()

    return ft.View(
        "/admin/hoteles",
        [
            back_button(page),
            ft.Text("Listado de Hoteles", style="titleLarge"),
            ft.ElevatedButton("Crear Hotel", on_click=crear_hotel),
            tabla_hoteles
        ]
    )

def hotel_create_view(page: ft.Page):
    controller = HotelController()

    nombre = ft.TextField(label="Nombre")
    direccion = ft.TextField(label="Dirección")
    telefono = ft.TextField(label="Teléfono")

    def guardar(e):
        controller.create_hotel(nombre.value, direccion.value, telefono.value)
        page.views.pop()  # Solo un pop
        # Refrescar la lista en la vista anterior
        page.views[-1] = hotel_list_view(page)
        page.update()

    return ft.View(
        "/admin/hoteles/crear",
        [
            back_button(page),
            ft.Text("Crear Hotel", style="titleLarge"),
            nombre, direccion, telefono,
            ft.ElevatedButton("Guardar", on_click=guardar)
        ]
    )

def hotel_edit_view(page: ft.Page, hotel_id):
    controller = HotelController()
    hotel = controller.get_hotel_by_id(hotel_id)
    if not hotel:
        return ft.View("/admin/hoteles/editar", [ft.Text("Hotel no encontrado")])

    nombre = ft.TextField(label="Nombre", value=hotel.name)
    direccion = ft.TextField(label="Dirección", value=hotel.address)
    telefono = ft.TextField(label="Teléfono", value=hotel.phone)

    def actualizar(e):
        controller.update_hotel(hotel_id, name=nombre.value, address=direccion.value, phone=telefono.value)
        page.views.pop()  # Solo un pop
        # Refrescar la lista en la vista anterior
        page.views[-1] = hotel_list_view(page)
        page.update()

    return ft.View(
        "/admin/hoteles/editar",
        [
            back_button(page),
            ft.Text("Editar Hotel", style="titleLarge"),
            nombre, direccion, telefono,
            ft.ElevatedButton("Actualizar", on_click=actualizar)
        ]
    )
