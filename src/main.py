import flet as ft


def main(page: ft.Page):
    page.add(ft.Text(value="KORMOLIPI"))

    def add_kormo(e):
        kormo_view.controls.append(ft.Checkbox(label=new_kormo.value))
        new_kormo.value = ""
        view.update()

    new_kormo = ft.TextField(hint_text="Add new kormo", expand=True)
    kormo_view = ft.Column()

    view = ft.Column(
        width=600,
        controls=[
            ft.Row(
                controls=[
                    new_kormo,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        on_click=add_kormo,
                        width=40,
                        height=40,
                    ),
                ]
            ),
            kormo_view,
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(view)


ft.app(main)
