from models.user import User

def get_user(page: ft.Page): # type: ignore
    user_id = page.session.get("user_id")
    if user_id:
        return User.get_by_id(user_id)
    return None

def require_role(page: ft.Page, required_role): # type: ignore
    user = get_user(page)
    if not user or user.role != required_role:
        page.dialog = ft.AlertDialog(title=ft.Text("Access Denied")) # type: ignore
        page.dialog.open = True
        page.update()
        return False
    return True
