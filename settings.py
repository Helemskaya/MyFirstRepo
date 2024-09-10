class Settings():
    def __init__(self):
        # Инициализирует статические настройки игры
        # Параметры экрана
        self.screen_width = 1200
        self.screen_heigh = 800
        self.color_bg = (230, 230, 230)
        # Параметры корабля
        self.ship_limit = 3
        # Параметры снаряда
        self.bullet_width = 1200
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Параметры пришельца
        self.fleet_drop_speed = 10
        # Темп ускорения игры
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 10.0
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево
        self.fleet_direction = 1
        self.alien_point = 50

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_point = int(self.alien_point * self.score_scale)



