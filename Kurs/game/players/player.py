from abc import ABC, abstractmethod
from ..cards.card import Card

class Player(ABC):
    """Абстрактный базовый класс игрока"""
    
    def __init__(self, name: str):
        self._name = name
        self._cards = []
        self._is_attacker = False
        self._is_defender = False
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def cards(self) -> list:
        return self._cards.copy()
    
    @property
    def card_count(self) -> int:
        return len(self._cards)
    
    @property
    def is_attacker(self) -> bool:
        return self._is_attacker
    
    @is_attacker.setter
    def is_attacker(self, value: bool):
        self._is_attacker = value
    
    @property
    def is_defender(self) -> bool:
        return self._is_defender
    
    @is_defender.setter
    def is_defender(self, value: bool):
        self._is_defender = value
    
    def add_card(self, card: Card):
        """Добавляет карту игроку"""
        self._cards.append(card)
    
    def remove_card(self, card: Card):
        """Удаляет карту у игрока"""
        self._cards.remove(card)
    
    def has_card(self, card: Card) -> bool:
        """Проверяет наличие карты у игрока"""
        return card in self._cards
    
    @abstractmethod
    def make_move(self, game_state) -> Card:
        """Абстрактный метод для совершения хода"""
        pass
    
    @abstractmethod
    def defend(self, attack_card: Card, game_state) -> Card:
        """Абстрактный метод для защиты"""
        pass