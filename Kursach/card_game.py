import tkinter as tk
from tkinter import messagebox
import random
import os
import sys
from PIL import Image, ImageTk

print("=== ФИНАЛЬНАЯ ВЕРСИЯ ДУРАКА ===")

class CardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("ДУРАК - ФИНАЛЬНАЯ ВЕРСИЯ")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2E8B57')
        
        # ЗАГРУЗКА ТЕКСТУР
        self.card_images = {}
        self.card_back_image = None
        self.table_image = None
        self.card_width = 100
        self.card_height = 140
        
        print("🔄 Загрузка ваших текстур...")
        self._load_textures("cards")
        self._load_table_texture()
        
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
        self.trump = self.deck[0]['suit'] if self.deck else 'hearts'
        self.game_over = False
        self.discard_pile = []
        
        self.card_widgets = []
        self._create_ui()
        self._deal_cards()
        self._update_display()
    
    def _load_textures(self, cards_dir):
        """Загрузка текстур карт"""
        if not os.path.exists(cards_dir):
            print(f"❌ Папки {cards_dir} нет!")
            return
        
        files = os.listdir(cards_dir)
        print(f"📁 Загружено текстур карт: {len(files)}")
        
        # Загружаем рубашку карты
        back_files = ['back.png', 'card_back.png', 'backside.png', 'рубашка.png']
        for back_file in back_files:
            back_path = os.path.join(cards_dir, back_file)
            if os.path.exists(back_path):
                try:
                    img = Image.open(back_path)
                    img = img.resize((self.card_width, self.card_height), Image.Resampling.LANCZOS)
                    self.card_back_image = ImageTk.PhotoImage(img)
                    print(f"✅ Загружена рубашка: {back_file}")
                    break
                except Exception as e:
                    print(f"❌ Ошибка загрузки рубашки {back_file}: {e}")
        
        # Загружаем остальные карты
        for filename in files:
            if filename.endswith('.png') and not any(back in filename for back in back_files):
                filepath = os.path.join(cards_dir, filename)
                try:
                    img = Image.open(filepath)
                    img = img.resize((self.card_width, self.card_height), Image.Resampling.LANCZOS)
                    self.card_images[filename] = ImageTk.PhotoImage(img)
                    print(f"✅ Загружено: {filename}")
                except Exception as e:
                    print(f"❌ Ошибка {filename}: {e}")
    
    def _load_table_texture(self):
        """Загрузка текстуры стола"""
        table_files = [
            "table.png", "table_texture.png", "table.jpg", "table_texture.jpg",
            "background.png", "background.jpg"
        ]
        
        for filename in table_files:
            filepath = os.path.join("cards", filename)
            if os.path.exists(filepath):
                try:
                    img = Image.open(filepath)
                    table_width = 2000
                    table_height = 1000
                    img = img.resize((table_width, table_height), Image.Resampling.LANCZOS)
                    self.table_image = ImageTk.PhotoImage(img)
                    print(f"✅ Загружена текстура стола: {filename}")
                    return
                except Exception as e:
                    print(f"❌ Ошибка загрузки текстуры стола {filename}: {e}")
        
        print("ℹ️ Текстура стола не найдена, будет использован стандартный фон")
    
    def _create_deck(self):
        """Создает колоду"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        
        deck = []
        for suit in suits:
            for rank in ranks:
                deck.append({'rank': rank, 'suit': suit})
        return deck
    
    def _create_ui(self):
        """Создает интерфейс"""
        # Верхняя панель
        top = tk.Frame(self.root, bg='#2E8B57', height=80)
        top.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(top, text="🎴 ДУРАК - Ваши текстуры загружены!", 
                                   font=('Arial', 14, 'bold'), bg='#2E8B57', fg='white')
        self.status_label.pack(pady=5)
        
        suit_symbols = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}
        self.trump_label = tk.Label(top, text=f"Козырь: {suit_symbols.get(self.trump, '?')}", 
                                  font=('Arial', 12), bg='#2E8B57', fg='gold')
        self.trump_label.pack()
        
        # Информация о картах
        self.info_label = tk.Label(top, text="", font=('Arial', 10), bg='#2E8B57', fg='white')
        self.info_label.pack()
        
        # Основной игровой стол
        middle = tk.Frame(self.root, bg='#2E8B57', height=400)
        middle.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas для стола с текстурой
        self.table_canvas = tk.Canvas(middle, bg='#228B22', height=380, relief=tk.SUNKEN, borderwidth=2)
        self.table_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Карты бота (вверху)
        bot_frame = tk.Frame(self.root, bg='#2E8B57', height=100)
        bot_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(bot_frame, text="КАРТЫ БОТА:", font=('Arial', 14, 'bold'),
                bg='#2E8B57', fg='white').pack()
        
        self.bot_cards_frame = tk.Frame(bot_frame, bg='#2E8B57')
        self.bot_cards_frame.pack(pady=10)
        
        # Карты игрока (внизу)
        player_frame = tk.Frame(self.root, bg='#2E8B57', height=100)
        player_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(player_frame, text="ВАШИ КАРТЫ:", font=('Arial', 14, 'bold'),
                bg='#2E8B57', fg='white').pack()
        
        self.player_cards_frame = tk.Frame(player_frame, bg='#2E8B57')
        self.player_cards_frame.pack(pady=10)
        
        # Кнопки управления
        # Кнопки управления
        controls = tk.Frame(self.root, bg='#2E8B57')
        controls.pack(fill=tk.X, padx=10, pady=10)

        self.take_btn = tk.Button(controls, text="ВЗЯТЬ КАРТЫ", command=self._take_cards,
                                font=('Arial', 12, 'bold'), state=tk.DISABLED, 
                                bg="#D7E60B", fg='white', width=15, height=2)
        self.take_btn.pack(side=tk.LEFT, padx=10)

        self.pass_btn = tk.Button(controls, text="ПРОПУСТИТЬ", command=self._pass_turn,
                                font=('Arial', 12, 'bold'), state=tk.DISABLED,
                                bg='#45B7D1', fg='white', width=15, height=2)
        self.pass_btn.pack(side=tk.LEFT, padx=10)

        # Кнопка ВЫХОД В МЕНЮ справа
        self.menu_btn = tk.Button(controls, text="ВЫХОД В МЕНЮ", command=self._exit_to_menu,
                                font=('Arial', 12, 'bold'),
                                bg="#FF0000", fg='white', width=15, height=2)
        self.menu_btn.pack(side=tk.RIGHT, padx=10)
    
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
        
        # Показываем карты бота (рубашкой вверх)
        bot = self.players[1]
        for card in bot['cards']:
            card_frame = tk.Frame(self.bot_cards_frame, width=self.card_width, height=self.card_height,
                                relief=tk.RAISED, borderwidth=2, bg='white')
            card_frame.pack_propagate(False)
            card_frame.pack(side=tk.LEFT, padx=3)
            
            card_canvas = tk.Canvas(card_frame, width=self.card_width, height=self.card_height, 
                                  bg='white', highlightthickness=0)
            card_canvas.pack(fill=tk.BOTH, expand=True)
            
            if self.card_back_image:
                card_canvas.create_image(0, 0, image=self.card_back_image, anchor=tk.NW)
            
            self.card_widgets.append(card_frame)
        
        # Показываем карты игрока
        human = self.players[0]
        can_attack = (not self.game_over and self.attacker == 0)
        can_defend = (not self.game_over and self.defender == 0 and self.table)
        
        for card in human['cards']:
            card_frame = tk.Frame(self.player_cards_frame, width=self.card_width, height=self.card_height,
                                relief=tk.RAISED, borderwidth=2, bg='white')
            card_frame.pack_propagate(False)
            card_frame.pack(side=tk.LEFT, padx=3)
            
            card_canvas = tk.Canvas(card_frame, width=self.card_width, height=self.card_height, 
                                  bg='white', highlightthickness=0)
            card_canvas.pack(fill=tk.BOTH, expand=True)
            
            filename = f"{card['rank']}_{card['suit']}.png"
            if filename in self.card_images:
                card_canvas.create_image(0, 0, image=self.card_images[filename], anchor=tk.NW)
                
                if card['suit'] == self.trump:
                    card_canvas.create_rectangle(2, 2, self.card_width-2, self.card_height-2,
                                               outline='gold', width=3)
            
            if can_attack or can_defend:
                card_canvas.bind('<Button-1>', lambda e, c=card: self._on_card_click(c))
                card_canvas.bind('<Enter>', lambda e, f=card_frame: f.configure(bg='lightblue'))
                card_canvas.bind('<Leave>', lambda e, f=card_frame: f.configure(bg='white'))
                card_canvas.config(cursor="hand2")
            
            self.card_widgets.append(card_frame)
        
        # Обновляем стол
        self._draw_table()
        
        # Обновляем статус и информацию
        attacker_name = self.players[self.attacker]['name']
        defender_name = self.players[self.defender]['name']
        self.status_label.config(text=f"🎯 Атакует: {attacker_name} | 🛡️ Защищается: {defender_name}")
        
        # Обновляем информацию о картах
        human_count = len(self.players[0]['cards'])
        bot_count = len(self.players[1]['cards'])
        deck_count = len(self.deck)
        discard_count = len(self.discard_pile)
        self.info_label.config(text=f"📊 Карты: Вы ({human_count}) | Бот ({bot_count}) | Колода ({deck_count}) | Отбой ({discard_count})")
        
        # Проверяем победу после обновления
        self._check_win()
        
        # Обновляем кнопки
        self._update_buttons()
    
    def _draw_table(self):
        """Рисует стол с текстурой"""
        self.table_canvas.delete("all")
        
        # Рисуем текстуру стола если есть
        if self.table_image:
            self.table_canvas.create_image(0, 0, image=self.table_image, anchor=tk.NW)
        
        # Рисуем общую колоду слева с рубашкой
        if self.deck and self.card_back_image:
            deck_x, deck_y = 50, 150
            self.table_canvas.create_image(deck_x, deck_y, image=self.card_back_image, anchor=tk.NW)
            self.table_canvas.create_text(deck_x + self.card_width//2, deck_y + self.card_height + 10,
                                        text=f"Колода\n{len(self.deck)}", 
                                        font=('Arial', 12, 'bold'), 
                                        fill='white' if not self.table_image else 'black',
                                        justify=tk.CENTER)
        
        # Рисуем отбой справа с рубашкой
        if self.discard_pile and self.card_back_image:
            discard_x, discard_y = 1000, 150
            self.table_canvas.create_image(discard_x, discard_y, image=self.card_back_image, anchor=tk.NW)
            self.table_canvas.create_text(discard_x + self.card_width//2, discard_y + self.card_height + 10,
                                        text=f"Отбой\n{len(self.discard_pile)}", 
                                        font=('Arial', 12, 'bold'),
                                        fill='white' if not self.table_image else 'black',
                                        justify=tk.CENTER)
        
        # Рисуем козырь
        trump_x, trump_y = 50, 50
        suit_symbols = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}
        symbol = suit_symbols.get(self.trump, '?')
        color = 'red' if self.trump in ['hearts', 'diamonds'] else 'white'
        self.table_canvas.create_text(trump_x, trump_y, text=f"Козырь: {symbol}", 
                                    font=('Arial', 14, 'bold'), 
                                    fill=color if not self.table_image else 'black')
        
        if not self.table:
            if not self.deck and not self.discard_pile:
                self.table_canvas.create_text(600, 200, text="🎴 Стол пуст", 
                                            font=('Arial', 16), 
                                            fill='white' if not self.table_image else 'black')
            return
        
        # Рисуем карты на столе для атаки/защиты по центру
        x, y = 400, 150
        for attack, defense in self.table:
            if attack:
                filename = f"{attack['rank']}_{attack['suit']}.png"
                if filename in self.card_images:
                    self.table_canvas.create_image(x, y, image=self.card_images[filename], anchor=tk.NW)
            
            if defense:
                filename = f"{defense['rank']}_{defense['suit']}.png"
                if filename in self.card_images:
                    self.table_canvas.create_image(x+80, y, image=self.card_images[filename], anchor=tk.NW)
            else:
                text_color = 'white' if not self.table_image else 'black'
                self.table_canvas.create_text(x+40, y+120, text="❌", 
                                            font=('Arial', 16), fill=text_color)
            
            x += 160
    
    def _update_buttons(self):
        """Обновляет кнопки"""
        self.take_btn.config(state=tk.DISABLED)
        self.pass_btn.config(state=tk.DISABLED)
    
        if self.game_over:
            return
    
    # Кнопка ВЗЯТЬ КАРТЫ активна для защищающегося
        if self.players[self.defender]['human'] and self.table:
            self.take_btn.config(state=tk.NORMAL)
    
    # Кнопка ПРОПУСТИТЬ активна для атакующего
        if self.players[self.attacker]['human']:
            self.pass_btn.config(state=tk.NORMAL)
    def _on_card_click(self, card):
        """Обработка клика по карте"""
        if self.game_over:
            return
            
        human = self.players[0]
        
        if self.attacker == 0:  # Игрок атакует
            # Проверяем, можно ли атаковать этой картой
            if not self.table:  # Первая атака - можно любой картой
                human['cards'].remove(card)
                self.table.append((card, None))
                self._update_display()
                self._start_defense()
            else:  # Дополнительная атака - только карты того же достоинства
                table_ranks = {pair[0]['rank'] for pair in self.table}
                if card['rank'] in table_ranks:
                    human['cards'].remove(card)
                    self.table.append((card, None))
                    self._update_display()
                else:
                    messagebox.showinfo("Нельзя подкинуть", "Можно подкидывать только карты того же достоинства, что уже на столе")
            
        elif self.defender == 0:  # Игрок защищается
            if not self.table:
                return
            
            for i, (attack, defense) in enumerate(self.table):
                if not defense and self._can_beat(card, attack):
                    human['cards'].remove(card)
                    self.table[i] = (attack, card)
                    self._update_display()
                    
                    # Автоматически нажимаем БИТО если все карты отбиты
                    if all(defense is not None for _, defense in self.table):
                        self.root.after(500, self._beat)
                    else:
                        self._start_defense()
                    return
            
            messagebox.showwarning("Нельзя отбиться", "Эта карта не может побить атакующую карту!")
    
    def _can_beat(self, card, attack):
        """Может ли карта побить атаку"""
        ranks = ['6','7','8','9','10','jack','queen','king','ace']
        
        if card['suit'] == attack['suit']:
            return ranks.index(card['rank']) > ranks.index(attack['rank'])
        elif card['suit'] == self.trump and attack['suit'] != self.trump:
            return True
        return False
    
    def _take_cards(self):
        """Игрок берет карты"""
        defender = self.players[self.defender]
        for attack, defense in self.table:
            if attack:
                defender['cards'].append(attack)
            if defense:
                defender['cards'].append(defense)
        
        self.table.clear()
        self._next_turn_failed()
        self._replenish_cards()
        self._update_display()
    
    def _beat(self):
        """Бито - карты уходят в сброс"""
        for attack, defense in self.table:
            if attack:
                self.discard_pile.append(attack)
            if defense:
                self.discard_pile.append(defense)
        
        self.table.clear()
        self._next_turn_success()
        self._replenish_cards()
        self._update_display()
    
    def _pass_turn(self):
        """Пропуск хода"""
        self._next_turn_success()
        self._update_display()
        self._start_turn()
    
    def _start_turn(self):
        """Начало хода"""
        if not self.game_over and not self.players[self.attacker]['human']:
            self.root.after(1000, self._ai_attack)
    
    def _start_defense(self):
        """Начало защиты"""
        if not self.game_over and not self.players[self.defender]['human']:
            self.root.after(1000, self._ai_defend)
    
    def _ai_attack(self):
        """Ход AI атакующего"""
        if self.game_over:
            return
            
        attacker = self.players[self.attacker]
        if not self.table:
            # Первая атака
            non_trump = [c for c in attacker['cards'] if c['suit'] != self.trump]
            card = min(non_trump if non_trump else attacker['cards'], 
                      key=lambda c: ['6','7','8','9','10','jack','queen','king','ace'].index(c['rank']))
        else:
            # Дополнительная атака
            table_ranks = {pair[0]['rank'] for pair in self.table}
            matching = [c for c in attacker['cards'] if c['rank'] in table_ranks]
            if matching:
                card = min(matching, key=lambda c: ['6','7','8','9','10','jack','queen','king','ace'].index(c['rank']))
            else:
                card = None
        
        if card:
            attacker['cards'].remove(card)
            self.table.append((card, None))
            self._update_display()
            self._start_defense()
        else:
            self._pass_turn()
    
    def _ai_defend(self):
        """Ход AI защитника"""
        if self.game_over:
            return
            
        defender = self.players[self.defender]
        
        attack_card = None
        for attack, defense in self.table:
            if not defense:
                attack_card = attack
                break
        
        if attack_card:
            valid = [c for c in defender['cards'] if self._can_beat(c, attack_card)]
            if valid:
                card = min(valid, key=lambda c: (c['suit'] != self.trump, 
                                               ['6','7','8','9','10','jack','queen','king','ace'].index(c['rank'])))
                defender['cards'].remove(card)
                for i, (a, d) in enumerate(self.table):
                    if a == attack_card and not d:
                        self.table[i] = (a, card)
                        break
                
                self._update_display()
                
                if all(defense is not None for _, defense in self.table):
                    self.root.after(1000, self._beat)
                else:
                    self._start_defense()
            else:
                self._take_cards()
    
    def _next_turn_success(self):
        """Следующий ход после успешной защиты"""
        self.attacker = self.defender
        self.defender = (self.defender + 1) % len(self.players)
        self._start_turn()
    
    def _next_turn_failed(self):
        """Следующий ход после неудачной защиты"""
        self.attacker = (self.defender + 1) % len(self.players)
        self.defender = (self.attacker + 1) % len(self.players)
        self._start_turn()
    
    def _replenish_cards(self):
        """Добирает карты"""
        for player in self.players:
            while len(player['cards']) < 6 and self.deck:
                player['cards'].append(self.deck.pop())
    
    def _check_win(self):
        """Проверяет победу - исправленная логика"""
        # Игра заканчивается, когда у одного из игроков закончились карты
        # И колода пуста, и ход завершен
        if self.game_over:
            return
            
        human_has_cards = len(self.players[0]['cards']) > 0
        bot_has_cards = len(self.players[1]['cards']) > 0
        deck_has_cards = len(self.deck) > 0
        
        # Если у кого-то нет карт и колода пуста - игра окончена
        if not human_has_cards and not deck_has_cards:
            self.game_over = True
            messagebox.showinfo("Игра окончена", "🎉 ПОБЕДИТЕЛЬ: Игрок! 🎉\nПОЗДРАВЛЯЕМ С ПОБЕДОЙ! 🏆")
        elif not bot_has_cards and not deck_has_cards:
            self.game_over = True
            messagebox.showinfo("Игра окончена", "🎉 ПОБЕДИТЕЛЬ: Бот! 🎉\nК сожалению, вы проиграли.")
    def _exit_to_menu(self):
        """Выход в главное меню"""
        if messagebox.askyesno("Выход в меню", "Вы уверены, что хотите выйти в меню?\nТекущая игра будет потеряна."):
            self.root.destroy()
            try:
                import subprocess
                subprocess.run([sys.executable, "menu.py"])
            except:
                print("Не удалось запустить меню")
# ЗАПУСК
if __name__ == "__main__":
    print("🎴 ЗАПУСК ФИНАЛЬНОЙ ВЕРСИИ ДУРАКА")
    print("✅ Ваши текстуры загружены и работают!")
    root = tk.Tk()
    game = CardGame(root)
    root.mainloop()