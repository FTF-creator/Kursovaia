import random
from .player import Player
from ..cards.card import Card

class AIPlayer(Player):
    """Класс AI игрока с разными стратегиями"""
    
    def __init__(self, name: str = "Бот", difficulty: str = "medium"):
        super().__init__(name)
        self._difficulty = difficulty
        self._ranks_order = ['6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    
    def make_move(self, game_state) -> Card:
        """AI выбирает карту для атаки"""
        table_cards = game_state.get_table_cards()
        trump_suit = game_state.trump_suit
        
        if not table_cards:
            # Первая атака - выбираем самую слабую некозырную карту
            return self._get_weakest_non_trump_card(trump_suit)
        else:
            # Дополнительная атака - ищем карты того же достоинства
            table_ranks = set()
            for attack_card, defense_card in table_cards:
                table_ranks.add(attack_card.rank)
                if defense_card:
                    table_ranks.add(defense_card.rank)
            
            matching_cards = [card for card in self._cards if card.rank in table_ranks]
            if matching_cards:
                return min(matching_cards, key=lambda c: self._ranks_order.index(c.rank))
        
        return None
    
    def defend(self, attack_card: Card, game_state) -> Card:
        """AI выбирает карту для защиты"""
        trump_suit = game_state.trump_suit
        valid_cards = self._get_valid_defense_cards(attack_card, trump_suit)
        
        if valid_cards:
            # Выбираем самую слабую подходящую карту
            return min(valid_cards, key=lambda c: (
                c.suit != trump_suit,  # Сначала некозырные
                self._ranks_order.index(c.rank)  # Потом по старшинству
            ))
        
        return None
    
    def _get_weakest_non_trump_card(self, trump_suit: str) -> Card:
        """Возвращает самую слабую некозырную карту"""
        non_trump_cards = [card for card in self._cards if card.suit != trump_suit]
        if non_trump_cards:
            return min(non_trump_cards, key=lambda c: self._ranks_order.index(c.rank))
        # Если все карты козырные, берем самую слабую
        return min(self._cards, key=lambda c: self._ranks_order.index(c.rank))
    
    def _get_valid_defense_cards(self, attack_card: Card, trump_suit: str) -> list:
        """Возвращает карты, которыми можно побить атаку"""
        valid_cards = []
        
        for card in self._cards:
            if card.suit == attack_card.suit:
                if self._ranks_order.index(card.rank) > self._ranks_order.index(attack_card.rank):
                    valid_cards.append(card)
            elif card.suit == trump_suit and attack_card.suit != trump_suit:
                valid_cards.append(card)
        
        return valid_cards