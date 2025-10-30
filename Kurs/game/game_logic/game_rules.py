class GameRules:
    """Класс правил игры"""
    
    def __init__(self):
        self._ranks_order = ['6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        self._max_cards_per_player = 6
    
    def can_beat(self, attack_card, defense_card, trump_suit: str) -> bool:
        """Проверяет, может ли defense_card побить attack_card"""
        if defense_card.suit == attack_card.suit:
            return (self._ranks_order.index(defense_card.rank) > 
                   self._ranks_order.index(attack_card.rank))
        elif defense_card.suit == trump_suit and attack_card.suit != trump_suit:
            return True
        return False
    
    def can_add_attack(self, card, table_cards: list) -> bool:
        """Проверяет, можно ли подкинуть карту"""
        if not table_cards:
            return True  # Первая атака
        
        table_ranks = {attack_card.rank for attack_card, _ in table_cards}
        # Также учитываем достоинства уже отбитых карт
        for _, defense_card in table_cards:
            if defense_card:
                table_ranks.add(defense_card.rank)
        
        return card.rank in table_ranks
    
    def is_valid_defense(self, defense_card, attack_card, trump_suit: str) -> bool:
        """Проверяет валидность защиты"""
        return self.can_beat(attack_card, defense_card, trump_suit)
    
    @property
    def max_cards_per_player(self) -> int:
        return self._max_cards_per_player