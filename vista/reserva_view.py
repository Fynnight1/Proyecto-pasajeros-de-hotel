import flet as ft
from controlador.reserva_controller import ReservaController
from controlador.cliente_controller import ClienteController
from controlador.habitacion_controller import HabitacionController
from controlador.trabajador_controller import TrabajadorController

def reserva_view(page: ft.Page):
    controller = ReservaController()
    cliente_controller = ClienteController()
    habitacion_controller = HabitacionController()
    trabajador_controller = TrabajadorController()
    
    def cargar_datos():
        reservas = controller.obtener_reservas()
        data_rows = []
        for r in reservas:
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(r.id))),
                        ft.DataCell(ft.Text(str(r.cliente_id))),
                        ft.DataCell(ft.Text(str(r.habitacion_id))),
                        ft.DataCell(ft.Text(str(r.trabajador_id))),
                        ft.DataCell(ft.Text(str(r.fecha_ingreso))),
                        ft.DataCell(ft.Text(str(r.fecha_salida))),
                    ]
                )
            )
        tabla.rows = data_rows
        page.update()
    
    def agregar_reserva(e):
        controller.crear_reserva(
            cliente_id=int(cliente_dropdown.value),
            habitacion_id=int(habitacion_dropdown.value),
            trabajador_id=int(trabajador_dropdown.value),
            fecha_ingreso=fecha_ingreso_field.value,
            fecha_salida=fecha_salida_field.value
        )
        cargar_datos()
    
    # Obtener listas para los Dropdowns
    clientes = cliente_controller.obtener_clientes()
    habitaciones = habitacion_controller.obtener_habitaciones()
    trabajadores = trabajador_controller.obtener_trabajadores()
    
    cliente_opciones = [ft.dropdown.Option(str(c.id), c.nombre) for c in clientes]
    habitacion_opciones = [ft.dropdown.Option(str(h.id), f"Habitación {h.numero}") for h in habitaciones]
    trabajador_opciones = [ft.dropdown.Option(str(t.id), t.nombre) for t in trabajadores]
    
    # Campos de entrada
    cliente_dropdown = ft.Dropdown(label="Cliente", options=cliente_opciones)
    habitacion_dropdown = ft.Dropdown(label="Habitación", options=habitacion_opciones)
    trabajador_dropdown = ft.Dropdown(label="Trabajador", options=trabajador_opciones)
    fecha_ingreso_field = ft.TextField(label="Fecha de Ingreso (YYYY-MM-DD)")
    fecha_salida_field = ft.TextField(label="Fecha de Salida (YYYY-MM-DD)")
    
    # Botones
    boton_agregar = ft.ElevatedButton(text="Agregar Reserva", on_click=agregar_reserva)
    
    # Tabla de datos
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Habitación")),
            ft.DataColumn(ft.Text("Trabajador")),
            ft.DataColumn(ft.Text("Fecha Ingreso")),
            ft.DataColumn(ft.Text("Fecha Salida")),
        ],
        rows=[]
    )
    
    cargar_datos()
    
    # Layout
    page.add(
        ft.Column([
            cliente_dropdown,
            habitacion_dropdown,
            trabajador_dropdown,
            ft.Row([fecha_ingreso_field, fecha_salida_field]),
            boton_agregar,
            tabla
        ])
    )