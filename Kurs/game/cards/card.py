class Card:
    """Базовый класс карты"""
    
    def __init__(self, rank: str, suit: str):
        self._rank = rank
        self._suit = suit
        self._is_trump = False
    
    @property
    def rank(self) -> str:
        return self._rank
    
    @property
    def suit(self) -> str:
        return self._suit
    
    @property
    def is_trump(self) -> bool:
        return self._is_trump
    
    @is_trump.setter
    def is_trump(self, value: bool):
        self._is_trump = value
    
    def __str__(self) -> str:
        return f"{self._rank}_{self._suit}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self._rank == other.rank and self._suit == other.suit
    
    def get_texture_filename(self) -> str:
        return f"{self._rank}_{self._suit}.png"