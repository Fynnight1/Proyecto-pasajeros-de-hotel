import flet as ft

def back_button(callback):
    return ft.IconButton(
        ft.icons.ARROW_BACK,
        on_click=callback
    )
