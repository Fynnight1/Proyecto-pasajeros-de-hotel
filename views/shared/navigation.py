# views/shared/navigation.py

import flet as ft  # type: ignore

def go_back(page: ft.Page):
    if len(page.views) > 1:
        page.views.pop()
        page.update()
    else:
        print("No hay más vistas para retroceder.")
