import tkinter as tk
from tkinter import messagebox

# Абсолютные импорты
from game.cards.deck import Deck
from game.players.human_player import HumanPlayer
from game.players.ai_player import AIPlayer
from game.game_logic.game_table import GameTable
from game.game_logic.game_rules import GameRules
from game.ui.texture_loader import TextureLoader

class CardGameEngine:
    """Основной класс игрового движка"""
    
    def __init__(self):
        self._deck = Deck()
        self._players = []
        self._table = GameTable()
        self._rules = GameRules()
        self._texture_loader = TextureLoader()
        
        self._current_attacker_index = 0
        self._current_defender_index = 1
        self._game_over = False
        self._discard_pile = []
    
    def initialize_game(self):
        """Инициализирует игру"""
        self._deck.shuffle()
        if not self._deck.is_empty:
            trump_card = self._deck.get_top_card()
            self._table.trump_suit = trump_card.suit
        else:
            self._table.trump_suit = 'hearts'
        self._deal_cards()
    
    def add_player(self, player):
        """Добавляет игрока"""
        self._players.append(player)
    
    def _deal_cards(self):
        """Раздает карты игрокам"""
        for player in self._players:
            while player.card_count < self._rules.max_cards_per_player and not self._deck.is_empty:
                card = self._deck.draw_card()
                if card:  # Проверка на None
                    card.is_trump = (card.suit == self._table.trump_suit)
                    player.add_card(card)
    
    def make_attack(self, player_index: int, card) -> bool:
        """Совершает атаку"""
        if player_index >= len(self._players):
            return False
            
        player = self._players[player_index]
        
        if not player.has_card(card):
            return False
            
        if not self._rules.can_add_attack(card, self._table.get_attack_defense_pairs()):
            return False
        
        player.remove_card(card)
        self._table.add_attack(card)
        return True
    
    def make_defense(self, player_index: int, defense_card, attack_index: int) -> bool:
        """Совершает защиту"""
        if player_index >= len(self._players) or attack_index >= self._table.attack_count:
            return False
            
        player = self._players[player_index]
        
        if not player.has_card(defense_card):
            return False
            
        pairs = self._table.get_attack_defense_pairs()
        if attack_index >= len(pairs):
            return False
            
        attack_card = pairs[attack_index][0]
        
        if not self._rules.is_valid_defense(defense_card, attack_card, self._table.trump_suit):
            return False
        
        player.remove_card(defense_card)
        self._table.add_defense(defense_card, attack_index)
        return True
    
    def take_cards(self, player_index: int):
        """Игрок забирает карты со стола"""
        if player_index >= len(self._players):
            return
            
        player = self._players[player_index]
        
        for attack_card, defense_card in self._table.get_attack_defense_pairs():
            player.add_card(attack_card)
            if defense_card:
                player.add_card(defense_card)
        
        self._table.clear()
        self._next_turn_failed()
        self._replenish_cards()
    
    def beat_cards(self):
        """Карты уходят в сброс"""
        for attack_card, defense_card in self._table.get_attack_defense_pairs():
            self._discard_pile.append(attack_card)
            if defense_card:
                self._discard_pile.append(defense_card)
        
        self._table.clear()
        self._next_turn_success()
        self._replenish_cards()
    
    def _next_turn_success(self):
        """Следующий ход после успешной защиты"""
        self._current_attacker_index = self._current_defender_index
        self._current_defender_index = (self._current_defender_index + 1) % len(self._players)
    
    def _next_turn_failed(self):
        """Следующий ход после неудачной защиты"""
        self._current_attacker_index = (self._current_defender_index + 1) % len(self._players)
        self._current_defender_index = (self._current_attacker_index + 1) % len(self._players)
    
    def _replenish_cards(self):
        """Добирает карты игрокам"""
        for player in self._players:
            while player.card_count < self._rules.max_cards_per_player and not self._deck.is_empty:
                card = self._deck.draw_card()
                if card:  # Проверка на None
                    card.is_trump = (card.suit == self._table.trump_suit)
                    player.add_card(card)
    
    def check_win_condition(self) -> bool:
        """Проверяет условия победы"""
        if self._deck.is_empty:
            players_with_cards = [p for p in self._players if p.card_count > 0]
            if len(players_with_cards) == 1:
                self._game_over = True
                return True
        return False

    # МЕТОДЫ ДЛЯ AI ИГРОКА
    def get_table_cards(self):
        """Возвращает карты на столе для AI"""
        return self._table.get_attack_defense_pairs()
    
    def get_unbeaten_attacks(self):
        """Возвращает неотбитые атаки для AI"""
        return self._table.get_unbeaten_attacks()
    
    # Геттеры для доступа к состоянию игры
    @property
    def players(self):
        return self._players
    
    @property
    def current_attacker_index(self):
        return self._current_attacker_index
    
    @property
    def current_defender_index(self):
        return self._current_defender_index
    
    @property
    def current_attacker(self):
        if self._players:
            return self._players[self._current_attacker_index]
        return None
    
    @property
    def current_defender(self):
        if self._players:
            return self._players[self._current_defender_index]
        return None
    
    @property
    def table(self):
        return self._table
    
    @property
    def deck(self):
        return self._deck
    
    @property
    def discard_pile(self):
        return self._discard_pile
    
    @property
    def game_over(self):
        return self._game_over
    
    @property
    def texture_loader(self):
        return self._texture_loader
    
    @property
    def rules(self):
        return self._rules
    
    @property
    def trump_suit(self):
        """Добавляем свойство trump_suit для AI"""
        return self._table.trump_suit