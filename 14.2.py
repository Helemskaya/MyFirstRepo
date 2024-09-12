import pygame
import sys
import pygame.font
from pygame.sprite import Sprite
from time import sleep
class Ship():
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/alien.bmp')
        self.image_rect = self.image.get_rect()
        self.image_rect.midleft = self.screen_rect.midleft
        self.move_up = False
        self.move_down = False
    def update(self):
        if self.move_up and self.image_rect.y > 0:
            self.image_rect.y -= 2
        if self.move_down and (self.image_rect.bottom < self.screen_rect.bottom):
            self.image_rect.y += 2
    def blit_me(self):
        self.screen.blit(self.image, self.image_rect)
class Bullet(Sprite):
        def __init__(self, ai_game):
            super().__init__()
            self.screen = ai_game.screen
            self.color = (60, 60, 60)
            self.rect = pygame.Rect(0, 0, 15, 3)
            self.rect.midright = ai_game.ship.image_rect.midright
        def update(self):
            self.rect.x += 2
        def draw_bullet(self):
            pygame.draw.rect(self.screen, self.color, self.rect)
class Kube(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.rect = pygame.Rect(0, 0, 200, 200)
        self.color = (0, 255, 0)
        self.rect.midright = self.screen_rect.midright
        self.fleet_direction = 1
        self.speed = 1.2
    def update(self):
        self.rect.y += self.speed * self.fleet_direction
    def check_edges(self):
        if self.rect.top <= 0 or self.rect.bottom >= self.screen_rect.bottom:
            return True
    def draw_kube(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Button():
    def __init__(self,ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.color_text = (255, 255, 255)
        self.color_button = (0, 255, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)
    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.color_text,
                                          self.color_button)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_button(self):
        self.screen.fill(self.color_button, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
class Stats():
    def __init__(self):
        self.reset_stats()
        self.game_active = False
    def reset_stats(self):
        self.left_try = 3
class MyGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.bg_color = (230, 0, 230)
        self.stats = Stats()
        self.ship = Ship(self.screen)
        self.kubes = pygame.sprite.Group()
        kube = Kube(self)
        self.kubes.add(kube)
        self.bullets = pygame.sprite.Group()
        self.play_button = Button(self, 'Play')
    def run_game(self):
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_kube()
                self.update_bullets()
            self.screen_update()
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.ship.move_up = True
                elif event.key == pygame.K_DOWN:
                    self.ship.move_down = True
                elif event.key == pygame.K_SPACE:
                    self.fire_bullet()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.ship.move_up = False
                elif event.key == pygame.K_DOWN:
                    self.ship.move_down = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_clicked = self.play_button.rect.collidepoint(mouse_pos)
                if button_clicked and not self.stats.game_active:
                    self._start_game()
    def _start_game(self):
        for kube in self.kubes.sprites():
            kube.speed = 1.2
        self.stats.reset_stats()
        self.stats.game_active = True
        self.bullets.empty()
        self.ship.image_rect.midleft = self.ship.screen_rect.midleft
    def fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.ship.screen_rect.right:
                self.left_one_try()
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.kubes, True, False)
        if collisions:
            self.bullets.empty()
            for kube in self.kubes.sprites():
                sleep(0.5)
                kube.speed *= 1.5
                kube.rect.midright = kube.screen_rect.midright
    def left_one_try(self):
        if self.stats.left_try > 0:
            self.stats.left_try -= 1
            self.bullets.empty()
        else:
            self.stats.game_active = False

    def _check_kube_edges(self):
        for kube in self.kubes:
            if kube.check_edges():
                self._change_kube_direction()
    def _change_kube_direction(self):
        for kube in self.kubes:
            kube.fleet_direction *= -1

    def update_kube(self):
        self._check_kube_edges()
        self.kubes.update()

    def screen_update(self):
        self.screen.fill(self.bg_color)
        self.ship.blit_me()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for kube in self.kubes.sprites():
            kube.draw_kube()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    game = MyGame()
    game.run_game()

