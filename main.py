import requests
import os
import sys
import subprocess

# Ссылка на RAW-версию твоего main.py
GITHUB_RAW_URL = "https://raw.githubusercontent.com/P4Installer/ipa/main/app.py"
TEMP_FILE = "p4_main_cached.py"

def update_and_run():
    print("Проверка обновлений P4Installer...")
    
    try:
        # 1. Скачиваем свежий код
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        if response.status_code == 200:
            with open(TEMP_FILE, "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Обновление успешно загружено.")
        else:
            print(f"Не удалось скачать обновление (код {response.status_code}).")
    except Exception as e:
        print(f"Ошибка при подключении к GitHub: {e}")
        if os.path.exists(TEMP_FILE):
            print("Запуск сохраненной локальной копии...")
        else:
            print("Локальная копия не найдена. Проверьте интернет.")
            return

    # 2. Запускаем скачанный файл как отдельный процесс
    # Это полностью изолирует основной код от загрузчика
    if os.path.exists(TEMP_FILE):
        print("Запуск приложения...")
        subprocess.run([sys.executable, TEMP_FILE])

if __name__ == "__main__":
    update_and_run()
