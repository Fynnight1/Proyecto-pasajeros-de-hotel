import flet as ft
from controlador.trabajador_controller import TrabajadorController
from controlador.hotel_controller import HotelController

def trabajador_view(page: ft.Page):
    controller = TrabajadorController()
    hotel_controller = HotelController()
    
    def cargar_datos():
        trabajadores = controller.obtener_trabajadores()
        data_rows = []
        for t in trabajadores:
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(t.id))),
                        ft.DataCell(ft.Text(t.nombre)),
                        ft.DataCell(ft.Text(t.rut)),
                        ft.DataCell(ft.Text(t.direccion)),
                        ft.DataCell(ft.Text(t.telefono)),
                        ft.DataCell(ft.Text(str(t.hotel_id))),
                    ]
                )
            )
        tabla.rows = data_rows
        page.update()
    
    def agregar_trabajador(e):
        controller.crear_trabajador(
            nombre=nombre_field.value,
            rut=rut_field.value,
            direccion=direccion_field.value,
            telefono=telefono_field.value,
            hotel_id=int(hotel_dropdown.value)
        )
        cargar_datos()
    
    # Obtener lista de hoteles para el Dropdown
    hoteles = hotel_controller.obtener_hoteles()
    hotel_opciones = [ft.dropdown.Option(str(h.id), h.nombre) for h in hoteles]
    
    # Campos de entrada
    nombre_field = ft.TextField(label="Nombre")
    rut_field = ft.TextField(label="RUT")
    direccion_field = ft.TextField(label="Dirección")
    telefono_field = ft.TextField(label="Teléfono")
    hotel_dropdown = ft.Dropdown(label="Hotel", options=hotel_opciones)
    
    # Botones
    boton_agregar = ft.ElevatedButton(text="Agregar Trabajador", on_click=agregar_trabajador)
    
    # Tabla de datos
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("RUT")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Hotel ID")),
        ],
        rows=[]
    )
    
    cargar_datos()
    
    # Layout
    page.add(
        ft.Column([
            ft.Row([nombre_field, rut_field]),
            ft.Row([direccion_field, telefono_field]),
            hotel_dropdown,
            boton_agregar,
            tabla
        ])
    )