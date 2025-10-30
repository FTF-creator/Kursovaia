import tkinter as tk
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(__file__))

from game.game_engine import CardGameEngine
from game.players.human_player import HumanPlayer
from game.players.ai_player import AIPlayer
from game.ui.game_ui import CardGameUI

def main():
    """Основная функция запуска игры"""
    print("=== ФИНАЛЬНАЯ ВЕРСИЯ ДУРАКА ===")
    print("🔄 Запуск игры...")
    
    root = tk.Tk()
    root.title("ДУРАК - ФИНАЛЬНАЯ ВЕРСИЯ")
    root.geometry("1200x700")
    root.configure(bg='#2E8B57')
    
    # Создаем игровой движок
    game_engine = CardGameEngine()
    
    # Добавляем игроков
    game_engine.add_player(HumanPlayer("Игрок"))
    game_engine.add_player(AIPlayer("Бот"))
    
    # Загружаем текстуры
    try:
        # Получаем абсолютный путь к папке cards
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cards_dir = os.path.join(current_dir, "cards")
        
        print(f"🔍 Ищем текстуры в: {cards_dir}")
        
        if not os.path.exists(cards_dir):
            print("❌ Папка cards не найдена! Создаю...")
            os.makedirs(cards_dir, exist_ok=True)
            print("✅ Папка cards создана")
            print("⚠️  Добавьте текстуры карт в папку cards:")
            print("   - back.png (рубашка карты)")
            print("   - table.png (текстура стола)")
            print("   - 6_hearts.png, 7_hearts.png, ... (карты)")
            return
        
        # Проверяем есть ли файлы в папке
        files = os.listdir(cards_dir)
        print(f"📁 Найдено файлов в cards: {len(files)}")
        
        game_engine.texture_loader.load_card_textures(cards_dir)
        game_engine.texture_loader.load_table_texture(cards_dir)
        print("✅ Текстуры загружены успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка загрузки текстур: {e}")
        print("⚠️  Убедитесь, что в папке cards есть необходимые текстуры")
        return
    
    # Инициализируем игру
    game_engine.initialize_game()
    
    # Создаем UI
    game_ui = CardGameUI(root, game_engine)
    
    print("🎮 Игра запущена!")
    root.mainloop()

if __name__ == "__main__":
    main()