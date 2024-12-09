# vista/adminoptions/gestionar_usuarios_view.py

import flet as ft
from controlador.usuario_controller import UsuarioController

def gestionar_usuarios_view(page: ft.Page):
    usuario_controller = UsuarioController()
    usuarios = usuario_controller.obtener_usuarios()

    usuarios_list = ft.Column(scroll="auto")
    usuarios_list.controls.append(
        ft.Row([
            ft.Text("ID", weight="bold", width=50),
            ft.Text("Nombre", weight="bold", width=150),
            ft.Text("Usuario", weight="bold", width=100),
            ft.Text("Rol", weight="bold", width=100),
            ft.Text("Activo", weight="bold", width=80),
            ft.Text("Acciones", weight="bold", width=150)
        ])
    )

    for u in usuarios:
        usuarios_list.controls.append(
            ft.Row([
                ft.Text(str(u.id), width=50),
                ft.Text(u.nombre, width=150),
                ft.Text(u.username, width=100),
                ft.Text(u.rol, width=100),
                ft.Text("Sí" if u.activo else "No", width=80),
                ft.Row([
                    ft.IconButton(
                        ft.icons.EDIT,
                        on_click=lambda e, uid=u.id: abrir_editar_usuario(page, uid)
                    ),
                    ft.IconButton(
                        ft.icons.DELETE,
                        on_click=lambda e, uid=u.id: desactivar_usuario(page, uid)
                    )
                ], width=150)
            ])
        )

    def abrir_crear_usuario(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Crear Nuevo Usuario"),
            content=crear_editar_usuario_form(),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Crear", on_click=lambda e: crear_usuario(page, dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def abrir_editar_usuario(page: ft.Page, usuario_id):
        usuario_obj = usuario_controller.obtener_usuario_por_id(usuario_id)
        if not usuario_obj:
            page.snack_bar = ft.SnackBar(ft.Text("Usuario no encontrado"))
            page.snack_bar.open = True
            page.update()
            return

        dialog = ft.AlertDialog(
            title=ft.Text(f"Editar Usuario ID: {usuario_id}"),
            content=crear_editar_usuario_form(usuario_obj),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Guardar", on_click=lambda e: editar_usuario(page, dialog, usuario_id))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def crear_usuario(page: ft.Page, dialog: ft.AlertDialog):
        nombre = nombre_field.value
        rut = rut_field.value
        direccion = direccion_field.value
        telefono = telefono_field.value
        username = username_field.value
        password = password_field.value
        rol = rol_dropdown.value

        if not nombre or not rut or not username or not password or not rol:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos obligatorios"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            usuario_controller.crear_usuario(nombre, rut, direccion, telefono, username, password, rol)
            page.snack_bar = ft.SnackBar(ft.Text("Usuario creado exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            # Refrescar la lista de usuarios
            gestionar_usuarios_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al crear usuario"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())]
            )
            page.dialog.open = True
            page.update()

    def editar_usuario(page: ft.Page, dialog: ft.AlertDialog, usuario_id):
        nombre = nombre_field.value
        rut = rut_field.value
        direccion = direccion_field.value
        telefono = telefono_field.value
        username = username_field.value
        password = password_field.value
        rol = rol_dropdown.value
        activo = activo_checkbox.value

        try:
            usuario_controller.actualizar_usuario(
                usuario_id, nombre=nombre, rut=rut, direccion=direccion,
                telefono=telefono, password=password or None, rol=rol, activo=activo
            )
            page.snack_bar = ft.SnackBar(ft.Text("Usuario actualizado exitosamente"))
            page.snack_bar.open = True
            dialog.close()
            page.update()
            # Refrescar la lista de usuarios
            gestionar_usuarios_view(page)
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error al actualizar usuario"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())]
            )
            page.dialog.open = True
            page.update()

    def desactivar_usuario(page: ft.Page, usuario_id):
        if usuario_controller.desactivar_usuario(usuario_id):
            page.snack_bar = ft.SnackBar(ft.Text("Usuario desactivado exitosamente"))
            page.snack_bar.open = True
            page.update()
            gestionar_usuarios_view(page)
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("Error al desactivar usuario"))
            page.dialog.open = True
            page.update()

    def crear_editar_usuario_form(usuario=None):
        """Crea el formulario para crear o editar un usuario."""
        nombre_field = ft.TextField(label="Nombre", value=usuario.nombre if usuario else "")
        rut_field = ft.TextField(label="RUT", value=usuario.rut if usuario else "")
        direccion_field = ft.TextField(label="Dirección", value=usuario.direccion if usuario else "")
        telefono_field = ft.TextField(label="Teléfono", value=usuario.telefono if usuario else "")
        username_field = ft.TextField(label="Usuario", value=usuario.username if usuario else "")
        password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
        rol_dropdown = ft.Dropdown(
            label="Rol",
            options=[
                ft.dropdown.Option("administrador"),
                ft.dropdown.Option("trabajador"),
                ft.dropdown.Option("cliente"),
            ],
            value=usuario.rol if usuario else None
        )
        activo_checkbox = ft.Checkbox(label="Activo", value=usuario.activo if usuario else True)

        form_controls = [
            nombre_field,
            rut_field,
            direccion_field,
            telefono_field,
            username_field,
            password_field,
            rol_dropdown
        ]

        if usuario:
            form_controls.append(activo_checkbox)

        form = ft.Column(form_controls, spacing=10)

        return form

    # Botón para crear nuevo usuario
    crear_usuario_button = ft.ElevatedButton("Crear Nuevo Usuario", on_click=abrir_crear_usuario)

    # Añadimos el botón de crear usuario arriba de la lista
    usuarios_view = ft.Column([
        ft.Text("Gestión de Usuarios", style="headlineMedium"),
        crear_usuario_button,
        usuarios_list
    ], scroll="auto")

    return usuarios_view
