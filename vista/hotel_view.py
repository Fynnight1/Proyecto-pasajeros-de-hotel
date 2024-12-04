import flet as ft
from controlador.hotel_controller import HotelController

def hotel_view(page: ft.Page):
    controller = HotelController()
    
    def cargar_datos():
        hoteles = controller.obtener_hoteles()
        data_rows = []
        for h in hoteles:
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(h.id))),
                        ft.DataCell(ft.Text(h.nombre)),
                        ft.DataCell(ft.Text(h.direccion)),
                        ft.DataCell(ft.Text(h.telefono)),
                    ]
                )
            )
        tabla.rows = data_rows
        page.update()
    
    def agregar_hotel(e):
        controller.crear_hotel(
            nombre=nombre_field.value,
            direccion=direccion_field.value,
            telefono=telefono_field.value
        )
        cargar_datos()
    
    # Campos de entrada
    nombre_field = ft.TextField(label="Nombre")
    direccion_field = ft.TextField(label="Dirección")
    telefono_field = ft.TextField(label="Teléfono")
    
    # Botones
    boton_agregar = ft.ElevatedButton(text="Agregar Hotel", on_click=agregar_hotel)
    
    # Tabla de datos
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Teléfono")),
        ],
        rows=[]
    )
    
    cargar_datos()
    
    # Layout
    page.add(
        ft.Column([
            nombre_field,
            ft.Row([direccion_field, telefono_field]),
            boton_agregar,
            tabla
        ])
    )