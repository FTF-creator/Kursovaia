import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def main():
    root = tk.Tk()
    root.title("Меню игры")
    root.geometry("400x300")
    
    tk.Label(root, text="🎴 КАРТОЧНЫЙ ДУРАК", font=('Arial', 16)).pack(pady=20)
    
    def start_game():
        root.destroy()
        try:
            subprocess.run([sys.executable, "main.py"])
        except:
            messagebox.showerror("Ошибка", "Не удалось запустить игру")
    
    tk.Button(root, text="🎮 НАЧАТЬ ИГРУ", command=start_game, 
              font=('Arial', 14), width=20, height=2).pack(pady=10)
    
    tk.Button(root, text="🚪 ВЫХОД", command=root.quit,
              font=('Arial', 14), width=20, height=2).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
