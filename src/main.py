import flet as ft


class Kormo(ft.Column):
    def __init__(self, kormo_name, kormo_status_change, kormo_delete):
        super().__init__()
        self.completed = False
        self.kormo_name = kormo_name
        self.kormo_status_change = kormo_status_change
        self.kormo_delete = kormo_delete
        self.display_kormo = ft.Checkbox(
            value=False,
            label=self.kormo_name,
            on_change=self.status_changed,
        )

        self.edit_kormo_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_kormo,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit Kormo",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete Kormo",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_kormo_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update Kormo",
                    on_click=self.save_clicked,
                )
            ]
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_kormo_name.value = self.display_kormo.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_kormo.label = self.edit_kormo_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.completed = self.display_kormo.value
        self.kormo_status_change(self)

    def delete_clicked(self, e):
        self.kormo_delete(self)


class KormolipiApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.new_kormo = ft.TextField(
            hint_text="What kormo needs to be done?",
            on_submit=self.add_clicked,
            expand=True,
        )
        self.kormotalika = ft.Column()

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text="All"),
                ft.Tab(text="Active"),
                ft.Tab(text="Completed"),
            ]
        )
        self.kormo_left = ft.Text("0 kormo left")

        self.width = 600
        self.controls=[
            ft.Row(
                [ft.Text(value="Kormolipi", theme_style=ft.TextThemeStyle.HEADLINE_LARGE)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_kormo,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        on_click=self.add_clicked,
                    )
                ]
            ),
            ft.Column(
                spacing=20,
                controls=[
                    self.filter,
                    self.kormotalika,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.kormo_left,
                            ft.OutlinedButton(
                                text="Clear completed",
                                on_click=self.clear_clicked,
                            )
                        ]
                    )
                ]
            )
        ]

    def add_clicked(self, e):
        if self.new_kormo.value:
            kormo = Kormo(
                self.new_kormo.value,
                self.kormos_status_change,
                self.kormo_delete
            )
            self.kormotalika.controls.append(kormo)
            self.new_kormo.value = ""
            self.new_kormo.focus()
            self.before_update()
            self.update()
    
    def kormos_status_change(self, kormo):
        self.before_update()
        self.update()

    def kormo_delete(self, kormo):
        self.kormotalika.controls.remove(kormo)
        self.before_update()
        self.update()
    
    def tabs_changed(self, e):
        self.before_update()
        self.update()

    def clear_clicked(self, e):
        for kormo in self.kormotalika.controls[:]:
            if kormo.completed:
                self.kormo_delete(kormo)
        self.before_update()
        self.update()

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for kormo in self.kormotalika.controls:
            kormo.visible = (
                status == "All"
                or (status == "Active" and kormo.completed == False)
                or (status == "Completed" and kormo.completed)
            )
            if not kormo.completed:
                count += 1
        self.kormo_left.value = f"{count} active kormo left"

def main(page: ft.Page):
    page.title = "Kormolipi"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    
    page.add(KormolipiApp())

ft.app(main)