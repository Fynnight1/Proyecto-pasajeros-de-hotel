import flet as ft
from controlador.cliente_controller import ClienteController

def cliente_view(page: ft.Page):
    controller = ClienteController()
    
    def cargar_datos():
        clientes = controller.obtener_clientes()
        data_rows = []
        for c in clientes:
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c.id))),
                        ft.DataCell(ft.Text(c.nombre)),
                        ft.DataCell(ft.Text(c.rut)),
                        ft.DataCell(ft.Text(c.direccion)),
                        ft.DataCell(ft.Text(c.telefono)),
                    ]
                )
            )
        tabla.rows = data_rows
        page.update()
    
    def agregar_cliente(e):
        controller.crear_cliente(
            nombre=nombre_field.value,
            rut=rut_field.value,
            direccion=direccion_field.value,
            telefono=telefono_field.value
        )
        cargar_datos()
    
    # Campos de entrada
    nombre_field = ft.TextField(label="Nombre")
    rut_field = ft.TextField(label="RUT")
    direccion_field = ft.TextField(label="Dirección")
    telefono_field = ft.TextField(label="Teléfono")
    
    # Botones
    boton_agregar = ft.ElevatedButton(text="Agregar Cliente", on_click=agregar_cliente)
    
    # Tabla de datos
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("RUT")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Teléfono")),
        ],
        rows=[]
    )
    
    cargar_datos()
    
    # Layout
    page.add(
        ft.Column([
            ft.Row([nombre_field, rut_field]),
            ft.Row([direccion_field, telefono_field]),
            boton_agregar,
            tabla
        ])
    )