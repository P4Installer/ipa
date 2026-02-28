import flet as ft
import requests
import time
import json
import os

# 1. Базовые настройки
DEFAULT_REPOS = [
    "https://raw.githubusercontent.com/P4Installer/asda/main/repo.json"
]
PROXY_ESIGN_URL = "https://applejr.net/post/esignpwerchina.plist"
SAVE_FILE = "repos_config.json"

async def main(page: ft.Page):
    page.title = "P4Installer"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0e0e0e" 
    page.padding = 16
    page.scroll = ft.ScrollMode.ADAPTIVE
    
    user_repos = []
    dynamic_content = ft.Column(spacing=12)

    # Функции сохранения (через файл)
    def save_to_file():
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(user_repos, f)
        except: pass

    def load_from_file():
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    return json.load(f)
            except: return []
        return []

    # --- ИСПРАВЛЕНО: Теперь ссылка реально откроется ---
    async def open_url(url):
        # Используем современный UrlLauncher, чтобы убрать DeprecationWarning
        await page.launch_url(url)

    async def load_repos(e=None):
        dynamic_content.controls.clear()
        dynamic_content.controls.append(
            ft.Container(
                content=ft.ProgressRing(color="#2fb5d2", width=20, height=20),
                alignment=ft.Alignment(0, 0), padding=20
            )
        )
        page.update()

        all_repos = list(set(DEFAULT_REPOS + user_repos))
        new_controls = []

        for url in all_repos:
            try:
                res = requests.get(f"{url}?t={int(time.time())}", timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    new_controls.append(
                        ft.Text(data.get("repo_name", "Источник"), size=22, weight="bold", margin=ft.Margin.only(top=10, bottom=5))
                    )
                    for pkg in data.get("packages", []):
                        new_controls.append(
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(
                                        content=ft.Text(pkg['name'][0], weight="bold", size=20, color="white"),
                                        width=54, height=54, bgcolor=pkg.get("color", "#2fb5d2"), border_radius=12, alignment=ft.Alignment(0, 0)
                                    ),
                                    ft.Column([
                                        ft.Text(pkg['name'], size=17, weight="bold", color="white"),
                                        ft.Text(pkg['description'], size=14, color="#8e8e93", width=180, no_wrap=True),
                                    ], expand=True, spacing=2),
                                    ft.Button(
                                        "GET",
                                        color="#2fb5d2", bgcolor="#2c2c2e",
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), padding=ft.Padding.symmetric(horizontal=18, vertical=6)),
                                        # Вызываем через run_task, чтобы await сработал внутри
                                        on_click=lambda e, u=pkg['url']: page.run_task(open_url, u)
                                    )
                                ]),
                                padding=12, bgcolor="#1c1c1e", border_radius=14
                            )
                        )
            except: pass

        dynamic_content.controls.clear()
        dynamic_content.controls.extend(new_controls)
        page.update()

    async def add_repo_click(e=None):
        url = repo_input.value.strip()
        if url and url not in user_repos:
            user_repos.append(url)
            save_to_file()
            repo_input.value = ""
            await load_repos()

    user_repos.extend(load_from_file())

    repo_input = ft.TextField(
        hint_text="https://...", expand=True, bgcolor="#1c1c1e",
        border_color="#2c2c2e", border_radius=10, content_padding=12
    )

    page.add(
        ft.Container(
            content=ft.Text("P4Installer", size=34, weight="bold"),
            padding=ft.Padding.only(top=20, bottom=10)
        ),
        ft.Column([
            ft.Text("Добавить источник", size=22, weight="bold"),
            ft.Row([
                repo_input,
                ft.IconButton(
                    icon=ft.Icons.SETTINGS, 
                    on_click=lambda e: page.run_task(add_repo_click), 
                    bgcolor="#2fb5d2", icon_color="white"
                )
            ])
        ], spacing=10),
        dynamic_content,
        ft.Column([
            ft.Text("Стандартные", size=22, weight="bold", margin=ft.Margin.only(top=15)),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text("E", weight="bold", size=20, color="white"),
                        width=54, height=54,
                        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=["#5856d6", "#3533a3"]),
                        border_radius=12, alignment=ft.Alignment(0, 0)
                    ),
                    ft.Column([
                        ft.Text("ESign Installer", size=17, weight="bold", color="white"),
                        ft.Text("Установщик с прокси", size=14, color="#8e8e93"),
                    ], expand=True, spacing=2),
                    ft.Button(
                        "GET",
                        color="#2fb5d2", bgcolor="#2c2c2e",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), padding=ft.Padding.symmetric(horizontal=18, vertical=6)),
                        on_click=lambda _: page.run_task(open_url, f"itms-services://?action=download-manifest&url={PROXY_ESIGN_URL}")
                    )
                ]),
                padding=12, bgcolor="#1c1c1e", border_radius=14
            )
        ])
    )

    await load_repos()

if __name__ == "__main__":
    # Убрали устаревший ft.app
    ft.run(main)