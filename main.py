import flet as ft
from family_data import families
from models import Person, UIItem

def main(page: ft.Page):
    page.title = "ספר משפחה"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.DARK

    # ---------- STATE ----------
    state = {
        "screen": "all",      # all | families | family
        "family_id": "all",
        "search": ""
    }

    # ---------- UI ----------
    family_list_view = ft.ListView(expand=1, spacing=10, padding=20)

    search_field = ft.TextField(
        hint_text="חיפוש...",
        visible=False,
        on_change=lambda e: update_search(e.control.value)
    )

    # ---------- RENDER ----------
    def render():
        if state["screen"] == "all":
            render_all()
        elif state["screen"] == "families":
            render_families()
        elif state["screen"] == "family":
            render_family(state["family_id"])

        page.update()

    def render_all():
        family_list_view.controls.clear()
        search_field.visible = True
        family_list_view.controls.append(search_field)

        for item in families["all"]:
            if isinstance(item, Person):
                text = f"{item.name} {item.family}"
                if state["search"] in text:
                    add_person_card(item)

    def render_families():
        family_list_view.controls.clear()
        search_field.visible = False

        family_list_view.controls.append(
            ft.Text("משפחות", size=30, weight="bold")
        )

        for fid, items in families.items():
            if fid == "all":
                continue
            for item in items:
                if isinstance(item, UIItem) and item.type == "main_title":
                    family_list_view.controls.append(
                        ft.Container(
                            content=ft.Text(item.title, size=18),
                            padding=10,
                            border=ft.Border.all(1),
                            border_radius=8,
                            ink=True,
                            on_click=lambda e, f=fid: open_family(f)
                        )
                    )
                    break

    def render_family(fid):
        family_list_view.controls.clear()
        search_field.visible = False

        family_list_view.controls.append(
            ft.Row(
                [ft.TextButton("← חזרה", on_click=lambda _: go_all())],
                alignment=ft.MainAxisAlignment.START, rtl=True
            )
        )

        for item in families.get(fid, []):
            if isinstance(item, UIItem):
                size = 30 if item.type == "main_title" else 20
                family_list_view.controls.append(
                    ft.Text(item.title, size=size, weight="bold")
                )
            elif isinstance(item, Person):
                add_person_card(item)

    # ---------- ACTIONS ----------
    def go_all():
        state["screen"] = "all"
        state["family_id"] = "all"
        render()

    def open_family(fid):
        state["screen"] = "family"
        state["family_id"] = fid
        render()

    def open_families():
        state["screen"] = "families"
        render()

    def update_search(text):
        state["search"] = text
        render()

    # ---------- PERSON CARD ----------
    def add_person_card(person):
        family_list_view.controls.append(
            ft.Container(
                padding=10,
                border=ft.Border.all(1),
                border_radius=8,
                ink=True,
                on_click=lambda _: show_details(person),
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON),
                    ft.Text(f"{person.name} {person.family}", expand=True),
                    ft.IconButton(
                        ft.Icons.HOME,
                        icon_color="orange",
                        on_click=lambda e, f=person.has_family_id: open_family(f)
                    ) if person.has_family_id else ft.Container()
                ],
                rtl=True
                )
            )
        )

    # ---------- DIALOG ----------
    def show_details(p):
        dlg = ft.AlertDialog(
            title=ft.Text(f"{p.name} {p.family}", weight="bold"),
            content=ft.Column([
                ft.Text(f"גיל: {p.age}"),
                ft.Text(f"טלפון: {p.phone}"),
                ft.Text(f"כתובת: {p.address}"),
                ft.Text(f"יום הולדת: {p.birthday}")
            ],rtl=True, tight=True),
            actions=[ft.TextButton("סגור", on_click=lambda e: close_dialog(dlg))]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def close_dialog(dlg):
        dlg.open = False
        page.update()

    # ---------- NAV ----------
    def on_nav_change(e):
        index = e.control.selected_index
        if index == 0:
            go_all()
        elif index == 1:
            open_families()
        elif index == 2:
            open_family("gadasi_parents")
        elif index == 3:
            open_family("jamil_parents")
        elif index == 4:
            open_family("bahur_parents")

    nav = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="כולם"),
            ft.NavigationRailDestination(icon=ft.Icons.FOLDER, label="משפחות"),
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="גדסי"),
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="ג'מיל"),
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="בחור"),
        ],
        on_change=on_nav_change
    )

    page.appbar = ft.AppBar(
        title=ft.Text("ספר משפחה"),
        actions=[
            ft.IconButton(
                ft.Icons.BRIGHTNESS_4,
                on_click=lambda e: toggle_theme()
            )
        ]
    )

    def toggle_theme():
        page.theme_mode = (
            ft.ThemeMode.LIGHT
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        page.update()

    page.add(
        ft.Row([nav, ft.VerticalDivider(width=1), family_list_view], expand=True)
    )

    render()

if __name__ == "__main__":  
    ft.run(main)

# C:\Users\ariel\Desktop\1\0\bfamily