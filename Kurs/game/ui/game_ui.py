import tkinter as tk
from tkinter import messagebox
import os
import sys

class CardGameUI:
    """Класс для управления пользовательским интерфейсом игры"""
    
    def __init__(self, root, game_engine):
        self.root = root
        self.game_engine = game_engine
        self.card_widgets = []
        
        self._create_ui()
        self._update_display()
    
    def _create_ui(self):
        """Создает пользовательский интерфейс"""
        # Верхняя панель
        top = tk.Frame(self.root, bg='#2E8B57', height=80)
        top.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(top, text="🎴 ДУРАК - ООП АРХИТЕКТУРА", 
                                   font=('Arial', 14, 'bold'), bg='#2E8B57', fg='white')
        self.status_label.pack(pady=5)
        
        suit_symbols = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}
        trump_symbol = suit_symbols.get(self.game_engine.table.trump_suit, '?')
        self.trump_label = tk.Label(top, text=f"Козырь: {trump_symbol}", 
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
        self._create_control_buttons()
    
    def _create_control_buttons(self):
        """Создает кнопки управления"""
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
    
    def _update_display(self):
        """Обновляет отображение игры"""
        # Очищаем старые карты
        for widget in self.card_widgets:
            widget.destroy()
        self.card_widgets = []
        
        # Показываем карты бота (рубашкой вверх)
        bot = self.game_engine.players[1]
        for card in bot.cards:
            self._create_card_widget(self.bot_cards_frame, card, is_human=False)
        
        # Показываем карты игрока
        human = self.game_engine.players[0]
        can_attack = (not self.game_engine.game_over and 
                     self.game_engine.current_attacker_index == 0)
        can_defend = (not self.game_engine.game_over and 
                     self.game_engine.current_defender_index == 0 and 
                     self.game_engine.table.attack_count > 0)
        
        for card in human.cards:
            self._create_card_widget(self.player_cards_frame, card, is_human=True,
                                   can_interact=can_attack or can_defend, card_obj=card)
        
        # Обновляем стол
        self._draw_table()
        
        # Обновляем статус и информацию
        attacker_name = self.game_engine.current_attacker.name
        defender_name = self.game_engine.current_defender.name
        self.status_label.config(text=f"🎯 Атакует: {attacker_name} | 🛡️ Защищается: {defender_name}")
        
        # Обновляем информацию о картах
        human_count = len(self.game_engine.players[0].cards)
        bot_count = len(self.game_engine.players[1].cards)
        deck_count = self.game_engine.deck.count
        discard_count = len(self.game_engine.discard_pile)
        self.info_label.config(text=f"📊 Карты: Вы ({human_count}) | Бот ({bot_count}) | Колода ({deck_count}) | Отбой ({discard_count})")
        
        # Проверяем победу
        if self.game_engine.check_win_condition():
            self._show_winner()
        
        # Обновляем кнопки
        self._update_buttons()
    
    def _create_card_widget(self, parent, card, is_human=True, can_interact=False, card_obj=None):
        """Создает виджет карты"""
        card_width = self.game_engine.texture_loader.card_width
        card_height = self.game_engine.texture_loader.card_height
        
        card_frame = tk.Frame(parent, width=card_width, height=card_height,
                            relief=tk.RAISED, borderwidth=2, bg='white')
        card_frame.pack_propagate(False)
        card_frame.pack(side=tk.LEFT, padx=3)
        
        card_canvas = tk.Canvas(card_frame, width=card_width, height=card_height, 
                              bg='white', highlightthickness=0)
        card_canvas.pack(fill=tk.BOTH, expand=True)
        
        if is_human:
            # Карты игрока - лицевой стороной
            texture = self.game_engine.texture_loader.get_card_texture(card)
            if texture:
                card_canvas.create_image(0, 0, image=texture, anchor=tk.NW)
                
                if card.is_trump:
                    card_canvas.create_rectangle(2, 2, card_width-2, card_height-2,
                                               outline='gold', width=3)
        else:
            # Карты бота - рубашкой
            back_texture = self.game_engine.texture_loader.card_back_texture
            if back_texture:
                card_canvas.create_image(0, 0, image=back_texture, anchor=tk.NW)
        
        if can_interact and card_obj:
            card_canvas.bind('<Button-1>', lambda e, c=card_obj: self._on_card_click(c))
            card_canvas.bind('<Enter>', lambda e, f=card_frame: f.configure(bg='lightblue'))
            card_canvas.bind('<Leave>', lambda e, f=card_frame: f.configure(bg='white'))
            card_canvas.config(cursor="hand2")
        
        self.card_widgets.append(card_frame)
    
    def _draw_table(self):
        """Рисует игровой стол"""
        self.table_canvas.delete("all")
        
        # Рисуем текстуру стола если есть
        table_texture = self.game_engine.texture_loader.table_texture
        if table_texture:
            self.table_canvas.create_image(0, 0, image=table_texture, anchor=tk.NW)
        
        # Рисуем общую колоду слева с рубашкой
        if not self.game_engine.deck.is_empty:
            back_texture = self.game_engine.texture_loader.card_back_texture
            if back_texture:
                deck_x, deck_y = 50, 150
                self.table_canvas.create_image(deck_x, deck_y, image=back_texture, anchor=tk.NW)
                self.table_canvas.create_text(deck_x + 50, deck_y + 160,
                                            text=f"Колода\n{self.game_engine.deck.count}", 
                                            font=('Arial', 12, 'bold'), 
                                            fill='white' if not table_texture else 'black',
                                            justify=tk.CENTER)
        
        # Рисуем отбой справа с рубашкой
        if self.game_engine.discard_pile:
            back_texture = self.game_engine.texture_loader.card_back_texture
            if back_texture:
                discard_x, discard_y = 1000, 150
                self.table_canvas.create_image(discard_x, discard_y, image=back_texture, anchor=tk.NW)
                self.table_canvas.create_text(discard_x + 50, discard_y + 160,
                                            text=f"Отбой\n{len(self.game_engine.discard_pile)}", 
                                            font=('Arial', 12, 'bold'),
                                            fill='white' if not table_texture else 'black',
                                            justify=tk.CENTER)
        
        # Рисуем козырь
        trump_x, trump_y = 50, 50
        suit_symbols = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}
        symbol = suit_symbols.get(self.game_engine.table.trump_suit, '?')
        color = 'red' if self.game_engine.table.trump_suit in ['hearts', 'diamonds'] else 'white'
        self.table_canvas.create_text(trump_x, trump_y, text=f"Козырь: {symbol}", 
                                    font=('Arial', 14, 'bold'), 
                                    fill=color if not table_texture else 'black')
        
        # Рисуем карты на столе
        pairs = self.game_engine.table.get_attack_defense_pairs()
        if not pairs:
            if self.game_engine.deck.is_empty and not self.game_engine.discard_pile:
                self.table_canvas.create_text(600, 200, text="🎴 Стол пуст", 
                                            font=('Arial', 16), 
                                            fill='white' if not table_texture else 'black')
            return
        
        # Рисуем карты на столе для атаки/защиты по центру
        x, y = 400, 150
        for attack_card, defense_card in pairs:
            # Атакующая карта
            attack_texture = self.game_engine.texture_loader.get_card_texture(attack_card)
            if attack_texture:
                self.table_canvas.create_image(x, y, image=attack_texture, anchor=tk.NW)
            
            # Защитная карта
            if defense_card:
                defense_texture = self.game_engine.texture_loader.get_card_texture(defense_card)
                if defense_texture:
                    self.table_canvas.create_image(x+80, y, image=defense_texture, anchor=tk.NW)
            else:
                text_color = 'white' if not table_texture else 'black'
                self.table_canvas.create_text(x+40, y+120, text="❌", 
                                            font=('Arial', 16), fill=text_color)
            
            x += 160
    
    def _on_card_click(self, card):
        """Обработка клика по карте игрока"""
        if self.game_engine.game_over:
            return
        
        human_player = self.game_engine.players[0]
        
        if self.game_engine.current_attacker_index == 0:  # Игрок атакует
            if self.game_engine.make_attack(0, card):
                self._update_display()
                self._start_ai_defense()
            else:
                messagebox.showinfo("Нельзя атаковать", "Нельзя подкидывать эту карту")
        
        elif self.game_engine.current_defender_index == 0:  # Игрок защищается
            # Находим первую неотбитую атаку
            unbeaten_attacks = self.game_engine.get_unbeaten_attacks()
            if unbeaten_attacks:
                # Находим индекс этой атаки
                pairs = self.game_engine.table.get_attack_defense_pairs()
                for i, (attack, defense) in enumerate(pairs):
                    if defense is None and attack == unbeaten_attacks[0]:
                        if self.game_engine.make_defense(0, card, i):
                            self._update_display()
                            if self.game_engine.table.is_all_beaten():
                                self.root.after(1000, self._beat_cards)
                            else:
                                self._start_ai_defense()
                        else:
                            messagebox.showwarning("Нельзя отбиться", "Эта карта не может побить атакующую карту!")
                        break
    
    def _take_cards(self):
        """Игрок берет карты"""
        self.game_engine.take_cards(self.game_engine.current_defender_index)
        self._update_display()
        self._start_ai_attack()
    
    def _beat_cards(self):
        """Карты уходят в сброс"""
        self.game_engine.beat_cards()
        self._update_display()
        self._start_ai_attack()
    
    def _pass_turn(self):
        """Пропуск хода"""
        # Используем внутренние методы game_engine
        self.game_engine._next_turn_success()
        self.game_engine._replenish_cards()
        self._update_display()
        self._start_ai_attack()
    
    def _start_ai_attack(self):
        """Запускает ход AI атакующего"""
        if (not self.game_engine.game_over and 
            self.game_engine.current_attacker_index == 1):
            self.root.after(1000, self._ai_attack)
    
    def _start_ai_defense(self):
        """Запускает защиту AI"""
        if (not self.game_engine.game_over and 
            self.game_engine.current_defender_index == 1):
            self.root.after(1000, self._ai_defend)
    
    def _ai_attack(self):
        """Ход AI атакующего"""
        if self.game_engine.game_over:
            return
        
        ai_player = self.game_engine.players[1]
        card = ai_player.make_move(self.game_engine)
        
        if card and self.game_engine.make_attack(1, card):
            self._update_display()
            # После атаки AI, игрок может подкидывать
        else:
            # AI пропускает ход
            self.game_engine._next_turn_success()
            self.game_engine._replenish_cards()
            self._update_display()
    
    def _ai_defend(self):
        """Защита AI"""
        if self.game_engine.game_over:
            return
        
        ai_player = self.game_engine.players[1]
        unbeaten_attacks = self.game_engine.get_unbeaten_attacks()
        
        if unbeaten_attacks:
            defense_card = ai_player.defend(unbeaten_attacks[0], self.game_engine)
            if defense_card:
                # Находим индекс атаки для защиты
                pairs = self.game_engine.table.get_attack_defense_pairs()
                for i, (attack, defense) in enumerate(pairs):
                    if defense is None and attack == unbeaten_attacks[0]:
                        self.game_engine.make_defense(1, defense_card, i)
                        self._update_display()
                        
                        if self.game_engine.table.is_all_beaten():
                            self.root.after(1000, self._beat_cards)
                        else:
                            self._start_ai_defense()
                        break
            else:
                # AI не может отбиться - забирает карты
                self.game_engine.take_cards(1)
                self._update_display()
                self._start_ai_attack()
    
    def _update_buttons(self):
        """Обновляет состояние кнопок"""
        self.take_btn.config(state=tk.DISABLED)
        self.pass_btn.config(state=tk.DISABLED)
        
        if self.game_engine.game_over:
            return
        
        # Кнопка ВЗЯТЬ КАРТЫ активна для защищающегося игрока
        if (self.game_engine.current_defender_index == 0 and 
            self.game_engine.table.attack_count > 0):
            self.take_btn.config(state=tk.NORMAL)
        
        # Кнопка ПРОПУСТИТЬ активна для атакующего игрока
        if self.game_engine.current_attacker_index == 0:
            self.pass_btn.config(state=tk.NORMAL)
    
    def _show_winner(self):
        """Показывает победителя"""
        if self.game_engine.players[0].card_count == 0:
            messagebox.showinfo("Игра окончена", "🎉 ПОБЕДИТЕЛЬ: Игрок! 🎉\nПОЗДРАВЛЯЕМ С ПОБЕДОЙ! 🏆")
        else:
            messagebox.showinfo("Игра окончена", "🎉 ПОБЕДИТЕЛЬ: Бот! 🎉\nК сожалению, вы проиграли.")
    
    def _exit_to_menu(self):
        """Выход в главное меню"""
        if messagebox.askyesno("Выход в меню", "Вы уверены, что хотите выйти в меню?\nТекущая игра будет потеряна."):
            self.root.destroy()
            try:
                # Создаем простой menu.py если его нет
                menu_path = os.path.join(os.path.dirname(__file__), "..", "menu.py")
                if not os.path.exists(menu_path):
                    print("⚠️  Файл menu.py не найден, создаем простую версию...")
                    self._create_simple_menu()
                import subprocess
                subprocess.run([sys.executable, "menu.py"])
            except Exception as e:
                print(f"Не удалось запустить меню: {e}")
    
    def _create_simple_menu(self):
        """Создает простой файл меню если его нет"""
        menu_content = '''import tkinter as tk
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
'''
        with open("menu.py", "w", encoding="utf-8") as f:
            f.write(menu_content)
        print("✅ Простой menu.py создан")