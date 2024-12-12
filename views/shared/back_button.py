# views/shared/back_button.py

import flet as ft  # type: ignore
from views.shared.navigation import go_back

def back_button(page: ft.Page):
    return ft.IconButton(
        ft.icons.ARROW_BACK,
        on_click=lambda e: go_back(page)
    )
