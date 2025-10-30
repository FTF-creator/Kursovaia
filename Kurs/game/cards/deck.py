import random
from .card import Card

class Deck:
    """Класс колоды карт"""
    
    def __init__(self):
        self._cards = []
        self._create_deck()
    
    def _create_deck(self):
        """Создает стандартную колоду из 36 карт"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        
        self._cards = [Card(rank, suit) for suit in suits for rank in ranks]
    
    def shuffle(self):
        """Перемешивает колоду"""
        random.shuffle(self._cards)
    
    def draw_card(self) -> Card:
        """Берет карту из колоды"""
        return self._cards.pop() if self._cards else None
    
    def add_card(self, card: Card):
        """Добавляет карту в колоду"""
        self._cards.append(card)
    
    @property
    def count(self) -> int:
        return len(self._cards)
    
    @property
    def is_empty(self) -> bool:
        return len(self._cards) == 0
    
    def get_top_card(self) -> Card:
        """Возвращает верхнюю карту без удаления"""
        return self._cards[-1] if self._cards else None