from ..cards.card import Card

class GameTable:
    """Класс игрового стола"""
    
    def __init__(self):
        self._attacks = []  # Атакующие карты
        self._defenses = []  # Защитные карты (None если не отбито)
        self._trump_suit = None
    
    @property
    def trump_suit(self) -> str:
        return self._trump_suit
    
    @trump_suit.setter
    def trump_suit(self, suit: str):
        self._trump_suit = suit
    
    def add_attack(self, card: Card):
        """Добавляет атакующую карту"""
        self._attacks.append(card)
        self._defenses.append(None)
    
    def add_defense(self, card: Card, attack_index: int):
        """Добавляет защитную карту"""
        if 0 <= attack_index < len(self._defenses):
            self._defenses[attack_index] = card
    
    def get_attack_defense_pairs(self) -> list:
        """Возвращает пары атака-защита"""
        return list(zip(self._attacks, self._defenses))
    
    def get_unbeaten_attacks(self) -> list:
        """Возвращает список неотбитых атак"""
        return [self._attacks[i] for i, defense in enumerate(self._defenses) if defense is None]
    
    def is_all_beaten(self) -> bool:
        """Проверяет, все ли атаки отбиты"""
        return all(defense is not None for defense in self._defenses)
    
    def clear(self):
        """Очищает стол"""
        self._attacks.clear()
        self._defenses.clear()
    
    @property
    def attack_count(self) -> int:
        return len(self._attacks)
    
    @property
    def defense_count(self) -> int:
        return sum(1 for defense in self._defenses if defense is not None)