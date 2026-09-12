import pygame
import sys
import os
import random

def resource_path(relative_path):
    """
    Get the absolute path to a resource file.
    Works for both development and when packaged into an executable by PyInstaller.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Entity:
    """
    Class representing a game entity (fruit or bomb).
    """
    def __init__(self, kind):
        self.kind = kind
        self.hit = False
        self.throw = False
        self.x = 0
        self.y = 800
        self.speed_x = 0
        self.speed_y = 0
        self.t = 0
        self.img = None
        self.reset()

    def reset(self):
        """Reset the entity with random position and speed."""
        fruit_path = resource_path(f"images/{self.kind}.png")
        self.img = pygame.image.load(fruit_path)
        self.x = random.randint(100, 500)
        self.y = 800
        self.speed_x = random.randint(-10, 10)
        self.speed_y = random.randint(-80, -60)
        self.t = 0
        self.hit = False
        # 75% chance to throw this entity
        self.throw = random.random() >= 0.75

    def update(self):
        """Update the entity's position."""
        if self.throw:
            self.x += self.speed_x
            self.y += self.speed_y
            self.speed_y += (1 * self.t)
            self.t += 1
            if self.y > 800:
                self.reset()
        else:
            self.reset()

    def draw(self, display):
        """Draw the entity on the given display."""
        if self.throw and self.y <= 800:
            display.blit(self.img, (self.x, self.y))

    def check_hit(self, pos):
        """Check if the entity is hit by the mouse."""
        if not self.hit and self.throw and self.y <= 800:
            mx, my = pos
            if self.x < mx < self.x + 60 and self.y < my < self.y + 60:
                return True
        return False

    def hit_effect(self):
        """Apply the effect when the entity is hit."""
        self.hit = True
        self.speed_x += 10
        if self.kind == 'bomb':
            img_path = resource_path("images/explosion.png")
        else:
            img_path = resource_path(f"images/half_{self.kind}.png")
        self.img = pygame.image.load(img_path)

class Game:
    """
    Main Game class handling the loop, rendering, and logic.
    """
    WIDTH = 800
    HEIGHT = 600
    FPS = 12
    WHITE = (255, 255, 255)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Fruit-Ninja')

        icon_img = pygame.image.load(resource_path('images/fruit-ninja.png'))
        pygame.display.set_icon(icon_img)

        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load(resource_path('images/back.jpg'))
        self.font = pygame.font.Font(resource_path('font/comic.ttf'), 42)

        self.fruits_list = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']

        self.player_lives = 3
        self.score = 0
        self.game_over = True
        self.first_round = True
        self.running = True

        self.entities = []

    def draw_text(self, text, size, x, y, color=WHITE):
        """Helper to draw text on the screen."""
        try:
            font = pygame.font.Font(resource_path('font/comic.ttf'), size)
        except Exception:
            font_name = pygame.font.match_font('comic.ttf')
            font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_lives(self):
        """Draw the player's remaining lives."""
        img_path = resource_path('images/red_lives.png')
        img = pygame.image.load(img_path)
        for i in range(self.player_lives):
            img_rect = img.get_rect()
            img_rect.x = 690 + 35 * i
            img_rect.y = 5
            self.display.blit(img, img_rect)

    def hide_cross_lives(self, x, y):
        """Draw a cross indicating a lost life."""
        self.display.blit(pygame.image.load(resource_path("images/red_lives.png")), (x, y))

    def show_gameover_screen(self):
        """Display the game over / start screen."""
        self.display.blit(self.background, (0, 0))
        self.draw_text("FRUIT NINJA!", 90, self.WIDTH / 2, self.HEIGHT / 4)

        if not self.game_over:
            self.draw_text(f"Score : {self.score}", 50, self.WIDTH / 2, self.HEIGHT / 2)

        self.draw_text("Press a key to begin!", 64, self.WIDTH / 2, self.HEIGHT * 3 / 4)
        pygame.display.flip()

        waiting = True
        while waiting:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def reset_game(self):
        """Reset the game state for a new round."""
        self.game_over = False
        self.player_lives = 3
        self.score = 0
        self.entities = [Entity(f) for f in self.fruits_list]

    def run(self):
        """Main game loop."""
        while self.running:
            if self.game_over:
                if self.first_round:
                    self.show_gameover_screen()
                    self.first_round = False
                self.reset_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.blit(self.background, (0, 0))

            score_text = self.font.render(f'Score : {self.score}', True, self.WHITE)
            self.display.blit(score_text, (0, 0))

            self.draw_lives()

            pos = pygame.mouse.get_pos()

            for entity in self.entities:
                entity.update()
                entity.draw(self.display)

                if entity.check_hit(pos):
                    if entity.kind == 'bomb':
                        self.player_lives -= 1

                        if self.player_lives == 0:
                            self.hide_cross_lives(690, 15)
                        elif self.player_lives == 1:
                            self.hide_cross_lives(725, 15)
                        elif self.player_lives == 2:
                            self.hide_cross_lives(760, 15)
                            
                        if self.player_lives <= 0:
                            self.show_gameover_screen()
                            self.game_over = True
                    else:
                        self.score += 1
                        
                    entity.hit_effect()

            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
