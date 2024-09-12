class GameStats():
    """Отслеживание статистики для игры Alien Invasion"""
    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра Alien Invasion запускается в активном состоянии
        self.game_active = False
        # Рекорд не должен сбрасываться
        self.high_score = 0
        try:
            with open('record.txt') as file_object:
                high_score = file_object.read()
            self.high_score = int(high_score)
        except FileNotFoundError:
            pass
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

