import flet as ft
#from database import PEOPLE, FAMILIES
from models import Person
from data_loader import load_people, load_families

PEOPLE = load_people()
FAMILIES = load_families()

def main(page: ft.Page):
    page.title = "ספר משפחה"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.DARK

    # ---------- STATE ----------
    state = {
        "screen": "all", 
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
        elif state["screen"] == "search_all":
            state["search"] = ""
            render_search_all()
        elif state["screen"] == "families":
            render_families()
        elif state["screen"] == "family":
            render_family(state["family_id"])

        page.update()


    def render_all():
        family_list_view.controls.clear()
        search_field.visible = True
        family_list_view.controls.append(search_field)

        for person in PEOPLE.values():
            full_name = f"{person.name} {person.family}"
            if state["search"] in full_name:
                add_person_card(person)

    def render_search_all():
        family_list_view.controls.clear()
        search_field.visible = True   
      
        family_list_view.controls.append(ft.Text("חיפוש כללי (שם, כתובת, יומולדת...)", size=20, weight="bold"))
        family_list_view.controls.append(search_field)
      
        if not state["search"]:
            family_list_view.controls.append(ft.Text("הקלד משהו כדי להתחיל לחפש...", italic=True, color="grey"))
            return
        term = state["search"]
        for person in PEOPLE.values():
            found_in = None
            if term in person.name or term in person.family:
                found_in = None
            elif term in person.address:
                found_in = f"כתובת: {person.address}"
            elif term in person.birthday:
                found_in = f"יום הולדת: {person.birthday}"
            elif term in person.phone:
                found_in = f"טלפון: {person.phone}"

            # אם מצאנו התאמה באחד השדות
            if found_in is not None or term in person.name or term in person.family:
                add_person_card(person, extra_info=found_in)

    # פותחת רשימה של משפחה ספציפית 
    def render_family(family_id): 
        family_list_view.controls.clear() 
        family_list_view.controls.append( 
            ft.Row([ ft.TextButton( "<- חזרה", 
                on_click=lambda _: go_all(), 
                style=ft.ButtonStyle(color=ft.Colors.BLUE_700))], 
                alignment=ft.MainAxisAlignment.START ) ) 
        family = FAMILIES.get(family_id)
        if not family:
            return
        family_list_view.controls.append(
            ft.Text(
                family["title"], size=40, weight="bold"
            )
        )
        # ===== הורים =====
        family_list_view.controls.append(
            ft.Text("הורים:", size=22, weight="bold"))
        for parent_id in family["parents"]:
            add_person_card(PEOPLE[parent_id])
        # ===== ילדים =====
        family_list_view.controls.append(
            ft.Text("ילדים:", size=22, weight="bold"))
        for child_id in family["children"]:
            add_person_card(PEOPLE[child_id]) 
        page.update()
         

    # ---------- ACTIONS ----------
    def go_all():
        state["screen"] = "all"
        state["family_id"] = "all"
        render()

    def open_family(fid):
        state["screen"] = "family"
        state["family_id"] = fid
        render()

    def update_search(text):
        state["search"] = text
        render()


    # ---------- PERSON CARD ----------
    def add_person_card(person, extra_info=None):
        info_text = ft.Text(extra_info, size=12, color="grey") if extra_info else ft.Container()
        
        family_list_view.controls.append(
            ft.Container(
                padding=10,
                border=ft.Border.all(1),
                border_radius=8,
                ink=True,
                on_click=lambda _: show_details(person),
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON),
                    ft.Column([
                        ft.Text(f"{person.name} {person.family}"),
                        info_text
                    ], expand=True, spacing=2),
                    ft.IconButton(
                        ft.Icons.HOME,
                        icon_color="orange",
                        on_click=lambda e, f=person.family_id: open_family(f)
                    ) if person.family_id else ft.Container()
                ],
                rtl=True
                )
            )
        )

    # ---------- DIALOG ----------
    def show_details(p):
        dlg = ft.AlertDialog(
            title=ft.Text(f"{p.name} {p.family}", weight="bold", rtl=True),
            content=ft.Column([
                ft.Text(f"כתובת: {p.address}"),
                ft.Text(f"יום הולדת: {p.birthday}"),
                ft.Text(f"טלפון: {p.phone}"),
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
            state["search"] = ""
            go_all()
        elif index == 1:
            state["screen"] = "search_all"
            state["search"] = ""
            render()
        #elif index == 2:
         #   state["screen"] = "families"
          #  render()


    nav = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.PEOPLE, label="כולם"),
            ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="חיפוש כללי"),
            #ft.NavigationRailDestination(icon=ft.Icons.FOLDER, label="משפחות"),
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
        ft.Column([family_list_view, ft.Divider(height=1), nav], expand=True)
    )

    render()

if __name__ == "__main__":  
    ft.run(main)

# C:\Users\ariel\Desktop\1\0\bfamily