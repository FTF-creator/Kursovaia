from .player import Player
from ..cards.card import Card

class HumanPlayer(Player):
    """Класс человеческого игрока"""
    
    def __init__(self, name: str = "Игрок"):
        super().__init__(name)
        self._selected_card = None
    
    def make_move(self, game_state) -> Card:
        """Человек выбирает карту через UI"""
        return self._selected_card
    
    def defend(self, attack_card: Card, game_state) -> Card:
        """Человек выбирает карту для защиты через UI"""
        return self._selected_card
    
    def select_card(self, card: Card):
        """Выбирает карту для хода"""
        self._selected_card = card
    
    def clear_selection(self):
        """Очищает выбор карты"""
        self._selected_card = None