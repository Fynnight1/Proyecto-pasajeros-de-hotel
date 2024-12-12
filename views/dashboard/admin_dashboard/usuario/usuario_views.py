import flet as ft  # type: ignore
from controllers.user_controller import UserController
from views.shared.back_button import back_button

def usuario_list_view(page: ft.Page):
    controller = UserController()

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("RUT")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Username")),
            ft.DataColumn(ft.Text("Rol")),
            ft.DataColumn(ft.Text("Activo")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def toggle_active(uid, new_value):
        # Esta función se llama cuando se cambia el estado del switch del usuario.
        # new_value es True/False. Actualizamos el usuario con active=new_value.
        controller.update_user(uid, active=new_value)
        refrescar()

    def refrescar():
        tabla.rows.clear()
        usuarios = controller.get_users()
        for u in usuarios:
            # Creamos el switch para activar/desactivar el usuario
            active_switch = ft.Switch(
                value=u.active,
                on_change=lambda e, uid=u.id: toggle_active(uid, e.control.value)
            )

            # Botón para editar usuario
            edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, uid=u.id: editar(uid))

            # No necesitamos un botón DELETE para desactivar/activar,
            # ya que eso se hace con el switch.

            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(u.id))),
                        ft.DataCell(ft.Text(u.name)),
                        ft.DataCell(ft.Text(u.rut)),
                        ft.DataCell(ft.Text(u.address or "")),
                        ft.DataCell(ft.Text(u.phone or "")),
                        ft.DataCell(ft.Text(u.username)),
                        ft.DataCell(ft.Text(u.role)),
                        ft.DataCell(active_switch),  # Aquí va el Switch para activar/desactivar
                        ft.DataCell(edit_button)     # Solo el botón de editar en la columna de acciones
                    ]
                )
            )
        page.update()

    def crear(e):
        page.views.append(usuario_create_view(page))
        page.go("/admin/usuarios/crear")
        page.update()

    def editar(uid):
        page.views.append(usuario_edit_view(page, uid))
        page.go("/admin/usuarios/editar")
        page.update()

    # Ya no necesitamos una función desactivar separada, ya que el switch se encarga.
    # def desactivar(uid):
    #     controller.deactivate_user(uid)
    #     refrescar()

    refrescar()

    return ft.View(
        "/admin/usuarios",
        [
            back_button(page),
            ft.Text("Listado de Usuarios", style="titleLarge"),
            ft.ElevatedButton("Crear Usuario", on_click=crear),
            tabla
        ]
    )

def usuario_create_view(page: ft.Page):
    controller = UserController()

    name = ft.TextField(label="Nombre")
    rut = ft.TextField(label="RUT")
    address = ft.TextField(label="Dirección")
    phone = ft.TextField(label="Teléfono")
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)

    # Opciones de rol con ft.dropdown.Option
    rol_opciones = [
        ft.dropdown.Option(text="Administrador", key="administrator"),
        ft.dropdown.Option(text="Trabajador", key="worker"),
        ft.dropdown.Option(text="Cliente", key="client")
    ]

    rol = ft.Dropdown(label="Rol", options=rol_opciones)

    def guardar(e):
        controller.create_user(name.value, rut.value, address.value, phone.value, username.value, password.value, rol.value)
        page.views.pop()
        page.views[-1] = usuario_list_view(page)
        page.update()

    return ft.View(
        "/admin/usuarios/crear",
        [
            back_button(page),
            ft.Text("Crear Usuario", style="titleLarge"),
            name, rut, address, phone, username, password, rol,
            ft.ElevatedButton("Guardar", on_click=guardar)
        ]
    )

def usuario_edit_view(page: ft.Page, usuario_id):
    controller = UserController()
    u = controller.get_user_by_id(usuario_id)
    if not u:
        return ft.View("/admin/usuarios/editar", [ft.Text("Usuario no encontrado")])

    name = ft.TextField(label="Nombre", value=u.name)
    rut = ft.TextField(label="RUT", value=u.rut)
    address = ft.TextField(label="Dirección", value=u.address or "")
    phone = ft.TextField(label="Teléfono", value=u.phone or "")
    username = ft.TextField(label="Username", value=u.username)
    password = ft.TextField(label="Password (opcional)", password=True, can_reveal_password=True)

    rol_opciones = [
        ft.dropdown.Option(text="Administrador", key="administrator"),
        ft.dropdown.Option(text="Trabajador", key="worker"),
        ft.dropdown.Option(text="Cliente", key="client")
    ]

    rol = ft.Dropdown(label="Rol", options=rol_opciones, value=u.role)
    activo = ft.Checkbox(label="Activo", value=u.active)

    def actualizar(e):
        controller.update_user(
            usuario_id,
            name=name.value,
            rut=rut.value,
            address=address.value,
            phone=phone.value,
            username=username.value,
            password=password.value if password.value else None,
            role=rol.value,
            active=activo.value
        )
        page.views.pop()
        page.views[-1] = usuario_list_view(page)
        page.update()

    return ft.View(
        "/admin/usuarios/editar",
        [
            back_button(page),
            ft.Text("Editar Usuario", style="titleLarge"),
            name, rut, address, phone, username, password, rol, activo,
            ft.ElevatedButton("Actualizar", on_click=actualizar)
        ]
    )
