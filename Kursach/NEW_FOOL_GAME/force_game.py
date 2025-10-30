import tkinter as tk
from tkinter import messagebox
import random
import os
import sys
from PIL import Image, ImageTk

print("=== СИЛОВАЯ ЗАГРУЗКА - ОБХОД КЭША ===")

class ForceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("ДУРАК - СИЛОВАЯ ЗАГРУЗКА")
        self.root.geometry("900x600")
        self.root.configure(bg='darkgreen')
        
        # ПРИНУДИТЕЛЬНАЯ ЗАГРУЗКА ТЕКСТУР
        self.textures = {}
        self.card_images = {}  # ОТДЕЛЬНЫЙ СЛОВАРЬ ДЛЯ КАРТ
        self.card_width = 122
        self.card_height = 172
        
        print("🔄 СИЛОВАЯ ЗАГРУЗКА ИЗ cards...")
        self._force_load_textures("cards")
        
        # Игроки
        self.players = [
            {'name': 'Игрок', 'cards': [], 'human': True},
            {'name': 'Бот', 'cards': [], 'human': False}
        ]
        
        # Колода
        self.deck = self._create_deck()
        random.shuffle(self.deck)
        
        # Игра
        self.table = []
        self.attacker = 0
        self.defender = 1
        self.trump = self.deck[0]['suit'] if self.deck else '♥'  # ИСПРАВЛЕНО
        self.game_over = False
        
        self.card_widgets = []
        self._create_ui()
        self._deal_cards()
        self._update_display()
    
    def _force_load_textures(self, cards_dir):
        """ПРИНУДИТЕЛЬНАЯ загрузка без кэша"""
        if not os.path.exists(cards_dir):
            print(f"❌ Папки {cards_dir} нет!")
            return
        
        files = os.listdir(cards_dir)
        print(f"📁 Файлов найдено: {len(files)}")
        
        # ОЧИСТКА ПРЕДЫДУЩИХ ТЕКСТУР
        self.card_images.clear()
        
        # ЗАГРУЗКА КАЖДОГО ФАЙЛА С ПРИНУДИТЕЛЬНЫМ ПЕРЕСОЗДАНИЕМ
        for filename in files:
            if filename.endswith('.png'):
                filepath = os.path.join(cards_dir, filename)
                try:
                    # ПРИНУДИТЕЛЬНОЕ ОТКРЫТИЕ И ПЕРЕСОЗДАНИЕ
                    with open(filepath, 'rb') as f:
                        img_data = f.read()
                    
                    # СОЗДАЕМ ИЗ ДАННЫХ ЗАНОВО
                    import io
                    img = Image.open(io.BytesIO(img_data))
                    img = img.resize((self.card_width, self.card_height), Image.LANCZOS)
                    
                    # ПРИНУДИТЕЛЬНОЕ СОЗДАНИЕ PhotoImage
                    photo_img = ImageTk.PhotoImage(img)
                    
                    # Сохраняем под оригинальным именем файла
                    self.card_images[filename] = photo_img
                    print(f"✅ СИЛОВАЯ ЗАГРУЗКА: {filename}")
                    
                except Exception as e:
                    print(f"❌ Ошибка {filename}: {e}")
        
        print(f"🎯 ЗАГРУЖЕНО ТЕКСТУР: {len(self.card_images)}")
        
        # Покажем что загрузилось
        print("📋 ЗАГРУЖЕННЫЕ ТЕКСТУРЫ:")
        for name in sorted(self.card_images.keys()):
            print(f"   {name}")
    
    def _create_deck(self):
        """Создает колоду"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']  # ИСПРАВЛЕНО
        ranks = ['6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        
        deck = []
        for suit in suits:
            for rank in ranks:
                deck.append({'rank': rank, 'suit': suit})
        return deck
    
    def _create_ui(self):
        """Создает интерфейс"""
        # Верхняя панель
        top = tk.Frame(self.root, bg='darkgreen', height=80)
        top.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(top, text="СИЛОВАЯ ЗАГРУЗКА - Игра начинается", 
                                   font=('Arial', 14, 'bold'), bg='darkgreen', fg='white')
        self.status_label.pack(pady=5)
        
        # Стол
        middle = tk.Frame(self.root, bg='darkgreen', height=200)
        middle.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.table_canvas = tk.Canvas(middle, bg='green', height=150)
        self.table_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Карты игрока
        bottom = tk.Frame(self.root, bg='darkgreen', height=150)
        bottom.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(bottom, text="ВАШИ КАРТЫ (силовая загрузка):", 
                font=('Arial', 12, 'bold'), bg='darkgreen', fg='white').pack()
        
        self.cards_frame = tk.Frame(bottom, bg='darkgreen')
        self.cards_frame.pack(pady=5)
        
        # Кнопка для теста
        test_btn = tk.Button(self.root, text="ТЕСТ: Показать 6_hearts.png", 
                           command=self._test_texture, font=('Arial', 12))
        test_btn.pack(pady=5)
    
    def _test_texture(self):
        """Тест отображения текстуры"""
        test_window = tk.Toplevel(self.root)
        test_window.title("ТЕСТ ТЕКСТУРЫ")
        test_window.geometry("200x250")
        
        # Пробуем показать 6_hearts.png
        if '6_hearts.png' in self.card_images:
            test_label = tk.Label(test_window, image=self.card_images['6_hearts.png'])
            test_label.pack(pady=10)
            tk.Label(test_window, text="Это ДОЛЖНА быть\nваша текстура 6♥", 
                    font=('Arial', 10), justify=tk.CENTER).pack()
            
            # Сохраним ссылку чтобы изображение не удалилось
            test_window.test_image = self.card_images['6_hearts.png']
        else:
            tk.Label(test_window, text="❌ 6_hearts.png не найден", 
                    font=('Arial', 12)).pack()
    
    def _deal_cards(self):
        """Раздача карт"""
        for player in self.players:
            player['cards'] = []
            for _ in range(6):
                if self.deck:
                    player['cards'].append(self.deck.pop())
    
    def _update_display(self):
        """Обновление отображения"""
        # Очищаем старые карты
        for widget in self.card_widgets:
            widget.destroy()
        self.card_widgets = []
        
        # Показываем карты игрока
        human = self.players[0]
        for card in human['cards']:
            card_frame = tk.Frame(self.cards_frame, relief=tk.RAISED, borderwidth=2, bg='white')
            card_frame.pack_propagate(False)
            
            card_canvas = tk.Canvas(card_frame, width=122, height=172, 
                                  bg='white', highlightthickness=0)
            card_canvas.pack(fill=tk.BOTH, expand=True)
            
            # Имя файла текстуры
            filename = f"{card['rank']}_{card['suit']}.png"
            
            if filename in self.card_images:
                # ИСПОЛЬЗУЕМ ЗАГРУЖЕННУЮ ТЕКСТУРУ
                card_canvas.create_image(61, 86, image=self.card_images[filename])
                print(f"🎴 ОТОБРАЖАЕМ: {filename}")
            else:
                # Резервный вариант
                suit_symbol = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}
                color = 'red' if card['suit'] in ['hearts', 'diamonds'] else 'black'
                symbol = suit_symbol.get(card['suit'], '?')
                
                card_canvas.create_rectangle(5, 5, 117, 167, fill='white', outline='black', width=2)
                card_canvas.create_text(61, 86, text=f"{card['rank']}{symbol}", 
                                      font=('Arial', 14), fill=color)
                print(f"❌ ТЕКСТУРА НЕ НАЙДЕНА: {filename}")
            
            card_frame.pack(side=tk.LEFT, padx=2)
            self.card_widgets.append(card_frame)
        
        # Обновляем статус
        attacker_name = self.players[self.attacker]['name']
        defender_name = self.players[self.defender]['name']
        self.status_label.config(text=f"Атакует: {attacker_name} | Защищается: {defender_name} | Текстуры: {len(self.card_images)}")

# ЗАПУСК
if __name__ == "__main__":
    print("Убедитесь что папка называется: cards")
    root = tk.Tk()
    game = ForceGame(root)
    root.mainloop()