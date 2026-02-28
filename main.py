import flet as ft
import requests
import time

# Список репозиториев ПО УМОЛЧАНИЮ
DEFAULT_REPOS = [
    "https://raw.githubusercontent.com/P4Installer/asda/main/repo.json"
]

def main(page: ft.Page):
    page.title = "P4Installer"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0e0e0e"
    page.padding = 20
    
    # Список для хранения добавленных репозиториев в рамках сессии
    user_repos = []

    # Контейнер для динамического контента (список приложений из JSON)
    dynamic_content = ft.Column(spacing=10)

    def load_repos():
        dynamic_content.controls.clear()
        all_repos = list(set(DEFAULT_REPOS + user_repos))
        
        dynamic_content.controls.append(ft.ProgressBar(color="#2fb5d2"))
        page.update()

        new_controls = []
        for url in all_repos:
            try:
                # Обход кэша через timestamp
                res = requests.get(f"{url}?t={int(time.time())}", timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    # Заголовок источника
                    new_controls.append(ft.Text(data.get("repo_name", "Источник"), size=22, weight="bold"))

                    # Пакеты внутри
                    for pkg in data.get("packages", []):
                        new_controls.append(
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(
                                        content=ft.Text(pkg['name'][0], weight="bold", size=20, color="white"),
                                        width=54, height=54,
                                        bgcolor=pkg.get("color", "#2fb5d2"),
                                        border_radius=12,
                                        # ИСПРАВЛЕНО: используем строку "center"
                                        alignment=ft.Alignment(0, 0) 
                                    ),
                                    ft.Column([
                                        ft.Text(pkg['name'], size=17, weight="bold", color="white"),
                                        ft.Text(pkg['description'], size=14, color="#8e8e93", width=180, no_wrap=True),
                                    ], expand=True),
                                    ft.ElevatedButton(
                                        "GET",
                                        color="#2fb5d2",
                                        bgcolor="#2c2c2e",
                                        on_click=lambda e, u=pkg['url']: page.launch_url(u)
                                    )
                                ]),
                                padding=12, bgcolor="#1c1c1e", border_radius=14
                            )
                        )
            except Exception as ex:
                print(f"Ошибка: {ex}")

        dynamic_content.controls.clear()
        if new_controls:
            dynamic_content.controls.extend(new_controls)
        else:
            dynamic_content.controls.append(ft.Text("Репозитории загружаются...", color="grey"))
        page.update()

    def add_repo_click(e):
        url = repo_input.value.strip()
        if url and url not in user_repos:
            user_repos.append(url)
            repo_input.value = ""
            load_repos()

    repo_input = ft.TextField(
        hint_text="https://...",
        expand=True,
        bgcolor="#1c1c1e",
        border_color="#2c2c2e",
        border_radius=10,
    )

    page.add(
        ft.Column([
            ft.Text("P4Installer", size=34, weight="bold"),
            ft.Text("Добавить источник", size=22, weight="bold", margin=ft.margin.only(top=20)),
            ft.Row([
                repo_input,
                # Использована строка "add"
                ft.IconButton(icon="add", on_click=add_repo_click, bgcolor="#2fb5d2", icon_color="white")
            ]),
            dynamic_content,
            ft.Text("Стандартные", size=22, weight="bold", margin=ft.margin.only(top=20)),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text("E", weight="bold", size=20, color="white"),
                        width=54, height=54,
                        gradient=ft.LinearGradient(["#5856d6", "#3533a3"]),
                        border_radius=12,
                        # ИСПРАВЛЕНО: используем объект Alignment напрямую (координаты 0,0 это центр)
                        alignment=ft.Alignment(0, 0)
                    ),
                    ft.Column([
                        ft.Text("ESign Installer", size=17, weight="bold", color="white"),
                        ft.Text("Установщик с прокси", size=14, color="#8e8e93"),
                    ], expand=True),
                    ft.ElevatedButton(
                        "GET",
                        color="#2fb5d2",
                        bgcolor="#2c2c2e",
                        on_click=lambda _: page.launch_url("itms-services://?action=download-manifest&url=https://applejr.net/post/esignpwerchina.plist")
                    )
                ]),
                padding=12, bgcolor="#1c1c1e", border_radius=14
            ),
        ], scroll=ft.ScrollMode.ADAPTIVE)
    )

    load_repos()

# Важный момент: для некоторых сред сборки
ft.app(target=main)