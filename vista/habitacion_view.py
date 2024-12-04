import flet as ft
from controlador.habitacion_controller import HabitacionController
from controlador.hotel_controller import HotelController

def habitacion_view(page: ft.Page):
    controller = HabitacionController()
    hotel_controller = HotelController()
    
    def cargar_datos():
        habitaciones = controller.obtener_habitaciones()
        data_rows = []
        for h in habitaciones:
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(h.id))),
                        ft.DataCell(ft.Text(str(h.numero))),
                        ft.DataCell(ft.Text(str(h.piso))),
                        ft.DataCell(ft.Text(h.estado)),
                        ft.DataCell(ft.Text(str(h.hotel_id))),
                    ]
                )
            )
        tabla.rows = data_rows
        page.update()
    
    def agregar_habitacion(e):
        controller.crear_habitacion(
            numero=int(numero_field.value),
            piso=int(piso_field.value),
            estado=estado_dropdown.value,
            hotel_id=int(hotel_dropdown.value)
        )
        cargar_datos()
    
    # Obtener lista de hoteles para el Dropdown
    hoteles = hotel_controller.obtener_hoteles()
    hotel_opciones = [ft.dropdown.Option(str(h.id), h.nombre) for h in hoteles]
    
    # Campos de entrada
    numero_field = ft.TextField(label="Número")
    piso_field = ft.TextField(label="Piso")
    estado_dropdown = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option("Disponible"),
            ft.dropdown.Option("Ocupada"),
        ]
    )
    hotel_dropdown = ft.Dropdown(
        label="Hotel",
        options=hotel_opciones
    )
    
    # Botones
    boton_agregar = ft.ElevatedButton(text="Agregar Habitación", on_click=agregar_habitacion)
    
    # Tabla de datos
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Número")),
            ft.DataColumn(ft.Text("Piso")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Hotel ID")),
        ],
        rows=[]
    )
    
    cargar_datos()
    
    # Layout
    page.add(
        ft.Column([
            ft.Row([numero_field, piso_field]),
            ft.Row([estado_dropdown, hotel_dropdown]),
            boton_agregar,
            tabla
        ])
    )