import os
import sys
import gc
import shutil
import platform
import subprocess
import tempfile
import threading
import re
import winreg
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox


APP_NAME = "🚀 Windows Optimizer Ultra 6.2.1"


def run_command(command, admin=False):
    """Безпечний запуск Windows-команди."""
    try:
        if admin:
            # Запуск через PowerShell з підвищенням прав.
            ps = (
                "Start-Process powershell -Verb RunAs -Wait "
                "-ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command "
                f"\"{command}\"'"
            )
            return subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps],
                capture_output=True, text=True
            )
        return subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        return None


class WindowsOptimizer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("1440x860")
        self.minsize(1180, 700)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.pages = {}
        self.menu_buttons = {}
        self.setup_languages()

        self.create_sidebar()
        self.create_main_area()
        self.show_page("Панель керування")
        self.update_stats()

        if "--ultimate" in sys.argv and self.is_admin():
            self.after(700, self.activate_ultimate_performance)


    # =========================================================
    # 5 LANGUAGES
    # =========================================================
    def setup_languages(self):
        self.languages = {
            "🇺🇦 Українська": "uk",
            "🇬🇧 English": "en",
            "🇵🇱 Polski": "pl",
            "🇩🇪 Deutsch": "de",
            "🇪🇸 Español": "es",
        }
        self.lang = "uk"
        self.translations = {
            "uk": {},
            "en": {
                "Панель керування":"Dashboard", "Оптимізація":"Optimization", "Очищення":"Cleaning", "Ігровий режим":"Game Mode", "Ultimate Performance":"Ultimate Performance", "Система":"System", "Моніторинг":"Monitoring", "Інструменти":"Tools", "ГОЛОВНЕ МЕНЮ":"MAIN MENU", "Швидкі дії":"Quick Actions", "ЗАПУСТИТИ":"RUN", "СКАНУВАТИ СИСТЕМУ":"SCAN SYSTEM", "Оптимізувати RAM":"Optimize RAM", "Очистити TEMP":"Clean TEMP", "Очистити DNS":"Flush DNS", "Очистити кошик":"Empty Recycle Bin", "Інформація про ПК":"PC Information", "Перевірити Windows":"Check Windows", "Повна оптимізація":"Full Optimization", "Диспетчер завдань":"Task Manager", "Windows Update":"Windows Update", "Зберегти звіт":"Save Report", "Вітаємо! 👋":"Welcome! 👋", "Оптимізуйте свій ПК для максимальної продуктивності!":"Optimize your PC for maximum performance!", "Процесор":"CPU", "Оперативна пам'ять":"RAM", "Диск (C:)":"Disk (C:)", "Створити / активувати":"Create / Activate", "Показати плани живлення":"Show power plans"
            },
            "pl": {
                "Панель керування":"Panel główny", "Оптимізація":"Optymalizacja", "Очищення":"Czyszczenie", "Ігровий режим":"Tryb gry", "Ultimate Performance":"Ultimate Performance", "Система":"System", "Моніторинг":"Monitoring", "Інструменти":"Narzędzia", "ГОЛОВНЕ МЕНЮ":"MENU GŁÓWNE", "Швидкі дії":"Szybkie akcje", "ЗАПУСТИТИ":"URUCHOM", "СКАНУВАТИ СИСТЕМУ":"SKANUJ SYSTEM", "Оптимізувати RAM":"Optymalizuj RAM", "Очистити TEMP":"Wyczyść TEMP", "Очистити DNS":"Wyczyść DNS", "Очистити кошик":"Opróżnij kosz", "Інформація про ПК":"Informacje o komputerze", "Перевірити Windows":"Sprawdź Windows", "Повна оптимізація":"Pełna optymalizacja", "Диспетчер завдань":"Menedżer zadań", "Windows Update":"Windows Update", "Зберегти звіт":"Zapisz raport", "Вітаємо! 👋":"Witaj! 👋", "Оптимізуйте свій ПК для максимальної продуктивності!":"Zoptymalizuj komputer dla maksymalnej wydajności!", "Процесор":"Procesor", "Оперативна пам'ять":"Pamięć RAM", "Диск (C:)":"Dysk (C:)", "Створити / активувати":"Utwórz / Aktywuj", "Показати плани живлення":"Pokaż plany zasilania"
            },
            "de": {
                "Панель керування":"Dashboard", "Оптимізація":"Optimierung", "Очищення":"Bereinigung", "Ігровий режим":"Gaming-Modus", "Ultimate Performance":"Ultimate Performance", "Система":"System", "Моніторинг":"Überwachung", "Інструменти":"Werkzeuge", "ГОЛОВНЕ МЕНЮ":"HAUPTMENÜ", "Швидкі дії":"Schnellaktionen", "ЗАПУСТИТИ":"STARTEN", "СКАНУВАТИ СИСТЕМУ":"SYSTEM SCANNEN", "Оптимізувати RAM":"RAM optimieren", "Очистити TEMP":"TEMP leeren", "Очистити DNS":"DNS leeren", "Очистити кошик":"Papierkorb leeren", "Інформація про ПК":"PC-Informationen", "Перевірити Windows":"Windows prüfen", "Повна оптимізація":"Vollständige Optimierung", "Диспетчер завдань":"Task-Manager", "Windows Update":"Windows Update", "Зберегти звіт":"Bericht speichern", "Вітаємо! 👋":"Willkommen! 👋", "Оптимізуйте свій ПК для максимальної продуктивності!":"Optimiere deinen PC für maximale Leistung!", "Процесор":"Prozessor", "Оперативна пам'ять":"Arbeitsspeicher", "Диск (C:)":"Laufwerk (C:)", "Створити / активувати":"Erstellen / Aktivieren", "Показати плани живлення":"Energiepläne anzeigen"
            },
            "es": {
                "Панель керування":"Panel", "Оптимізація":"Optimización", "Очищення":"Limpieza", "Ігровий режим":"Modo juego", "Ultimate Performance":"Ultimate Performance", "Система":"Sistema", "Моніторинг":"Monitorización", "Інструменти":"Herramientas", "ГОЛОВНЕ МЕНЮ":"MENÚ PRINCIPAL", "Швидкі дії":"Acciones rápidas", "ЗАПУСТИТИ":"EJECUTAR", "СКАНУВАТИ СИСТЕМУ":"ESCANEAR SISTEMA", "Оптимізувати RAM":"Optimizar RAM", "Очистити TEMP":"Limpiar TEMP", "Очистити DNS":"Limpiar DNS", "Очистити кошик":"Vaciar papelera", "Інформація про ПК":"Información del PC", "Перевірити Windows":"Comprobar Windows", "Повна оптимізація":"Optimización completa", "Диспетчер завдань":"Administrador de tareas", "Windows Update":"Windows Update", "Зберегти звіт":"Guardar informe", "Вітаємо! 👋":"¡Bienvenido! 👋", "Оптимізуйте свій ПК для максимальної продуктивності!":"¡Optimiza tu PC para obtener el máximo rendimiento!", "Процесор":"Procesador", "Оперативна пам'ять":"Memoria RAM", "Диск (C:)":"Disco (C:)", "Створити / активувати":"Crear / Activar", "Показати плани живлення":"Mostrar planes de energía"
            }
        }

    # Complete UI translations for all five languages.
        self.translations['en'].update({'Диск C:': 'Disk C:'})
        self.translations['pl'].update({'Диск C:': 'Dysk C:'})
        self.translations['de'].update({'Диск C:': 'Datenträger C:'})
        self.translations['es'].update({'Диск C:': 'Disco C:'})

        self.translations['en'].update({'🖥️ Система':'🖥️ System', '📊 Моніторинг':'📊 Monitoring', 'Статистика системи в реальному часі':'Real-time system statistics', 'Завантаження...':'Loading...', "Інформація про ваш комп'ютер":'Information about your computer', 'Операційна система:':'Operating system:', 'Версія:':'Version:', 'Фізичних ядер:':'Physical cores:', 'Логічних процесорів:':'Logical processors:', "Ім'я ПК:":'PC name:', 'Використано:':'Used:', 'Система':'System'})
        self.translations['en'].update({'Процесор:':'Processor:', "Оперативна пам'ять:":'RAM:', 'Фізичних ядер:':'Physical cores:', 'Логічних процесорів:':'Logical processors:'})
        self.translations['pl'].update({'🖥️ Система':'🖥️ System', '📊 Моніторинг':'📊 Monitoring', 'Статистика системи в реальному часі':'Statystyki systemu w czasie rzeczywistym', 'Завантаження...':'Ładowanie...', "Інформація про ваш комп'ютер":'Informacje o komputerze', 'Операційна система:':'System operacyjny:', 'Версія:':'Wersja:', 'Фізичних ядер:':'Rdzenie fizyczne:', 'Логічних процесорів:':'Procesory logiczne:', "Ім'я ПК:":'Nazwa komputera:', 'Використано:':'Użyto:', 'Система':'System'})
        self.translations['pl'].update({'Процесор:':'Procesor:', "Оперативна пам'ять:":'Pamięć RAM:', 'Фізичних ядер:':'Rdzenie fizyczne:', 'Логічних процесорів:':'Procesory logiczne:'})
        self.translations['de'].update({'🖥️ Система':'🖥️ System', '📊 Моніторинг':'📊 Überwachung', 'Статистика системи в реальному часі':'Echtzeit-Systemstatistik', 'Завантаження...':'Wird geladen...', "Інформація про ваш комп'ютер":'Informationen über Ihren Computer', 'Операційна система:':'Betriebssystem:', 'Версія:':'Version:', 'Фізичних ядер:':'Physische Kerne:', 'Логічних процесорів:':'Logische Prozessoren:', "Ім'я ПК:":'PC-Name:', 'Використано:':'Verwendet:', 'Система':'System'})
        self.translations['de'].update({'Процесор:':'Prozessor:', "Оперативна пам'ять:":'Arbeitsspeicher:', 'Фізичних ядер:':'Physische Kerne:', 'Логічних процесорів:':'Logische Prozessoren:'})
        self.translations['es'].update({'🖥️ Система':'🖥️ Sistema', '📊 Моніторинг':'📊 Monitorización', 'Статистика системи в реальному часі':'Estadísticas del sistema en tiempo real', 'Завантаження...':'Cargando...', "Інформація про ваш комп'ютер":'Información sobre tu ordenador', 'Операційна система:':'Sistema operativo:', 'Версія:':'Versión:', 'Фізичних ядер:':'Núcleos físicos:', 'Логічних процесорів:':'Procesadores lógicos:', "Ім'я ПК:":'Nombre del PC:', 'Використано:':'Usado:', 'Система':'Sistema'})
        self.translations['es'].update({'Процесор:':'Procesador:', "Оперативна пам'ять:":'Memoria RAM:', 'Фізичних ядер:':'Núcleos físicos:', 'Логічних процесорів:':'Procesadores lógicos:'})

        self.translations['en'].update({'⚡ Оптимізація': '⚡ Optimization', 'Інструменти для покращення продуктивності': 'Tools to improve performance', '🧠 Оптимізація RAM': '🧠 RAM Optimization', "Очищення пам'яті Python": 'Python memory cleanup', '🚀 Швидка оптимізація': '🚀 Quick Optimization', 'Безпечний набір оптимізацій': 'Safe set of optimizations', '🔋 Висока продуктивність': '🔋 High Performance', 'Активувати High Performance': 'Activate High Performance', '🚀 ULTIMATE PERFORMANCE': '🚀 ULTIMATE PERFORMANCE', 'Створити, знайти та активувати план Ultimate Performance': 'Create, find and activate Ultimate Performance plan', '📡 Телеметрія Windows': '📡 Windows Telemetry', 'Обмежити діагностичні дані': 'Limit diagnostic data', '🧹 Очищення': '🧹 Cleaning', 'Видалення непотрібних тимчасових файлів': 'Remove unnecessary temporary files', '🧹 Очистити TEMP': '🧹 Clean TEMP', 'Видалити тимчасові файли користувача': 'Delete user temporary files', '🗑️ Очистити кошик': '🗑️ Empty Recycle Bin', 'Очистити кошик Windows': 'Empty Windows Recycle Bin', '🌐 Очистити DNS': '🌐 Flush DNS', 'Очистити DNS cache': 'Clear DNS cache', '🎮 Ігровий режим': '🎮 Game Mode', 'Підготовка системи до запуску гри': 'Preparing the system for gaming', '🎮 TURBO GAME MODE': '🎮 TURBO GAME MODE', 'Активувати режим для гри': 'Activate gaming mode', '🚀 Ultimate Performance': '🚀 Ultimate Performance', 'Активувати максимальну продуктивність': 'Activate maximum performance', '🖥️ Система': '🖥️ System', "Інформація про ваш комп'ютер": 'Information about your computer', '🔧 Інструменти': '🔧 Tools', 'Корисні інструменти Windows': 'Useful Windows tools', '📋 Диспетчер завдань': '📋 Task Manager', 'Відкрити Task Manager': 'Open Task Manager', '⚙️ Windows Update': '⚙️ Windows Update', 'Відкрити Windows Update': 'Open Windows Update', '🛠️ SFC /scannow': '🛠️ SFC /scannow', 'Перевірити системні файли Windows': 'Check Windows system files', '📝 Зберегти звіт': '📝 Save Report', 'Створити звіт про систему': 'Create system report', '🧠 Оптимізувати RAM': '🧠 Optimize RAM', 'Очистити TEMP': 'Clean TEMP', 'Game Mode': 'Game Mode', 'Повна оптимізація': 'Full Optimization', 'Інформація про ПК': 'PC Information', 'Перевірити Windows': 'Check Windows', 'СКАНУВАТИ СИСТЕМУ': 'SCAN SYSTEM', 'ЗАПУСТИТИ': 'RUN', 'ГОЛОВНЕ МЕНЮ': 'MAIN MENU', 'Швидкі дії': 'Quick Actions', 'Плани живлення': 'Power Plans', 'Показати плани живлення': 'Show Power Plans', 'Створити / активувати': 'Create / Activate', 'Статус: перевірка...': 'Status: checking...', 'Статус: план ще не створено': 'Status: plan not created', 'Автоматично створити та активувати план максимальної продуктивності': 'Automatically create and activate the maximum performance plan', 'Програма перевірить наявні плани живлення,\nстворить Ultimate Performance, якщо його немає,\nзнайде його GUID і автоматично активує.': 'The program checks power plans,\ncreates Ultimate Performance if needed,\nfinds its GUID and activates it automatically.', '🚀 СТВОРИТИ / АКТИВУВАТИ ULTIMATE PERFORMANCE': '🚀 CREATE / ACTIVATE ULTIMATE PERFORMANCE', '📋 Показати плани живлення': '📋 Show Power Plans', 'Процесор': 'CPU', "Оперативна пам'ять": 'RAM', 'Диск (C:)': 'Disk (C:)', 'Система': 'System'})
        self.translations['pl'].update({'⚡ Оптимізація': '⚡ Optymalizacja', 'Інструменти для покращення продуктивності': 'Narzędzia poprawiające wydajność', '🧠 Оптимізація RAM': '🧠 Optymalizacja RAM', "Очищення пам'яті Python": 'Czyszczenie pamięci Pythona', '🚀 Швидка оптимізація': '🚀 Szybka optymalizacja', 'Безпечний набір оптимізацій': 'Bezpieczny zestaw optymalizacji', '🔋 Висока продуктивність': '🔋 Wysoka wydajność', 'Активувати High Performance': 'Aktywuj High Performance', '🚀 ULTIMATE PERFORMANCE': '🚀 ULTIMATE PERFORMANCE', 'Створити, знайти та активувати план Ultimate Performance': 'Utwórz, znajdź i aktywuj plan Ultimate Performance', '📡 Телеметрія Windows': '📡 Telemetria Windows', 'Обмежити діагностичні дані': 'Ogranicz dane diagnostyczne', '🧹 Очищення': '🧹 Czyszczenie', 'Видалення непотрібних тимчасових файлів': 'Usuwanie niepotrzebnych plików tymczasowych', '🧹 Очистити TEMP': '🧹 Wyczyść TEMP', 'Видалити тимчасові файли користувача': 'Usuń tymczasowe pliki użytkownika', '🗑️ Очистити кошик': '🗑️ Opróżnij kosz', 'Очистити кошик Windows': 'Opróżnij Kosz Windows', '🌐 Очистити DNS': '🌐 Wyczyść DNS', 'Очистити DNS cache': 'Wyczyść pamięć podręczną DNS', '🎮 Ігровий режим': '🎮 Tryb gry', 'Підготовка системи до запуску гри': 'Przygotowanie systemu do gry', '🎮 TURBO GAME MODE': '🎮 TURBO GAME MODE', 'Активувати режим для гри': 'Aktywuj tryb gry', '🚀 Ultimate Performance': '🚀 Ultimate Performance', 'Активувати максимальну продуктивність': 'Aktywuj maksymalną wydajność', '🖥️ Система': '🖥️ System', "Інформація про ваш комп'ютер": 'Informacje o komputerze', '🔧 Інструменти': '🔧 Narzędzia', 'Корисні інструменти Windows': 'Przydatne narzędzia Windows', '📋 Диспетчер завдань': '📋 Menedżer zadań', 'Відкрити Task Manager': 'Otwórz Menedżera zadań', '⚙️ Windows Update': '⚙️ Windows Update', 'Відкрити Windows Update': 'Otwórz Windows Update', '🛠️ SFC /scannow': '🛠️ SFC /scannow', 'Перевірити системні файли Windows': 'Sprawdź pliki systemowe Windows', '📝 Зберегти звіт': '📝 Zapisz raport', 'Створити звіт про систему': 'Utwórz raport systemowy', '🧠 Оптимізувати RAM': '🧠 Optymalizuj RAM', 'Очистити TEMP': 'Wyczyść TEMP', 'Game Mode': 'Tryb gry', 'Повна оптимізація': 'Pełna optymalizacja', 'Інформація про ПК': 'Informacje o komputerze', 'Перевірити Windows': 'Sprawdź Windows', 'СКАНУВАТИ СИСТЕМУ': 'SKANUJ SYSTEM', 'ЗАПУСТИТИ': 'URUCHOM', 'ГОЛОВНЕ МЕНЮ': 'MENU GŁÓWNE', 'Швидкі дії': 'Szybkie akcje', 'Плани живлення': 'Plany zasilania', 'Показати плани живлення': 'Pokaż plany zasilania', 'Створити / активувати': 'Utwórz / Aktywuj', 'Статус: перевірка...': 'Status: sprawdzanie...', 'Статус: план ще не створено': 'Status: plan nie został utworzony', 'Автоматично створити та активувати план максимальної продуктивності': 'Automatycznie utwórz i aktywuj plan maksymalnej wydajności', 'Програма перевірить наявні плани живлення,\nстворить Ultimate Performance, якщо його немає,\nзнайде його GUID і автоматично активує.': 'Program sprawdzi plany zasilania,\nutworzy Ultimate Performance, jeśli go nie ma,\nznajdzie GUID i automatycznie go aktywuje.', '🚀 СТВОРИТИ / АКТИВУВАТИ ULTIMATE PERFORMANCE': '🚀 UTWÓRZ / AKTYWUJ ULTIMATE PERFORMANCE', '📋 Показати плани живлення': '📋 Pokaż plany zasilania', 'Процесор': 'Procesor', "Оперативна пам'ять": 'Pamięć RAM', 'Диск (C:)': 'Dysk (C:)', 'Система': 'System'})
        self.translations['de'].update({'⚡ Оптимізація': '⚡ Optimierung', 'Інструменти для покращення продуктивності': 'Werkzeuge zur Leistungssteigerung', '🧠 Оптимізація RAM': '🧠 RAM-Optimierung', "Очищення пам'яті Python": 'Python-Speicherbereinigung', '🚀 Швидка оптимізація': '🚀 Schnelloptimierung', 'Безпечний набір оптимізацій': 'Sicheres Optimierungspaket', '🔋 Висока продуктивність': '🔋 Hohe Leistung', 'Активувати High Performance': 'High Performance aktivieren', '🚀 ULTIMATE PERFORMANCE': '🚀 ULTIMATE PERFORMANCE', 'Створити, знайти та активувати план Ultimate Performance': 'Ultimate-Performance-Energiesparplan erstellen, finden und aktivieren', '📡 Телеметрія Windows': '📡 Windows-Telemetrie', 'Обмежити діагностичні дані': 'Diagnosedaten begrenzen', '🧹 Очищення': '🧹 Bereinigung', 'Видалення непотрібних тимчасових файлів': 'Unnötige temporäre Dateien entfernen', '🧹 Очистити TEMP': '🧹 TEMP leeren', 'Видалити тимчасові файли користувача': 'Temporäre Benutzerdaten löschen', '🗑️ Очистити кошик': '🗑️ Papierkorb leeren', 'Очистити кошик Windows': 'Windows-Papierkorb leeren', '🌐 Очистити DNS': '🌐 DNS leeren', 'Очистити DNS cache': 'DNS-Cache leeren', '🎮 Ігровий режим': '🎮 Gaming-Modus', 'Підготовка системи до запуску гри': 'System für Spiele vorbereiten', '🎮 TURBO GAME MODE': '🎮 TURBO GAME MODE', 'Активувати режим для гри': 'Gaming-Modus aktivieren', '🚀 Ultimate Performance': '🚀 Ultimate Performance', 'Активувати максимальну продуктивність': 'Maximale Leistung aktivieren', '🖥️ Система': '🖥️ System', "Інформація про ваш комп'ютер": 'Informationen über Ihren Computer', '🔧 Інструменти': '🔧 Werkzeuge', 'Корисні інструменти Windows': 'Nützliche Windows-Werkzeuge', '📋 Диспетчер завдань': '📋 Task-Manager', 'Відкрити Task Manager': 'Task-Manager öffnen', '⚙️ Windows Update': '⚙️ Windows Update', 'Відкрити Windows Update': 'Windows Update öffnen', '🛠️ SFC /scannow': '🛠️ SFC /scannow', 'Перевірити системні файли Windows': 'Windows-Systemdateien prüfen', '📝 Зберегти звіт': '📝 Bericht speichern', 'Створити звіт про систему': 'Systembericht erstellen', '🧠 Оптимізувати RAM': '🧠 RAM optimieren', 'Очистити TEMP': 'TEMP leeren', 'Game Mode': 'Gaming-Modus', 'Повна оптимізація': 'Vollständige Optimierung', 'Інформація про ПК': 'PC-Informationen', 'Перевірити Windows': 'Windows prüfen', 'СКАНУВАТИ СИСТЕМУ': 'SYSTEM SCANNEN', 'ЗАПУСТИТИ': 'STARTEN', 'ГОЛОВНЕ МЕНЮ': 'HAUPTMENÜ', 'Швидкі дії': 'Schnellaktionen', 'Плани живлення': 'Energiepläne', 'Показати плани живлення': 'Energiepläne anzeigen', 'Створити / активувати': 'Erstellen / Aktivieren', 'Статус: перевірка...': 'Status: Prüfung...', 'Статус: план ще не створено': 'Status: Plan noch nicht erstellt', 'Автоматично створити та активувати план максимальної продуктивності': 'Plan für maximale Leistung automatisch erstellen und aktivieren', '🚀 СТВОРИТИ / АКТИВУВАТИ ULTIMATE PERFORMANCE': '🚀 ULTIMATE PERFORMANCE ERSTELLEN / AKTIVIEREN', '📋 Показати плани живлення': '📋 Energiepläne anzeigen', 'Процесор': 'Prozessor', "Оперативна пам'ять": 'Arbeitsspeicher', 'Диск (C:)': 'Laufwerk (C:)', 'Система': 'System'})
        self.translations['es'].update({'⚡ Оптимізація': '⚡ Optimización', 'Інструменти для покращення продуктивності': 'Herramientas para mejorar el rendimiento', '🧠 Оптимізація RAM': '🧠 Optimización de RAM', "Очищення пам'яті Python": 'Limpieza de memoria de Python', '🚀 Швидка оптимізація': '🚀 Optimización rápida', 'Безпечний набір оптимізацій': 'Conjunto seguro de optimizaciones', '🔋 Висока продуктивність': '🔋 Alto rendimiento', 'Активувати High Performance': 'Activar High Performance', '🚀 ULTIMATE PERFORMANCE': '🚀 ULTIMATE PERFORMANCE', 'Створити, знайти та активувати план Ultimate Performance': 'Crear, encontrar y activar el plan Ultimate Performance', '📡 Телеметрія Windows': '📡 Telemetría de Windows', 'Обмежити діагностичні дані': 'Limitar datos de diagnóstico', '🧹 Очищення': '🧹 Limpieza', 'Видалення непотрібних тимчасових файлів': 'Eliminar archivos temporales innecesarios', '🧹 Очистити TEMP': '🧹 Limpiar TEMP', 'Видалити тимчасові файли користувача': 'Eliminar archivos temporales del usuario', '🗑️ Очистити кошик': '🗑️ Vaciar papelera', 'Очистити кошик Windows': 'Vaciar la papelera de Windows', '🌐 Очистити DNS': '🌐 Vaciar DNS', 'Очистити DNS cache': 'Limpiar caché DNS', '🎮 Ігровий режим': '🎮 Modo juego', 'Підготовка системи до запуску гри': 'Preparar el sistema para jugar', '🎮 TURBO GAME MODE': '🎮 TURBO GAME MODE', 'Активувати режим для гри': 'Activar modo juego', '🚀 Ultimate Performance': '🚀 Ultimate Performance', 'Активувати максимальну продуктивність': 'Activar máximo rendimiento', '🖥️ Система': '🖥️ Sistema', "Інформація про ваш комп'ютер": 'Información de tu ordenador', '🔧 Інструменти': '🔧 Herramientas', 'Корисні інструменти Windows': 'Herramientas útiles de Windows', '📋 Диспетчер завдань': '📋 Administrador de tareas', 'Відкрити Task Manager': 'Abrir Administrador de tareas', '⚙️ Windows Update': '⚙️ Windows Update', 'Відкрити Windows Update': 'Abrir Windows Update', '🛠️ SFC /scannow': '🛠️ SFC /scannow', 'Перевірити системні файли Windows': 'Comprobar archivos del sistema de Windows', '📝 Зберегти звіт': '📝 Guardar informe', 'Створити звіт про систему': 'Crear informe del sistema', '🧠 Оптимізувати RAM': '🧠 Optimizar RAM', 'Очистити TEMP': 'Limpiar TEMP', 'Game Mode': 'Modo juego', 'Повна оптимізація': 'Optimización completa', 'Інформація про ПК': 'Información del PC', 'Перевірити Windows': 'Comprobar Windows', 'СКАНУВАТИ СИСТЕМУ': 'ESCANEAR SISTEMA', 'ЗАПУСТИТИ': 'EJECUTAR', 'ГОЛОВНЕ МЕНЮ': 'MENÚ PRINCIPAL', 'Швидкі дії': 'Acciones rápidas', 'Плани живлення': 'Planes de energía', 'Показати плани живлення': 'Mostrar planes de energía', 'Створити / активувати': 'Crear / Activar', 'Статус: перевірка...': 'Estado: comprobando...', 'Статус: план ще не створено': 'Estado: plan aún no creado', 'Автоматично створити та активувати план максимальної продуктивності': 'Crear y activar automáticamente el plan de máximo rendimiento', '🚀 СТВОРИТИ / АКТИВУВАТИ ULTIMATE PERFORMANCE': '🚀 CREAR / ACTIVAR ULTIMATE PERFORMANCE', '📋 Показати плани живлення': '📋 Mostrar planes de energía', 'Процесор': 'Procesador', "Оперативна пам'ять": 'Memoria RAM', 'Диск (C:)': 'Disco (C:)', 'Система': 'Sistema'})


        self.translations['en'].update({'🧹 Очищення диска Windows': '🧹 Windows Disk Cleanup', 'Запустити стандартний Disk Cleanup': 'Run the standard Windows Disk Cleanup', '💾 Storage Sense': '💾 Storage Sense', "Відкрити автоматичне очищення пам'яті Windows": 'Open Windows automatic storage cleanup', '🚀 Програми автозапуску': '🚀 Startup Apps', 'Відкрити керування автозапуском Windows': 'Open Windows startup app management', '💿 Оптимізація дисків': '💿 Optimize Drives', 'Відкрити стандартний Optimize Drives': 'Open the standard Optimize Drives tool', '🖼️ Очистити кеш ескізів': '🖼️ Clear Thumbnail Cache', 'Видалити кеш мініатюр Windows': 'Delete the Windows thumbnail cache', '💽 Стан дисків': '💽 Drive Health', 'Перевірити базовий HealthStatus фізичних дисків': 'Check basic physical drive health', '🛠️ DISM RestoreHealth': '🛠️ DISM RestoreHealth', 'Відновити компоненти Windows через DISM': 'Repair Windows components with DISM'})
        self.translations['pl'].update({'🧹 Очищення диска Windows': '🧹 Oczyszczanie dysku Windows', 'Запустити стандартний Disk Cleanup': 'Uruchom standardowe Oczyszczanie dysku', '💾 Storage Sense': '💾 Czujnik pamięci', "Відкрити автоматичне очищення пам'яті Windows": 'Otwórz automatyczne czyszczenie pamięci Windows', '🚀 Програми автозапуску': '🚀 Aplikacje startowe', 'Відкрити керування автозапуском Windows': 'Otwórz zarządzanie aplikacjami startowymi', '💿 Оптимізація дисків': '💿 Optymalizacja dysków', 'Відкрити стандартний Optimize Drives': 'Otwórz narzędzie optymalizacji dysków', '🖼️ Очистити кеш ескізів': '🖼️ Wyczyść pamięć miniaturek', 'Видалити кеш мініатюр Windows': 'Usuń pamięć podręczną miniaturek Windows', '💽 Стан дисків': '💽 Stan dysków', 'Перевірити базовий HealthStatus фізичних дисків': 'Sprawdź podstawowy stan dysków fizycznych', '🛠️ DISM RestoreHealth': '🛠️ DISM RestoreHealth', 'Відновити компоненти Windows через DISM': 'Napraw składniki Windows za pomocą DISM'})
        self.translations['de'].update({'🧹 Очищення диска Windows': '🧹 Windows-Datenträgerbereinigung', 'Запустити стандартний Disk Cleanup': 'Standard-Datenträgerbereinigung starten', '💾 Storage Sense': '💾 Speicheroptimierung', "Відкрити автоматичне очищення пам'яті Windows": 'Automatische Speicherbereinigung öffnen', '🚀 Програми автозапуску': '🚀 Autostart-Apps', 'Відкрити керування автозапуском Windows': 'Autostart-Verwaltung öffnen', '💿 Оптимізація дисків': '💿 Laufwerke optimieren', 'Відкрити стандартний Optimize Drives': 'Standardtool zum Optimieren von Laufwerken öffnen', '🖼️ Очистити кеш ескізів': '🖼️ Miniaturcache leeren', 'Видалити кеш мініатюр Windows': 'Windows-Miniaturcache löschen', '💽 Стан дисків': '💽 Laufwerkszustand', 'Перевірити базовий HealthStatus фізичних дисків': 'Grundlegenden Zustand physischer Laufwerke prüfen', '🛠️ DISM RestoreHealth': '🛠️ DISM RestoreHealth', 'Відновити компоненти Windows через DISM': 'Windows-Komponenten mit DISM reparieren'})
        self.translations['es'].update({'🧹 Очищення диска Windows': '🧹 Limpieza de disco de Windows', 'Запустити стандартний Disk Cleanup': 'Ejecutar la limpieza de disco estándar', '💾 Storage Sense': '💾 Sensor de almacenamiento', "Відкрити автоматичне очищення пам'яті Windows": 'Abrir la limpieza automática de almacenamiento', '🚀 Програми автозапуску': '🚀 Aplicaciones de inicio', 'Відкрити керування автозапуском Windows': 'Abrir la gestión de aplicaciones de inicio', '💿 Оптимізація дисків': '💿 Optimizar unidades', 'Відкрити стандартний Optimize Drives': 'Abrir la herramienta estándar Optimizar unidades', '🖼️ Очистити кеш ескізів': '🖼️ Limpiar caché de miniaturas', 'Видалити кеш мініатюр Windows': 'Eliminar la caché de miniaturas de Windows', '💽 Стан дисків': '💽 Estado de discos', 'Перевірити базовий HealthStatus фізичних дисків': 'Comprobar el estado básico de los discos físicos', '🛠️ DISM RestoreHealth': '🛠️ DISM RestoreHealth', 'Відновити компоненти Windows через DISM': 'Reparar componentes de Windows con DISM'})


        self.translations['en'].update({'SYSTEM DIAGNOSTICS': 'SYSTEM DIAGNOSTICS', '🧩 Device Manager': '🧩 Device Manager', 'Відкрити Диспетчер пристроїв': 'Open Device Manager', '📜 Event Viewer': '📜 Event Viewer', 'Переглянути журнали подій Windows': 'View Windows event logs', '📈 Resource Monitor': '📈 Resource Monitor', 'Відкрити монітор ресурсів Windows': 'Open Windows Resource Monitor', 'ℹ️ System Information': 'ℹ️ System Information', 'Відкрити повну інформацію про систему': 'Open detailed system information', '💽 Disk Management': '💽 Disk Management', 'Відкрити керування дисками': 'Open Disk Management', '⚙️ Services': '⚙️ Services', 'Відкрити служби Windows': 'Open Windows Services', '📊 Reliability Monitor': '📊 Reliability Monitor', 'Відкрити журнал стабільності Windows': 'Open Windows reliability history', '📦 Installed Apps': '📦 Installed Apps', 'Показати список встановлених програм': 'Show installed applications', '🚀 Startup Entries': '🚀 Startup Entries', 'Показати записи автозапуску без змін': 'Show startup entries without changing them', '🌐 Network Test': '🌐 Network Test', 'Перевірити доступ до мережі та DNS': 'Test network connectivity and DNS', '📝 Advanced Report': '📝 Advanced Report', 'Створити детальний діагностичний звіт': 'Create a detailed diagnostic report'})
        self.translations['pl'].update({'SYSTEM DIAGNOSTICS': 'DIAGNOSTYKA SYSTEMU', '🧩 Device Manager': '🧩 Menedżer urządzeń', 'Відкрити Диспетчер пристроїв': 'Otwórz Menedżer urządzeń', '📜 Event Viewer': '📜 Podgląd zdarzeń', 'Переглянути журнали подій Windows': 'Wyświetl dzienniki zdarzeń Windows', '📈 Resource Monitor': '📈 Monitor zasobów', 'Відкрити монітор ресурсів Windows': 'Otwórz Monitor zasobów Windows', 'ℹ️ System Information': 'ℹ️ Informacje o systemie', 'Відкрити повну інформацію про систему': 'Otwórz szczegółowe informacje o systemie', '💽 Disk Management': '💽 Zarządzanie dyskami', 'Відкрити керування дисками': 'Otwórz Zarządzanie dyskami', '⚙️ Services': '⚙️ Usługi', 'Відкрити служби Windows': 'Otwórz usługi Windows', '📊 Reliability Monitor': '📊 Monitor niezawodności', 'Відкрити журнал стабільності Windows': 'Otwórz historię niezawodności Windows', '📦 Installed Apps': '📦 Zainstalowane programy', 'Показати список встановлених програм': 'Pokaż zainstalowane programy', '🚀 Startup Entries': '🚀 Wpisy autostartu', 'Показати записи автозапуску без змін': 'Pokaż wpisy autostartu bez zmian', '🌐 Network Test': '🌐 Test sieci', 'Перевірити доступ до мережі та DNS': 'Sprawdź sieć i DNS', '📝 Advanced Report': '📝 Raport rozszerzony', 'Створити детальний діагностичний звіт': 'Utwórz szczegółowy raport diagnostyczny'})
        self.translations['de'].update({'SYSTEM DIAGNOSTICS': 'SYSTEMDIAGNOSE', '🧩 Device Manager': '🧩 Geräte-Manager', 'Відкрити Диспетчер пристроїв': 'Geräte-Manager öffnen', '📜 Event Viewer': '📜 Ereignisanzeige', 'Переглянути журнали подій Windows': 'Windows-Ereignisprotokolle anzeigen', '📈 Resource Monitor': '📈 Ressourcenmonitor', 'Відкрити монітор ресурсів Windows': 'Windows-Ressourcenmonitor öffnen', 'ℹ️ System Information': 'ℹ️ Systeminformationen', 'Відкрити повну інформацію про систему': 'Detaillierte Systeminformationen öffnen', '💽 Disk Management': '💽 Datenträgerverwaltung', 'Відкрити керування дисками': 'Datenträgerverwaltung öffnen', '⚙️ Services': '⚙️ Dienste', 'Відкрити служби Windows': 'Windows-Dienste öffnen', '📊 Reliability Monitor': '📊 Zuverlässigkeitsverlauf', 'Відкрити журнал стабільності Windows': 'Windows-Zuverlässigkeitsverlauf öffnen', '📦 Installed Apps': '📦 Installierte Apps', 'Показати список встановлених програм': 'Installierte Programme anzeigen', '🚀 Startup Entries': '🚀 Autostart-Einträge', 'Показати записи автозапуску без змін': 'Autostart-Einträge nur anzeigen', '🌐 Network Test': '🌐 Netzwerktest', 'Перевірити доступ до мережі та DNS': 'Netzwerk und DNS testen', '📝 Advanced Report': '📝 Erweiterter Bericht', 'Створити детальний діагностичний звіт': 'Detaillierten Diagnosebericht erstellen'})
        self.translations['es'].update({'SYSTEM DIAGNOSTICS': 'DIAGNÓSTICO DEL SISTEMA', '🧩 Device Manager': '🧩 Administrador de dispositivos', 'Відкрити Диспетчер пристроїв': 'Abrir Administrador de dispositivos', '📜 Event Viewer': '📜 Visor de eventos', 'Переглянути журнали подій Windows': 'Ver registros de eventos de Windows', '📈 Resource Monitor': '📈 Monitor de recursos', 'Відкрити монітор ресурсів Windows': 'Abrir Monitor de recursos de Windows', 'ℹ️ System Information': 'ℹ️ Información del sistema', 'Відкрити повну інформацію про систему': 'Abrir información detallada del sistema', '💽 Disk Management': '💽 Administración de discos', 'Відкрити керування дисками': 'Abrir Administración de discos', '⚙️ Services': '⚙️ Servicios', 'Відкрити служби Windows': 'Abrir Servicios de Windows', '📊 Reliability Monitor': '📊 Monitor de confiabilidad', 'Відкрити журнал стабільності Windows': 'Abrir historial de confiabilidad de Windows', '📦 Installed Apps': '📦 Aplicaciones instaladas', 'Показати список встановлених програм': 'Mostrar aplicaciones instaladas', '🚀 Startup Entries': '🚀 Entradas de inicio', 'Показати записи автозапуску без змін': 'Mostrar entradas de inicio sin modificarlas', '🌐 Network Test': '🌐 Prueba de red', 'Перевірити доступ до мережі та DNS': 'Comprobar la red y DNS', '📝 Advanced Report': '📝 Informe avanzado', 'Створити детальний діагностичний звіт': 'Crear un informe de diagnóstico detallado'})

    def tr(self, key):
        """Return the translated text without recursively calling tr()."""
        try:
            lang_table = self.translations.get(self.lang, {})
            return lang_table.get(key, key)
        except Exception:
            return key


    def change_language(self, value):
        """Change language and refresh the current page safely."""
        self.lang = self.languages.get(value, "uk")

        icons = {
            "Панель керування": "🏠",
            "Оптимізація": "⚡",
            "Очищення": "🧹",
            "Ігровий режим": "🎮",
            "Ultimate Performance": "🚀",
            "Система": "🖥️",
            "Моніторинг": "📊",
            "Інструменти": "🔧",
        }

        for name, button in self.menu_buttons.items():
            button.configure(
                text=f"{icons.get(name, '•')}    {self.tr(name)}"
            )

        current = getattr(self, "_current_page", "Панель керування")
        if hasattr(self, "content"):
            self.show_page(current)
        else:
            self.page_title.configure(text=self.tr(current))

    # =========================================================
    # SIDEBAR
    # =========================================================
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=245, corner_radius=0, fg_color="#0A1120"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        logo = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo.pack(padx=20, pady=(25, 5), fill="x")

        ctk.CTkLabel(logo, text="🚀", font=ctk.CTkFont(size=34)).pack(side="left")
        ctk.CTkLabel(
            logo, text="Windows\nOptimizer",
            font=ctk.CTkFont(size=20, weight="bold"), anchor="w"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            self.sidebar, text="ULTRA 6.2.1", text_color="#4EA1FF",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=72)

        ctk.CTkLabel(
            self.sidebar, text=f"  {self.tr('ГОЛОВНЕ МЕНЮ')}",
            text_color="#65748B", font=ctk.CTkFont(size=11, weight="bold")
        ).pack(anchor="w", padx=15, pady=(30, 8))

        menu_items = [
            ("🏠", "Панель керування"),
            ("⚡", "Оптимізація"),
            ("🧹", "Очищення"),
            ("🎮", "Ігровий режим"),
            ("🚀", "Ultimate Performance"),
            ("🖥️", "Система"),
            ("📊", "Моніторинг"),
            ("🔧", "Інструменти"),
        ]

        for icon, name in menu_items:
            button = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}    {self.tr(name)}",
                anchor="w",
                height=44,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#17253D",
                text_color="#D9E2F2",
                font=ctk.CTkFont(size=13, weight="bold"),
                command=lambda n=name: self.show_page(n)
            )
            button.pack(fill="x", padx=12, pady=2)
            self.menu_buttons[name] = button

        bottom = ctk.CTkFrame(
            self.sidebar, fg_color="#111B2D", corner_radius=12
        )
        bottom.pack(side="bottom", fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            bottom, text=self.tr("Система"), text_color="#4EA1FF",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 3))

        ctk.CTkLabel(
            bottom, text=f"{platform.system()} {platform.release()}",
            text_color="#C8D1E0", font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=15)

        cpu = platform.processor() or self.tr("CPU не визначено")
        if len(cpu) > 28:
            cpu = cpu[:28] + "..."

        ctk.CTkLabel(
            bottom, text=cpu, text_color="#8190A6",
            font=ctk.CTkFont(size=10)
        ).pack(anchor="w", padx=15, pady=(2, 12))

    # =========================================================
    # MAIN
    # =========================================================
    def create_main_area(self):
        self.main = ctk.CTkFrame(
            self, fg_color="#08111F", corner_radius=0
        )
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        self.topbar = ctk.CTkFrame(
            self.main, height=65, fg_color="#0D1728", corner_radius=0
        )
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_propagate(False)

        self.page_title = ctk.CTkLabel(
            self.topbar, text=self.tr("Панель керування"),
            font=ctk.CTkFont(size=23, weight="bold")
        )
        self.page_title.pack(side="left", padx=30)

        self.clock_label = ctk.CTkLabel(
            self.topbar, text="", text_color="#7D8DA5",
            font=ctk.CTkFont(size=12)
        )
        self.clock_label.pack(side="right", padx=15)

        self.language_menu = ctk.CTkOptionMenu(
            self.topbar,
            values=list(self.languages.keys()),
            width=165,
            height=34,
            command=self.change_language
        )
        self.language_menu.set("🇺🇦 Українська")
        self.language_menu.pack(side="right", padx=10)

        self.update_clock()

        self.content = ctk.CTkScrollableFrame(
            self.main, fg_color="#08111F", corner_radius=0
        )
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)

    def update_clock(self):
        if not self.winfo_exists():
            return
        self.clock_label.configure(
            text=datetime.now().strftime("%d.%m.%Y   %H:%M:%S")
        )
        self.after(1000, self.update_clock)

    # =========================================================
    # PAGE SYSTEM
    # =========================================================
    def show_page(self, page_name):
        self._current_page = page_name
        for name, button in self.menu_buttons.items():
            if name == page_name:
                button.configure(fg_color="#1769D1", hover_color="#1D78E8")
            else:
                button.configure(fg_color="transparent", hover_color="#17253D")

        for widget in self.content.winfo_children():
            widget.destroy()

        self.page_title.configure(text=self.tr(page_name))

        pages = {
            "Панель керування": self.dashboard_page,
            "Оптимізація": self.optimization_page,
            "Очищення": self.cleaning_page,
            "Ігровий режим": self.game_page,
            "Ultimate Performance": self.ultimate_page,
            "Система": self.system_page,
            "Моніторинг": self.monitor_page,
            "Інструменти": self.tools_page,
        }

        pages.get(page_name, self.dashboard_page)()

    # =========================================================
    # DASHBOARD
    # =========================================================
    def dashboard_page(self):
        welcome = ctk.CTkFrame(
            self.content, fg_color="#101C2F", corner_radius=18
        )
        welcome.grid(row=0, column=0, sticky="ew", padx=25, pady=25)

        ctk.CTkLabel(
            welcome, text=self.tr("Вітаємо! 👋"),
            font=ctk.CTkFont(size=30, weight="bold")
        ).pack(anchor="w", padx=25, pady=(20, 3))

        ctk.CTkLabel(
            welcome,
            text=self.tr("Оптимізуйте свій ПК для максимальної продуктивності!"),
            text_color="#8291A8", font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=25, pady=(0, 20))

        stats = ctk.CTkFrame(self.content, fg_color="transparent")
        stats.grid(row=1, column=0, sticky="ew", padx=25)
        stats.grid_columnconfigure((0, 1, 2), weight=1)

        self.cpu_card = self.create_stat_card(stats, 0, "🧠", self.tr("Процесор"), "0%")
        self.ram_card = self.create_stat_card(stats, 1, "💾", self.tr("Оперативна пам'ять"), "0%")
        self.disk_card = self.create_stat_card(stats, 2, "💿", self.tr("Диск (C:)"), "0%")

        ctk.CTkLabel(
            self.content, text=self.tr("Швидкі дії"),
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=2, column=0, sticky="w", padx=30, pady=(30, 10))

        quick = ctk.CTkFrame(
            self.content, fg_color="#101C2F", corner_radius=18
        )
        quick.grid(row=3, column=0, sticky="ew", padx=25)
        quick.grid_columnconfigure((0, 1, 2, 3), weight=1)

        actions = [
            ("🧠", "Оптимізувати RAM", self.clean_ram),
            ("🧹", "Очистити TEMP", self.clean_temp),
            ("🎮", "Game Mode", lambda: self.show_page("Ігровий режим")),
            ("🚀", "Ultimate Performance", lambda: self.activate_ultimate_performance()),
            ("🌐", "Очистити DNS", self.flush_dns),
            ("🖥️", "Інформація про ПК", lambda: self.show_page("Система")),
            ("🛠️", "Перевірити Windows", self.check_windows),
            ("⚡", "Повна оптимізація", self.full_optimize),
        ]

        for i, (icon, text, command) in enumerate(actions):
            button = ctk.CTkButton(
                quick, text=f"{icon}\n{self.tr(text)}", height=74,
                corner_radius=14, fg_color="#13223A",
                hover_color="#1D3150",
                font=ctk.CTkFont(size=12, weight="bold"),
                command=command
            )
            button.grid(
                row=i // 4, column=i % 4,
                padx=8, pady=8, sticky="ew"
            )

        ctk.CTkButton(
            self.content, text=f"🔍  {self.tr("СКАНУВАТИ СИСТЕМУ")}",
            height=58, corner_radius=16,
            fg_color="#1769D1", hover_color="#2180F5",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.scan_system
        ).grid(row=4, column=0, sticky="ew", padx=25, pady=30)

    def create_stat_card(self, parent, column, icon, title, value):
        card = ctk.CTkFrame(
            parent, fg_color="#101C2F", corner_radius=18
        )
        card.grid(row=0, column=column, padx=7, sticky="ew")

        ctk.CTkLabel(
            card, text=icon, font=ctk.CTkFont(size=30)
        ).pack(anchor="w", padx=20, pady=(18, 3))

        ctk.CTkLabel(
            card, text=title, text_color="#9AA8BC",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=20)

        label = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=30, weight="bold")
        )
        label.pack(anchor="w", padx=20, pady=(3, 18))
        return label

    # =========================================================
    # OPTIMIZATION
    # =========================================================
    def optimization_page(self):
        self.create_page_title(self.tr("⚡ Оптимізація"), self.tr("Інструменти для покращення продуктивності"))
        self.create_action(self.tr("🧠 Оптимізація RAM"), self.tr("Очищення пам'яті Python"), self.clean_ram)
        self.create_action(self.tr("🚀 Швидка оптимізація"), self.tr("Безпечний набір оптимізацій"), self.quick_optimize)
        self.create_action(self.tr("🔋 Висока продуктивність"), self.tr("Активувати High Performance"), self.high_performance)
        self.create_action(self.tr("🚀 ULTIMATE PERFORMANCE"), self.tr("Створити, знайти та активувати план Ultimate Performance"), self.activate_ultimate_performance)
        self.create_action(self.tr("📡 Телеметрія Windows"), self.tr("Обмежити діагностичні дані"), self.show_telemetry_window)

    # =========================================================
    # ULTIMATE PERFORMANCE
    # =========================================================
    def ultimate_page(self):
        self.create_page_title(
            self.tr("🚀 Ultimate Performance"),
            self.tr("Автоматично створити та активувати план максимальної продуктивності")
        )

        card = ctk.CTkFrame(
            self.content, fg_color="#101C2F", corner_radius=16
        )
        card.grid(row=1, column=0, sticky="ew", padx=25, pady=20)

        ctk.CTkLabel(
            card,
            text=self.tr("🚀 ULTIMATE PERFORMANCE"),
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(25, 8))

        ctk.CTkLabel(
            card,
            text=self.tr("Програма перевірить наявні плани живлення,\nстворить Ultimate Performance, якщо його немає,\nзнайде його GUID і автоматично активує."),
            text_color="#8291A8",
            justify="center"
        ).pack(pady=5)

        self.power_status = ctk.CTkLabel(
            card, text=self.tr("Статус: перевірка..."),
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.power_status.pack(pady=15)

        ctk.CTkButton(
            card,
            text=self.tr("🚀 СТВОРИТИ / АКТИВУВАТИ ULTIMATE PERFORMANCE"),
            height=55,
            corner_radius=12,
            fg_color="#1769D1",
            hover_color="#2180F5",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.activate_ultimate_performance
        ).pack(fill="x", padx=35, pady=15)

        ctk.CTkButton(
            card,
            text=self.tr("📋 Показати плани живлення"),
            height=45,
            fg_color="#18263A",
            hover_color="#223650",
            command=self.show_power_plans
        ).pack(fill="x", padx=35, pady=(0, 30))

        self.update_power_status()

    def get_power_plans(self):
        result = run_command("powercfg /list")
        if not result or result.returncode != 0:
            return []
        plans = []
        for line in result.stdout.splitlines():
            m = re.search(
                r"([0-9a-fA-F-]{36}).*?\((.*?)\)",
                line
            )
            if m:
                plans.append((m.group(1), m.group(2).strip()))
        return plans

    def is_ultimate_plan_name(self, name):
        value = (name or "").strip().casefold()
        known = (
            "ultimate performance",
            "максимальна продуктивність",
            "najwyższa wydajność",
            "ultimative leistung",
            "máximo rendimiento",
            "rendimiento máximo",
        )
        return any(item.casefold() in value for item in known)

    def is_admin(self):
        """Перевіряє, чи програма запущена від адміністратора."""
        try:
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def restart_as_admin(self, extra_arg=None):
        """Перезапускає Optimizer з UAC-правами адміністратора."""
        try:
            import ctypes
            args = []
            if not getattr(sys, "frozen", False):
                args.append(os.path.abspath(sys.argv[0]))
            args.extend(a for a in sys.argv[1:] if a != "--ultimate")
            if extra_arg:
                args.append(extra_arg)
            params = " ".join(f'"{a}"' for a in args)
            result = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params or None, None, 1
            )
            if result <= 32:
                raise RuntimeError(f"ShellExecuteW code: {result}")
            self.after(250, self.destroy)
            return True
        except Exception as e:
            self.show_message(
                self.tr("🔐 Права адміністратора"),
                f"{self.tr('Не вдалося запустити від адміністратора:')}\n\n{e}"
            )
            return False


    def activate_ultimate_performance(self):
        """Створює Ultimate Performance, бере GUID з powercfg і активує його."""
        try:
            # Це системна зміна. Якщо EXE/скрипт не має прав — автоматично показуємо UAC.
            if not self.is_admin():
                self.show_message(
                    self.tr("🔐 Потрібні права адміністратора"),
                    self.tr("Для створення плану живлення Windows потрібні права адміністратора.\n\nНатисни OK — програма перезапуститься з UAC і продовжить автоматично.")
                )
                self.restart_as_admin("--ultimate")
                return

            base_guid = "e9a42b02-d5df-448d-aa00-03f14749eb61"
            plans_before = self.get_power_plans()

            # Спочатку шукаємо вже створений план за назвою.
            ultimate = next(
                (p for p in plans_before if self.is_ultimate_plan_name(p[1])),
                None
            )

            guid = None
            name = "Ultimate Performance"

            if ultimate:
                guid, name = ultimate
            else:
                # Ключовий момент: НЕ намагаємося вгадувати назву після duplicate.
                # powercfg сам повертає GUID нового плану, незалежно від мови Windows.
                result = run_command(f"powercfg -duplicatescheme {base_guid}")

                if result:
                    output = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
                    matches = re.findall(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", output)
                    if matches:
                        # У duplicatescheme зазвичай спочатку зустрічається GUID нового плану.
                        guid = matches[0].lower()

                # Якщо stdout не містить GUID — пробуємо ще раз через /list.
                if not guid:
                    plans_after = self.get_power_plans()
                    # Відкидаємо старі плани й беремо новий GUID, якщо він з'явився.
                    old_guids = {g.lower() for g, _ in plans_before}
                    new_plans = [(g, n) for g, n in plans_after if g.lower() not in old_guids]
                    if new_plans:
                        guid, name = new_plans[-1]

            if not guid:
                self.show_message(
                    self.tr("🚀 Ultimate Performance"),
                    self.tr("Windows не повернула GUID нового плану.\n\nПеревір, що Windows дозволяє створювати плани живлення, і спробуй ще раз.")
                )
                return

            # Активуємо саме знайдений GUID.
            activate = run_command(f"powercfg /setactive {guid}")

            if not activate or activate.returncode != 0:
                details = ""
                if activate:
                    details = (activate.stderr or activate.stdout or "").strip()
                self.show_message(
                    self.tr("🚀 Ultimate Performance"),
                    self.tr("План створено/знайдено, але Windows не дозволила його активувати.\n\n") + f"GUID: {guid}\n\n" + (details or self.tr("Спробуй ще раз від імені адміністратора."))
                )
                return

            if hasattr(self, "power_status") and self.power_status.winfo_exists():
                self.power_status.configure(
                    text=f"{self.tr('Статус: АКТИВНО')}\nGUID: {guid}",
                    text_color="#4CAF50"
                )

            self.show_message(
                self.tr("🚀 Ultimate Performance"),
                self.tr("Готово!\n\n") + f"{self.tr('План:')} {name}\nGUID: {guid}\n\n" + self.tr("Ultimate Performance успішно активовано.")
            )

        except Exception as e:
            self.show_message(self.tr("Помилка Ultimate Performance"), str(e))

    def update_power_status(self):
        if not hasattr(self, "power_status") or not self.power_status.winfo_exists():
            return

        plans = self.get_power_plans()
        active = None

        result = run_command("powercfg /getactivescheme")
        if result and result.returncode == 0:
            m = re.search(r"([0-9a-fA-F-]{36})", result.stdout)
            if m:
                active = m.group(1)

        ultimate = next(
            (p for p in plans if self.is_ultimate_plan_name(p[1])),
            None
        )

        if ultimate and active == ultimate[0]:
            self.power_status.configure(
                text=f"{self.tr('Статус: АКТИВНО')}\nGUID: {ultimate[0]}",
                text_color="#4CAF50"
            )
        elif ultimate:
            self.power_status.configure(
                text=f"{self.tr('Статус: створено, але не активовано')}\nGUID: {ultimate[0]}",
                text_color="#FFB74D"
            )
        else:
            self.power_status.configure(
                text=self.tr("Статус: план ще не створено"),
                text_color="#AAB7C9"
            )

    def show_power_plans(self):
        plans = self.get_power_plans()
        if not plans:
            self.show_message(self.tr("Плани живлення"), self.tr("Не вдалося отримати список планів."))
            return

        text = "\n".join(
            f"{'●' if self.is_active_guid(guid) else '○'} {name}\n   {guid}"
            for guid, name in plans
        )
        self.show_text_window(self.tr("📋 Плани живлення"), text)

    def is_active_guid(self, guid):
        result = run_command("powercfg /getactivescheme")
        if result and result.returncode == 0:
            return guid.lower() in result.stdout.lower()
        return False

    # =========================================================
    # CLEANING
    # =========================================================
    def cleaning_page(self):
        self.create_page_title(self.tr("🧹 Очищення"), self.tr("Видалення непотрібних тимчасових файлів"))
        self.create_action(self.tr("🧹 Очистити TEMP"), self.tr("Видалити тимчасові файли користувача"), self.clean_temp)
        self.create_action(self.tr("🗑️ Очистити кошик"), self.tr("Очистити кошик Windows"), self.empty_recycle)
        self.create_action(self.tr("🌐 Очистити DNS"), self.tr("Очистити DNS cache"), self.flush_dns)

    # =========================================================
    # GAME MODE
    # =========================================================
    def game_page(self):
        self.create_page_title(self.tr("🎮 Ігровий режим"), self.tr("Підготовка системи до запуску гри"))
        self.create_action(self.tr("🎮 TURBO GAME MODE"), self.tr("Активувати режим для гри"), self.game_mode)
        self.create_action(self.tr("🚀 Ultimate Performance"), self.tr("Активувати максимальну продуктивність"), self.activate_ultimate_performance)

    def game_mode(self):
        self.activate_ultimate_performance()

    # =========================================================
    # SYSTEM
    # =========================================================
    def system_page(self):
        self.create_page_title(self.tr("🖥️ Система"), self.tr("Інформація про ваш комп'ютер"))

        info = ctk.CTkTextbox(
            self.content, height=400, corner_radius=12,
            fg_color="#101C2F", font=ctk.CTkFont(size=13)
        )
        info.grid(row=1, column=0, sticky="ew", padx=25, pady=20)

        data = f"""WINDOWS OPTIMIZER ULTRA 6.2.1.1
────────────────────────────────

{self.tr("Операційна система:")}
{platform.system()} {platform.release()}

{self.tr("Версія:")}
{platform.version()}

{self.tr("Процесор:")}
{platform.processor()}

{self.tr("Фізичних ядер:")}
{__import__('psutil').cpu_count(logical=False)}

{self.tr("Логічних процесорів:")}
{__import__('psutil').cpu_count(logical=True)}

{self.tr("Оперативна пам'ять:")}
{__import__('psutil').virtual_memory().total / (1024**3):.2f} GB

{self.tr("Ім'я ПК:")}
{platform.node()}

Python:
{sys.version.split()[0]}
"""
        info.insert("1.0", data)
        info.configure(state="disabled")

    # =========================================================
    # MONITOR
    # =========================================================
    def monitor_page(self):
        self.create_page_title(self.tr("📊 Моніторинг"), self.tr("Статистика системи в реальному часі"))
        self.monitor_label = ctk.CTkLabel(
            self.content, text=self.tr("Завантаження..."),
            font=ctk.CTkFont(size=20)
        )
        self.monitor_label.grid(row=1, column=0, pady=50)
        self.update_monitor()

    def update_monitor(self):
        try:
            if not hasattr(self, "monitor_label") or not self.monitor_label.winfo_exists():
                return
        except Exception:
            return

        import psutil
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("C:\\").percent

        self.monitor_label.configure(
            text=(
                f"🧠 CPU: {cpu:.1f}%\n\n"
                f"💾 RAM: {ram.percent:.1f}%\n"
                f"{self.tr('Використано:')} {ram.used / (1024**3):.2f} GB\n\n"
                f"💿 {self.tr('Диск C:')} {disk:.1f}%"
            )
        )
        self.after(1000, self.update_monitor)

    # =========================================================
    # TOOLS
    # =========================================================
    def tools_page(self):
        self.create_page_title(self.tr("🔧 Інструменти"), self.tr("Корисні інструменти Windows"))
        self.create_action(self.tr("📋 Диспетчер завдань"), self.tr("Відкрити Task Manager"), self.open_task_manager)

        ctk.CTkLabel(
            self.content,
            text="SYSTEM REPAIR & TOOLS",
            text_color="#6E7F96",
            font=ctk.CTkFont(size=11, weight="bold")
        ).grid(column=0, sticky="w", padx=28, pady=(10, 4))
        self.create_action(self.tr("⚙️ Windows Update"), self.tr("Відкрити Windows Update"), self.windows_update)
        self.create_action(self.tr("🛠️ SFC /scannow"), self.tr("Перевірити системні файли Windows"), self.check_windows)
        self.create_action(self.tr("📝 Зберегти звіт"), self.tr("Створити звіт про систему"), self.save_report)
        self.create_action(self.tr("⚡ Chris Titus Utility"), self.tr("Офіційна Windows Utility"), self.chris_titus_utility)

        self.create_action(
            "🧹 Очищення диска Windows",
            "Запустити стандартний Disk Cleanup",
            self.run_disk_cleanup
        )

        self.create_action(
            "💾 Storage Sense",
            "Відкрити автоматичне очищення пам'яті Windows",
            self.open_storage_sense
        )

        self.create_action(
            "🚀 Програми автозапуску",
            "Відкрити керування автозапуском Windows",
            self.open_startup_apps
        )

        self.create_action(
            "💿 Оптимізація дисків",
            "Відкрити стандартний Optimize Drives",
            self.open_optimize_drives
        )

        self.create_action(
            "🖼️ Очистити кеш ескізів",
            "Видалити кеш мініатюр Windows",
            self.clear_thumbnail_cache
        )

        self.create_action(
            "💽 Стан дисків",
            "Перевірити базовий HealthStatus фізичних дисків",
            self.check_drive_health
        )

        self.create_action(
            "🛠️ DISM RestoreHealth",
            "Відновити компоненти Windows через DISM",
            self.run_dism_restorehealth
        )

        self.create_action("🛡️ Створити точку відновлення", "Створити Restore Point перед змінами", self.create_restore_point)
        self.create_action("🩺 DISM CheckHealth", "Швидка перевірка образу Windows", self.dism_checkhealth)
        self.create_action("🔎 DISM ScanHealth", "Повне сканування образу Windows", self.dism_scanhealth)
        self.create_action("💿 CHKDSK Scan", "Перевірити диск C: без автоматичного ремонту", self.chkdsk_scan)
        self.create_action("🔋 Battery Report", "Створити офіційний звіт Windows про батарею", self.battery_report)
        self.create_action("🧠 TOP CPU / RAM", "Показати процеси, які використовують найбільше пам'яті", self.top_processes)
        self.create_action("💾 Disk Analyzer", "Показати зайняте та вільне місце на дисках", self.disk_analyzer)
        self.create_action("🌐 Network Info", "Показати інформацію про мережеві адаптери", self.network_info)
        self.create_action("🛡️ Windows Security", "Відкрити Безпеку Windows", self.open_windows_security)

        ctk.CTkLabel(
            self.content,
            text=self.tr("SYSTEM DIAGNOSTICS"),
            text_color="#6E7F96",
            font=ctk.CTkFont(size=11, weight="bold")
        ).grid(column=0, sticky="w", padx=28, pady=(18, 4))

        self.create_action(self.tr("🧩 Device Manager"), self.tr("Відкрити Диспетчер пристроїв"), self.open_device_manager)
        self.create_action(self.tr("📜 Event Viewer"), self.tr("Переглянути журнали подій Windows"), self.open_event_viewer)
        self.create_action(self.tr("📈 Resource Monitor"), self.tr("Відкрити монітор ресурсів Windows"), self.open_resource_monitor)
        self.create_action(self.tr("ℹ️ System Information"), self.tr("Відкрити повну інформацію про систему"), self.open_system_information)
        self.create_action(self.tr("💽 Disk Management"), self.tr("Відкрити керування дисками"), self.open_disk_management)
        self.create_action(self.tr("⚙️ Services"), self.tr("Відкрити служби Windows"), self.open_services)
        self.create_action(self.tr("📊 Reliability Monitor"), self.tr("Відкрити журнал стабільності Windows"), self.open_reliability_monitor)
        self.create_action(self.tr("📦 Installed Apps"), self.tr("Показати список встановлених програм"), self.installed_apps)
        self.create_action(self.tr("🚀 Startup Entries"), self.tr("Показати записи автозапуску без змін"), self.startup_entries)
        self.create_action(self.tr("🌐 Network Test"), self.tr("Перевірити доступ до мережі та DNS"), self.network_quick_test)
        self.create_action(self.tr("📝 Advanced Report"), self.tr("Створити детальний діагностичний звіт"), self.advanced_report)

    def chris_titus_utility(self):
        if not messagebox.askyesno(
            "Chris Titus Utility",
            "Відкрити офіційну Chris Titus Windows Utility?\n\n"
            "PowerShell завантажить і виконає скрипт з christitus.com з правами адміністратора."
        ):
            return
        try:
            ps = "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command \"iwr https://christitus.com/win | iex\"'"
            subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", ps],
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
        except Exception as e:
            messagebox.showerror(self.tr("Помилка"), str(e))


    # =========================================================
    # TELEMETRY
    # =========================================================
    def show_telemetry_window(self):
        window = ctk.CTkToplevel(self)
        window.title(self.tr("📡 Телеметрія Windows"))
        window.geometry("560x430")
        window.resizable(False, False)
        window.transient(self)
        window.grab_set()

        ctk.CTkLabel(
            window, text=self.tr("📡 Телеметрія Windows"),
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(30, 10))

        status = ctk.CTkLabel(window, text=self.tr("Статус: перевірка..."))
        status.pack(pady=20)

        def get_status():
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                    0, winreg.KEY_READ
                )
                try:
                    value, _ = winreg.QueryValueEx(key, "AllowTelemetry")
                except FileNotFoundError:
                    value = None
                winreg.CloseKey(key)

                return {
                    0: self.tr("Вимкнено"), 1: self.tr("Обмежено"),
                    2: self.tr("Розширено"), 3: self.tr("Повне")
                }.get(value, self.tr("Стандарт Windows"))
            except Exception:
                return self.tr("Стандарт Windows")

        def refresh():
            status.configure(text=f"{self.tr('Статус: ')}{get_status()}")

        def limit_telemetry():
            try:
                key = winreg.CreateKeyEx(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                    0, winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(key, "AllowTelemetry", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                refresh()
                messagebox.showinfo(self.tr("📡 Телеметрія"), self.tr("Телеметрію встановлено в обмежений режим."))
            except PermissionError:
                messagebox.showerror(self.tr("🔐 Потрібні права адміністратора"), self.tr("Запусти Optimizer від імені адміністратора."))
            except Exception as e:
                messagebox.showerror(self.tr("Помилка"), str(e))

        def restore_telemetry():
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                    0, winreg.KEY_SET_VALUE
                )
                try:
                    winreg.DeleteValue(key, "AllowTelemetry")
                except FileNotFoundError:
                    pass
                winreg.CloseKey(key)
                refresh()
                messagebox.showinfo(self.tr("📡 Телеметрія"), self.tr("Стандартне налаштування Windows відновлено."))
            except FileNotFoundError:
                refresh()
            except PermissionError:
                messagebox.showerror(self.tr("🔐 Потрібні права адміністратора"), self.tr("Запусти Optimizer від імені адміністратора."))
            except Exception as e:
                messagebox.showerror(self.tr("Помилка"), str(e))

        ctk.CTkButton(
            window, text=self.tr("🔒 ВИМКНУТИ / ОБМЕЖИТИ ТЕЛЕМЕТРІЮ"),
            height=50, command=limit_telemetry
        ).pack(fill="x", padx=40, pady=10)

        ctk.CTkButton(
            window, text=self.tr("↩ Відновити стандартні налаштування"),
            height=45, fg_color="#18263A", hover_color="#223650",
            command=restore_telemetry
        ).pack(fill="x", padx=40, pady=5)

        ctk.CTkButton(
            window, text=self.tr("Закрити"), fg_color="transparent",
            command=window.destroy
        ).pack(pady=15)

        refresh()

    # =========================================================
    # ACTIONS
    # =========================================================
    def clean_ram(self):
        import psutil
        before = psutil.virtual_memory().percent
        gc.collect()
        after = psutil.virtual_memory().percent
        self.show_message(
            self.tr("🧠 Оптимізація RAM"),
            self.tr("Готово!\n\nRAM до: ") + f"{before:.1f}%" + self.tr("\nRAM після: ") + f"{after:.1f}%"
        )

    def clean_temp(self):
        folders = [tempfile.gettempdir()]
        deleted = 0

        for folder in folders:
            try:
                for name in os.listdir(folder):
                    path = os.path.join(folder, name)
                    try:
                        if os.path.isfile(path) or os.path.islink(path):
                            os.remove(path)
                            deleted += 1
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                            deleted += 1
                    except Exception:
                        pass
            except Exception:
                pass

        self.show_message(self.tr("🧹 Очищення TEMP"), self.tr("Готово!\n\nВидалено об'єктів: ") + str(deleted))

    def flush_dns(self):
        result = run_command("ipconfig /flushdns")
        self.show_message(
            self.tr("🌐 DNS"),
            self.tr("DNS cache успішно очищено!") if result and result.returncode == 0
            else self.tr("Не вдалося очистити DNS.")
        )

    def empty_recycle(self):
        result = run_command(
            'PowerShell.exe -NoProfile -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"'
        )
        self.show_message(
            self.tr("🗑️ Кошик"),
            self.tr("Команду очищення кошика виконано.")
        )

    def quick_optimize(self):
        self.flush_dns()
        gc.collect()
        self.show_message(self.tr("🚀 Швидка оптимізація"), self.tr("Основну безпечну оптимізацію виконано!"))

    def full_optimize(self):
        self.clean_temp()
        self.flush_dns()
        gc.collect()
        self.activate_ultimate_performance()

    def high_performance(self):
        result = run_command("powercfg /setactive SCHEME_MIN")
        if result and result.returncode == 0:
            self.show_message(self.tr("🔋 Продуктивність"), self.tr("Режим високої продуктивності увімкнено."))
        else:
            self.show_message(self.tr("🔋 Продуктивність"), self.tr("Не вдалося активувати режим."))

    def check_windows(self):
        if not messagebox.askyesno(
            "SFC /scannow",
            "Запустити перевірку системних файлів Windows?\n\nПотрібні права адміністратора."
        ):
            return
        try:
            cmd = (
                "Start-Process cmd -Verb RunAs "
                "-ArgumentList '/k sfc /scannow'"
            )
            subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", cmd],
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
        except Exception as e:
            self.show_message("SFC /scannow", str(e))


    def scan_system(self):
        import psutil

        cpu = psutil.cpu_percent(interval=0.35)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("C:\\").percent

        score = 100
        notes = []

        if cpu >= 85:
            score -= 25
            notes.append("• CPU зараз сильно завантажений.")
        elif cpu >= 60:
            score -= 10
            notes.append("• CPU має помітне навантаження.")

        if ram >= 90:
            score -= 30
            notes.append("• Дуже мало вільної оперативної пам'яті.")
        elif ram >= 75:
            score -= 15
            notes.append("• Використання RAM підвищене.")

        if disk >= 95:
            score -= 30
            notes.append("• На диску C: майже немає вільного місця.")
        elif disk >= 85:
            score -= 15
            notes.append("• Варто звільнити місце на диску C:.")

        score = max(0, min(100, score))
        status = (
            "Відмінно" if score >= 90 else
            "Добре" if score >= 75 else
            "Потрібна увага" if score >= 55 else
            "Потрібна перевірка"
        )

        if not notes:
            notes.append("• Критичних проблем у поточному навантаженні не видно.")

        self.show_message(
            "🔍 Сканування системи",
            f"Оцінка стану: {score}/100 — {status}\n\n"
            f"CPU: {cpu:.1f}%\n"
            f"RAM: {ram:.1f}%\n"
            f"Диск C: {disk:.1f}%\n\n"
            + "\n".join(notes)
        )



    def open_task_manager(self):
        subprocess.Popen("taskmgr.exe", shell=True)

    def windows_update(self):
        os.system("start ms-settings:windowsupdate")

    def save_report(self):
        import psutil
        filename = os.path.abspath("optimizer_report.txt")

        with open(filename, "w", encoding="utf-8") as file:
            file.write("WINDOWS OPTIMIZER ULTRA 6.2.1.1\n")
            file.write("===========================\n\n")
            file.write(f"Дата: {datetime.now()}\n")
            file.write(f"Windows: {platform.system()} {platform.release()}\n")
            file.write(f"CPU: {platform.processor()}\n")
            file.write(f"RAM: {psutil.virtual_memory().total / (1024**3):.2f} GB\n")

        self.show_message(self.tr("📝 Звіт"), self.tr("Звіт збережено:\n") + filename)


    def open_storage_sense(self):
        """Відкрити Storage Sense / Пам'ять Windows."""
        try:
            os.system("start ms-settings:storagesense")
        except Exception as e:
            self.show_message("Storage Sense", str(e))

    def open_startup_apps(self):
        """Відкрити керування програмами автозапуску."""
        try:
            os.system("start ms-settings:startupapps")
        except Exception as e:
            self.show_message("Автозапуск", str(e))

    def open_optimize_drives(self):
        """Відкрити стандартний Optimize Drives."""
        try:
            subprocess.Popen("dfrgui.exe", shell=True)
        except Exception as e:
            self.show_message("Оптимізація дисків", str(e))

    def run_disk_cleanup(self):
        """Запустити стандартне очищення диска Windows."""
        try:
            subprocess.Popen("cleanmgr.exe", shell=True)
        except Exception as e:
            self.show_message("Очищення диска", str(e))

    def clear_thumbnail_cache(self):
        """Очистити кеш ескізів користувача."""
        try:
            local = os.environ.get("LOCALAPPDATA", "")
            cache_dir = os.path.join(
                local, "Microsoft", "Windows", "Explorer"
            )
            removed = 0

            if os.path.isdir(cache_dir):
                for name in os.listdir(cache_dir):
                    if name.lower().startswith("thumbcache_"):
                        path = os.path.join(cache_dir, name)
                        try:
                            os.remove(path)
                            removed += 1
                        except Exception:
                            pass

            self.show_message(
                "🖼️ Кеш ескізів",
                f"Готово. Видалено файлів кешу: {removed}"
            )
        except Exception as e:
            self.show_message("Помилка", str(e))

    def check_drive_health(self):
        """Показати базовий стан фізичних дисків (тільки читання)."""
        try:
            ps = (
                "Get-PhysicalDisk | "
                "Select-Object FriendlyName, MediaType, HealthStatus, "
                "OperationalStatus, Size | Format-Table -AutoSize"
            )
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps],
                capture_output=True,
                text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )

            output = (result.stdout or result.stderr or "").strip()
            if not output:
                output = "Не вдалося отримати інформацію про диски."

            self.show_text_window("💽 Стан дисків", output)

        except Exception as e:
            self.show_message("Помилка", str(e))

    def run_dism_restorehealth(self):
        """Запустити DISM /RestoreHealth у новому вікні консолі."""
        try:
            ok = messagebox.askyesno(
                "DISM RestoreHealth",
                "Запустити відновлення компонентів Windows?\n\n"
                "Процес може тривати довго. Не вимикайте ПК під час виконання."
            )
            if not ok:
                return

            cmd = (
                'Start-Process cmd -Verb RunAs '
                '-ArgumentList \'/k DISM /Online /Cleanup-Image /RestoreHealth\''
            )
            subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", cmd],
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
        except Exception as e:
            self.show_message("DISM", str(e))

    def show_text_window(self, title, text):
        """Велике вікно для текстового результату."""
        window = ctk.CTkToplevel(self)
        window.title(title)
        window.geometry("760x480")
        window.transient(self)

        ctk.CTkLabel(
            window,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 10))

        box = ctk.CTkTextbox(
            window,
            corner_radius=12,
            font=ctk.CTkFont(size=12)
        )
        box.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        box.insert("1.0", text)
        box.configure(state="disabled")

        ctk.CTkButton(
            window,
            text="OK",
            width=120,
            command=window.destroy
        ).pack(pady=(0, 18))


    def dism_checkhealth(self):
        if not messagebox.askyesno("DISM CheckHealth", "Запустити безпечну перевірку образу Windows?"):
            return
        cmd = 'Start-Process cmd -Verb RunAs -ArgumentList \'/k DISM /Online /Cleanup-Image /CheckHealth\''
        subprocess.Popen(["powershell", "-NoProfile", "-Command", cmd],
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    def dism_scanhealth(self):
        if not messagebox.askyesno("DISM ScanHealth", "Запустити повне сканування образу Windows? Це може зайняти деякий час."):
            return
        cmd = 'Start-Process cmd -Verb RunAs -ArgumentList \'/k DISM /Online /Cleanup-Image /ScanHealth\''
        subprocess.Popen(["powershell", "-NoProfile", "-Command", cmd],
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    def chkdsk_scan(self):
        if not messagebox.askyesno("CHKDSK", "Перевірити диск C: без автоматичного виправлення?"):
            return
        subprocess.Popen(["cmd", "/k", "chkdsk C: /scan"],
                         creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0))

    def battery_report(self):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            if not os.path.isdir(desktop):
                desktop = os.path.expanduser("~")
            report = os.path.join(desktop, "battery-report.html")
            result = subprocess.run(
                ["powercfg", "/batteryreport", "/output", report],
                capture_output=True, text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            if result.returncode == 0:
                self.show_message("🔋 Battery Report", f"Звіт створено:\n{report}")
                os.startfile(report)
            else:
                self.show_message("🔋 Battery Report", "Не вдалося створити звіт. На ПК може не бути батареї.")
        except Exception as e:
            self.show_message("Помилка", str(e))

    def top_processes(self):
        try:
            import psutil
            rows = []
            for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
                try:
                    info = p.info
                    rows.append((
                        float(info.get("memory_percent") or 0),
                        float(info.get("cpu_percent") or 0),
                        int(info.get("pid") or 0),
                        info.get("name") or "Unknown"
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            rows.sort(reverse=True)
            lines = ["TOP процесів за RAM", "=" * 55]
            for mem, cpu, pid, name in rows[:15]:
                lines.append(f"{name[:28]:28} PID {pid:<7} RAM {mem:5.1f}%  CPU {cpu:5.1f}%")
            self.show_text_window("🧠 TOP CPU / RAM", "\n".join(lines))
        except Exception as e:
            self.show_message("Помилка", str(e))

    def disk_analyzer(self):
        try:
            import psutil
            lines = ["АНАЛІЗ ДИСКІВ", "=" * 50]
            seen = set()
            for part in psutil.disk_partitions(all=False):
                mount = part.mountpoint
                if mount in seen:
                    continue
                seen.add(mount)
                try:
                    u = psutil.disk_usage(mount)
                    lines.append(
                        f"\n{mount}\n"
                        f"  Всього: {u.total/(1024**3):.1f} GB\n"
                        f"  Зайнято: {u.used/(1024**3):.1f} GB ({u.percent:.1f}%)\n"
                        f"  Вільно: {u.free/(1024**3):.1f} GB"
                    )
                except Exception:
                    pass
            self.show_text_window("💾 Disk Analyzer", "\n".join(lines))
        except Exception as e:
            self.show_message("Помилка", str(e))

    def network_info(self):
        try:
            result = subprocess.run(
                ["ipconfig", "/all"], capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            self.show_text_window("🌐 Network Info", (result.stdout or result.stderr or "Немає даних."))
        except Exception as e:
            self.show_message("Помилка", str(e))

    def open_windows_security(self):
        try:
            os.system("start windowsdefender:")
        except Exception as e:
            self.show_message("Windows Security", str(e))

    def create_restore_point(self):
        if not messagebox.askyesno(
            "Точка відновлення",
            "Створити точку відновлення Windows перед системними змінами?"
        ):
            return
        try:
            ps = (
                'Checkpoint-Computer -Description "Windows Optimizer Ultra 6.2.1" '
                '-RestorePointType "MODIFY_SETTINGS"'
            )
            cmd = (
                "Start-Process powershell -Verb RunAs -Wait "
                f"-ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command \"{ps}\"'"
            )
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", cmd],
                capture_output=True, text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            self.show_message(
                "🛡️ Точка відновлення",
                "Команду створення точки відновлення виконано. "
                "Windows може обмежувати частоту створення точок."
            )
        except Exception as e:
            self.show_message("Помилка", str(e))



    def open_device_manager(self):
        try:
            subprocess.Popen("devmgmt.msc", shell=True)
        except Exception as e:
            self.show_message("Device Manager", str(e))

    def open_event_viewer(self):
        try:
            subprocess.Popen("eventvwr.msc", shell=True)
        except Exception as e:
            self.show_message("Event Viewer", str(e))

    def open_resource_monitor(self):
        try:
            subprocess.Popen("resmon.exe", shell=True)
        except Exception as e:
            self.show_message("Resource Monitor", str(e))

    def open_system_information(self):
        try:
            subprocess.Popen("msinfo32.exe", shell=True)
        except Exception as e:
            self.show_message("System Information", str(e))

    def open_disk_management(self):
        try:
            subprocess.Popen("diskmgmt.msc", shell=True)
        except Exception as e:
            self.show_message("Disk Management", str(e))

    def open_services(self):
        try:
            subprocess.Popen("services.msc", shell=True)
        except Exception as e:
            self.show_message("Services", str(e))

    def open_reliability_monitor(self):
        try:
            subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", "perfmon /rel"],
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
        except Exception as e:
            self.show_message("Reliability Monitor", str(e))

    def installed_apps(self):
        try:
            ps = (
                "$paths=@("
                "'HKLM:\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Uninstall\\\\*',"
                "'HKLM:\\\\Software\\\\WOW6432Node\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Uninstall\\\\*',"
                "'HKCU:\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Uninstall\\\\*'"
                ");"
                "Get-ItemProperty $paths -ErrorAction SilentlyContinue | "
                "Where-Object {$_.DisplayName} | "
                "Select-Object DisplayName,DisplayVersion,Publisher | "
                "Sort-Object DisplayName | Format-Table -AutoSize"
            )
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps],
                capture_output=True, text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            output = (result.stdout or result.stderr or "").strip()
            self.show_text_window(
                "📦 Installed Apps",
                output if output else "Список програм не отримано."
            )
        except Exception as e:
            self.show_message("Помилка", str(e))

    def startup_entries(self):
        try:
            ps = (
                "Get-CimInstance Win32_StartupCommand | "
                "Select-Object Name,Command,Location,User | "
                "Sort-Object Name | Format-Table -Wrap -AutoSize"
            )
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps],
                capture_output=True, text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            output = (result.stdout or result.stderr or "").strip()
            self.show_text_window(
                "🚀 Startup Entries",
                output if output else "Записи автозапуску не знайдено."
            )
        except Exception as e:
            self.show_message("Помилка", str(e))

    def network_quick_test(self):
        try:
            commands = [
                ("Internet", ["ping", "-n", "2", "1.1.1.1"]),
                ("DNS", ["nslookup", "microsoft.com"]),
            ]
            parts = []
            for title, cmd in commands:
                result = subprocess.run(
                    cmd,
                    capture_output=True, text=True,
                    encoding="utf-8", errors="replace",
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
                )
                parts.append(f"=== {title} ===\n{result.stdout or result.stderr}")
            self.show_text_window("🌐 Network Test", "\n\n".join(parts))
        except Exception as e:
            self.show_message("Помилка", str(e))

    def advanced_report(self):
        try:
            import psutil

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            if not os.path.isdir(desktop):
                desktop = os.path.expanduser("~")
            filename = os.path.join(
                desktop,
                f"Windows_Optimizer_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )

            vm = psutil.virtual_memory()
            cpu_now = psutil.cpu_percent(interval=0.4)
            uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())

            lines = [
                "WINDOWS OPTIMIZER ULTRA 6.2.1.1 - DIAGNOSTIC REPORT",
                "=" * 62,
                f"Date: {datetime.now()}",
                f"Administrator: {'YES' if self.is_admin() else 'NO'}",
                "",
                "SYSTEM",
                "-" * 62,
                f"PC: {platform.node()}",
                f"Windows: {platform.system()} {platform.release()}",
                f"Version: {platform.version()}",
                f"CPU: {platform.processor()}",
                f"Physical cores: {psutil.cpu_count(logical=False)}",
                f"Logical CPUs: {psutil.cpu_count(logical=True)}",
                f"CPU load: {cpu_now:.1f}%",
                f"RAM total: {vm.total/(1024**3):.2f} GB",
                f"RAM used: {vm.percent:.1f}%",
                f"Uptime: {str(uptime).split('.')[0]}",
                "",
                "DISKS",
                "-" * 62,
            ]

            seen = set()
            for part in psutil.disk_partitions(all=False):
                mount = part.mountpoint
                if mount in seen:
                    continue
                seen.add(mount)
                try:
                    u = psutil.disk_usage(mount)
                    lines.extend([
                        f"{mount}  filesystem={part.fstype}",
                        f"  Total: {u.total/(1024**3):.2f} GB",
                        f"  Used:  {u.used/(1024**3):.2f} GB ({u.percent:.1f}%)",
                        f"  Free:  {u.free/(1024**3):.2f} GB",
                    ])
                except Exception:
                    pass

            lines.extend(["", "NETWORK", "-" * 62])
            try:
                for name, addrs in psutil.net_if_addrs().items():
                    ips = []
                    for addr in addrs:
                        if getattr(addr.family, "name", "") in ("AF_INET", "AF_INET6"):
                            ips.append(addr.address)
                    if ips:
                        lines.append(f"{name}: {', '.join(ips)}")
            except Exception:
                pass

            try:
                battery = psutil.sensors_battery()
                lines.extend(["", "BATTERY", "-" * 62])
                if battery:
                    lines.append(f"Charge: {battery.percent:.1f}%")
                    lines.append(f"Plugged in: {'YES' if battery.power_plugged else 'NO'}")
                else:
                    lines.append("Battery not detected.")
            except Exception:
                pass

            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            self.show_message(
                "📝 Advanced Report",
                f"Готово.\n\nЗвіт збережено на Робочому столі:\n{filename}"
            )
        except Exception as e:
            self.show_message("Помилка", str(e))

    # =========================================================
    # UI HELPERS
    # =========================================================
    def create_page_title(self, title, subtitle):
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 5))

        ctk.CTkLabel(
            frame, text=title,
            font=ctk.CTkFont(size=30, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame, text=subtitle, text_color="#78879E",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=(3, 0))

    def create_action(self, title, description, command):
        frame = ctk.CTkFrame(
            self.content, fg_color="#101C2F", corner_radius=16
        )
        frame.grid(column=0, sticky="ew", padx=25, pady=7)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 2))

        ctk.CTkLabel(
            frame, text=description, text_color="#77869C",
            font=ctk.CTkFont(size=12), wraplength=700, justify="left"
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))

        ctk.CTkButton(
            frame, text=self.tr("ЗАПУСТИТИ"), width=145, height=38,
            corner_radius=9, command=command
        ).grid(row=0, column=1, rowspan=2, padx=20)

    def update_stats(self):
        try:
            import psutil
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("C:\\").percent

            if hasattr(self, "cpu_card"):
                self.cpu_card.configure(text=f"{cpu:.0f}%")
            if hasattr(self, "ram_card"):
                self.ram_card.configure(text=f"{ram:.0f}%")
            if hasattr(self, "disk_card"):
                self.disk_card.configure(text=f"{disk:.0f}%")
        except Exception:
            pass

        self.after(1000, self.update_stats)

    def show_message(self, title, message):
        message = str(message)
        window = ctk.CTkToplevel(self)
        window.title(title)
        long_message = len(message) > 350 or message.count("\n") > 10
        window.geometry("680x460" if long_message else "500x300")
        window.resizable(long_message, long_message)
        window.transient(self)
        window.grab_set()

        ctk.CTkLabel(
            window, text=title,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(25, 10))

        if long_message:
            box = ctk.CTkTextbox(window, corner_radius=12, font=ctk.CTkFont(size=12))
            box.pack(fill="both", expand=True, padx=22, pady=10)
            box.insert("1.0", message)
            box.configure(state="disabled")
        else:
            ctk.CTkLabel(
                window, text=message, wraplength=430,
                justify="center", text_color="#AAB7C9"
            ).pack(padx=25, pady=10, expand=True)

        ctk.CTkButton(
            window, text="OK", width=120,
            command=window.destroy
        ).pack(pady=(8, 20))



if __name__ == "__main__":
    app = WindowsOptimizer()
    app.mainloop()




