import os
from PIL import Image, ImageTk

class TextureLoader:
    """Класс для загрузки и управления текстурами"""
    
    def __init__(self):
        self._card_textures = {}
        self._card_back_texture = None
        self._table_texture = None
        self._card_width = 100
        self._card_height = 140
    
    def load_card_textures(self, cards_dir: str):
        """Загружает текстуры карт"""
        if not os.path.exists(cards_dir):
            raise FileNotFoundError(f"Папка {cards_dir} не найдена")
        
        # Загрузка рубашки
        back_files = ['back.png', 'card_back.png', 'backside.png', 'рубашка.png']
        for back_file in back_files:
            back_path = os.path.join(cards_dir, back_file)
            if os.path.exists(back_path):
                self._card_back_texture = self._load_and_resize_texture(back_path)
                break
        
        # Загрузка карт
        for filename in os.listdir(cards_dir):
            if filename.endswith('.png') and not any(back in filename for back in back_files):
                filepath = os.path.join(cards_dir, filename)
                texture_name = filename.replace('.png', '')
                self._card_textures[texture_name] = self._load_and_resize_texture(filepath)
    
    def load_table_texture(self, cards_dir: str):
        """Загружает текстуру стола"""
        table_files = ["table.png", "table_texture.png", "table.jpg", "table_texture.jpg"]
        for filename in table_files:
            filepath = os.path.join(cards_dir, filename)
            if os.path.exists(filepath):
                self._table_texture = self._load_and_resize_texture(filepath, 1200, 400)
                return
    
    def _load_and_resize_texture(self, filepath: str, width: int = None, height: int = None):
        """Загружает и изменяет размер текстуры"""
        img = Image.open(filepath)
        if width and height:
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        else:
            img = img.resize((self._card_width, self._card_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    
    def get_card_texture(self, card):
        """Возвращает текстуру карты"""
        return self._card_textures.get(f"{card.rank}_{card.suit}")
    
    @property
    def card_back_texture(self):
        return self._card_back_texture
    
    @property
    def table_texture(self):
        return self._table_texture
    
    @property
    def card_width(self) -> int:
        return self._card_width
    
    @property
    def card_height(self) -> int:
        return self._card_height