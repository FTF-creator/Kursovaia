# launcher.py
import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
import time
import random

class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Дурак - Загрузка")
        self.root.geometry("600x400")
        self.root.configure(bg='#000000')
        self.root.resizable(False, False)
        self.root.overrideredirect(True)  # Убираем рамку окна
        
        # Центрируем окно
        self.center_window()
        
        self.create_loading_screen()

    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = 600
        height = 400
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_loading_screen(self):
        """Создает экран загрузки"""
        # Основной фрейм
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Логотип
        logo_label = tk.Label(
            main_frame,
            text="🎴",
            font=('Arial', 48),
            bg='#000000',
            fg='#FFFFFF'
        )
        logo_label.pack(pady=20)
        
        # Название игры
        title_label = tk.Label(
            main_frame,
            text="КАРТОЧНЫЙ ДУРАК",
            font=('Arial', 24, 'bold'),
            bg='#000000',
            fg='#00FF00'
        )
        title_label.pack(pady=10)
        
        # Версия
        version_label = tk.Label(
            main_frame,
            text="ФИНАЛЬНАЯ ВЕРСИЯ",
            font=('Arial', 12),
            bg='#000000',
            fg='#888888'
        )
        version_label.pack(pady=5)
        
        # Прогресс-бар
        self.progress = ttk.Progressbar(
            main_frame,
            orient='horizontal',
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=30)
        
        # Текст загрузки
        self.loading_label = tk.Label(
            main_frame,
            text="Подготовка к запуску...",
            font=('Arial', 11),
            bg='#000000',
            fg='#CCCCCC'
        )
        self.loading_label.pack(pady=10)
        
        # Процент загрузки
        self.percent_label = tk.Label(
            main_frame,
            text="0%",
            font=('Arial', 12, 'bold'),
            bg='#000000',
            fg='#00FF00'
        )
        self.percent_label.pack(pady=5)
        
        # Стиль для прогресс-бара
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Horizontal.TProgressbar",
                       background='#00FF00',
                       troughcolor='#333333',
                       borderwidth=0,
                       lightcolor='#00FF00',
                       darkcolor='#00FF00')

    def update_progress(self, value, text):
        """Обновляет прогресс загрузки"""
        self.progress['value'] = value
        self.percent_label['text'] = f"{int(value)}%"
        self.loading_label['text'] = text
        self.root.update()

    def fake_loading(self):
        """Фейковая загрузка с разными сообщениями"""
        loading_steps = [
            (10, "Инициализация игрового движка..."),
            (25, "Загрузка графических ресурсов..."),
            (40, "Подготовка игрового поля..."),
            (55, "Инициализация искусственного интеллекта..."),
            (70, "Загрузка колоды карт..."),
            (85, "Проверка текстур..."),
            (95, "Финальная настройка..."),
            (100, "Запуск игры!")
        ]
        
        for progress, text in loading_steps:
            self.update_progress(progress, text)
            # Случайная задержка от 0.5 до 2 секунд
            time.sleep(random.uniform(0.5, 2.0))

class GameLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.loading_screen = LoadingScreen(self.root)
        
    def launch(self):
        """Запускает процесс загрузки и запуска игры"""
        # Запускаем фейковую загрузку
        self.loading_screen.fake_loading()
        
        # Закрываем окно загрузки
        self.root.destroy()
        
        # Запускаем меню
        self.launch_menu()
    
    def launch_menu(self):
        """Запускает главное меню"""
        try:
            if os.path.exists('menu.py'):
                print("🚀 Запуск меню игры...")
                subprocess.run([sys.executable, 'menu.py'])
            else:
                self.show_error("Файл меню не найден!")
        except Exception as e:
            self.show_error(f"Не удалось запустить меню: {e}")
    
    def launch_game_directly(self):
        """Запускает игру напрямую (без меню)"""
        try:
            if os.path.exists('card_game.py'):
                print("🚀 Прямой запуск игры...")
                subprocess.run([sys.executable, 'card_game.py'])
            else:
                self.show_error("Файл игры не найден!")
        except Exception as e:
            self.show_error(f"Не удалось запустить игру: {e}")
    
    def show_error(self, message):
        """Показывает сообщение об ошибке"""
        error_root = tk.Tk()
        error_root.withdraw()
        tk.messagebox.showerror("Ошибка запуска", message)
        error_root.destroy()

def quick_launch():
    """Быстрый запуск без загрузки (для разработки)"""
    root = tk.Tk()
    root.withdraw()
    
    choice = tk.messagebox.askyesno(
        "Быстрый запуск", 
        "Запустить с загрузочным экраном? (Да)\n\nИли быстрый запуск? (Нет)"
    )
    
    launcher = GameLauncher()
    
    if choice:
        launcher.launch()
    else:
        root.destroy()
        launcher.launch_menu()

if __name__ == "__main__":
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        quick_launch()
    else:
        # Обычный запуск с загрузочным экраном
        launcher = GameLauncher()
        launcher.launch()