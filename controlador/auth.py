from modelo.usuario import Usuario

def obtener_usuario(page: ft.Page):
    usuario_id = page.session.get("usuario_id")
    if usuario_id:
        return Usuario.get_by_id(usuario_id)
    return None

def requiere_rol(page: ft.Page, rol_requerido):
    usuario = obtener_usuario(page)
    if not usuario or usuario.rol != rol_requerido:
        page.dialog = ft.AlertDialog(title=ft.Text("Acceso Denegado"))
        page.dialog.open = True
        page.update()
        return False
    return True
