# menu.py
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
def start_game(self):
    """Запускает основную игру"""
    try:
        # Закрываем меню
        self.root.destroy()
        
        # Запускаем игру через лаунчер с загрузкой
        if os.path.exists('launcher.py'):
            subprocess.run([sys.executable, 'launcher.py', '--quick'])
        elif os.path.exists('card_game.py'):
            subprocess.run([sys.executable, 'card_game.py'])
        else:
            messagebox.showerror("Ошибка", "Файл игры не найден!")
            sys.exit()
            
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить игру: {e}")
class GameMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("ДУРАК - МЕНЮ")
        self.root.geometry("800x730")
        self.root.configure(bg='#000000')
        self.root.resizable(False, False)
        
        # Центрируем окно
        self.center_window()
        
        self.create_menu()

    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_menu(self):
        """Создает главное меню"""
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="🎴 КАРТОЧНАЯ ИГРА ДУРАК 🎴",
            font=('Arial', 24, 'bold'),
            bg='#000000',
            fg='#FFFFFF'
        )
        title_label.pack(pady=40)

        # Версия
        version_label = tk.Label(
            self.root,
            text="ФИНАЛЬНАЯ ВЕРСИЯ",
            font=('Arial', 12),
            bg='#000000',
            fg='#888888'
        )
        version_label.pack(pady=5)

        # Кнопки меню
        button_frame = tk.Frame(self.root, bg='#000000')
        button_frame.pack(pady=50)

        buttons = [
            ("🎮 НАЧАТЬ ИГРУ", self.start_game, '#00FF00'),
            ("⚙️ НАСТРОЙКИ", self.show_settings, '#0088FF'),
            ("📊 СТАТИСТИКА", self.show_stats, '#FF8800'),
            ("❓ ПРАВИЛА", self.show_rules, '#FF0088'),
            ("🚪 ВЫХОД", self.exit_game, '#FF0000')
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=('Arial', 14, 'bold'),
                bg='#111111',
                fg=color,
                activebackground='#222222',
                activeforeground=color,
                relief='raised',
                borderwidth=3,
                width=20,
                height=2,
                cursor='hand2',
                command=command
            )
            btn.pack(pady=8)

        # Футер
        footer_label = tk.Label(
            self.root,
            text="© 2025 Карточный Дурак | Все права защищены FTF",
            font=('Arial', 10),
            bg='#000000',
            fg='#444444'
        )
        footer_label.pack(side='bottom', pady=20)

    def start_game(self):
        """Запускает основную игру"""
        try:
            # Закрываем меню
            self.root.destroy()
            
            # Запускаем игру
            if os.path.exists('card_game.py'):
                subprocess.run([sys.executable, 'card_game.py'])
            else:
                messagebox.showerror("Ошибка", "Файл игры не найден!")
                sys.exit()
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить игру: {e}")

    def show_settings(self):
        """Показывает настройки"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#000000')
        settings_window.resizable(False, False)
        
        # Центрируем
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        tk.Label(
            settings_window,
            text="⚙️ НАСТРОЙКИ ИГРЫ",
            font=('Arial', 16, 'bold'),
            bg='#000000',
            fg='#FFFFFF'
        ).pack(pady=20)

        # Настройки будут здесь
        tk.Label(
            settings_window,
            text="Раздел настроек в разработке...",
            font=('Arial', 12),
            bg='#000000',
            fg='#888888'
        ).pack(pady=50)

        tk.Button(
            settings_window,
            text="ЗАКРЫТЬ",
            font=('Arial', 12, 'bold'),
            bg='#111111',
            fg='#FF0000',
            command=settings_window.destroy
        ).pack(pady=20)

    def show_stats(self):
        """Показывает статистику"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика")
        stats_window.geometry("400x300")
        stats_window.configure(bg='#000000')
        stats_window.resizable(False, False)
        
        stats_window.transient(self.root)
        stats_window.grab_set()
        
        tk.Label(
            stats_window,
            text="📊 СТАТИСТИКА ИГРЫ",
            font=('Arial', 16, 'bold'),
            bg='#000000',
            fg='#FFFFFF'
        ).pack(pady=20)

        # Статистика будет здесь
        stats_text = """
        Побед: 0
        Поражений: 0
        Ничьих: 0
        
        Лучшая серия: 0
        Всего игр: 0
        """
        
        tk.Label(
            stats_window,
            text=stats_text,
            font=('Arial', 12),
            bg='#000000',
            fg='#888888',
            justify='left'
        ).pack(pady=20)

        tk.Button(
            stats_window,
            text="ЗАКРЫТЬ",
            font=('Arial', 12, 'bold'),
            bg='#111111',
            fg='#FF0000',
            command=stats_window.destroy
        ).pack(pady=20)

    def show_rules(self):
        """Показывает правила игры"""
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила игры")
        rules_window.geometry("500x400")
        rules_window.configure(bg='#000000')
        rules_window.resizable(False, False)
        
        rules_window.transient(self.root)
        rules_window.grab_set()
        
        tk.Label(
            rules_window,
            text="❓ ПРАВИЛА ИГРЫ ДУРАК",
            font=('Arial', 16, 'bold'),
            bg='#000000',
            fg='#FFFFFF'
        ).pack(pady=20)

        rules_text = """
        🎯 Цель игры: избавиться от всех карт
        
        📋 Основные правила:
        • Играют 2 игрока
        • Каждому раздается по 6 карт
        • Первый ходит игрок с младшим козырем
        • Можно подкидывать карты того же достоинства
        • Защищающийся должен побить все карты
        • Если не может - забирает все карты со стола
        
        🃏 Старшинство карт:
        6, 7, 8, 9, 10, В, Д, К, Т
        """
        
        text_widget = tk.Text(
            rules_window,
            font=('Arial', 11),
            bg='#111111',
            fg='#CCCCCC',
            wrap='word',
            relief='flat',
            borderwidth=10
        )
        text_widget.pack(pady=10, padx=20, fill='both', expand=True)
        text_widget.insert('1.0', rules_text)
        text_widget.config(state='disabled')

        tk.Button(
            rules_window,
            text="ЗАКРЫТЬ",
            font=('Arial', 12, 'bold'),
            bg='#111111',
            fg='#FF0000',
            command=rules_window.destroy
        ).pack(pady=20)

    def exit_game(self):
        """Выход из игры"""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()
            sys.exit()

def main():
    """Запуск меню"""
    root = tk.Tk()
    app = GameMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()