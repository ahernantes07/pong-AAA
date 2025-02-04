import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colores
white = (255, 255, 0)
black = (0, 0, 0)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 10

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        if keys[up] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(screen_width // 2 - 10, screen_height // 2 - 10, 20, 20)
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1
        if self.rect.left <= 0:
            return 'right'
        if self.rect.right >= screen_width:
            return 'left'
        return None

    def draw(self):
        pygame.draw.ellipse(screen, white, self.rect)

    def reset(self):
        self.rect.x, self.rect.y = screen_width // 2 - 10, screen_height // 2 - 10
        self.speed_x *= -1

class Game:
    def __init__(self):
        self.left_paddle = Paddle(10, screen_height // 2 - 50)
        self.right_paddle = Paddle(screen_width - 20, screen_height // 2 - 50)
        self.ball = Ball()
        self.left_score = 0
        self.right_score = 0
        self.font = pygame.font.Font(None, 74)

    def draw(self):
        screen.fill(black)
        self.left_paddle.draw()
        self.right_paddle.draw()
        self.ball.draw()
        pygame.draw.aaline(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))

        left_text = self.font.render(str(self.left_score), True, white)
        screen.blit(left_text, (screen_width // 4, 20))
        right_text = self.font.render(str(self.right_score), True, white)
        screen.blit(right_text, (screen_width * 3 // 4, 20))

    def update(self):
        self.left_paddle.move(pygame.K_w, pygame.K_s)
        self.right_paddle.move(pygame.K_UP, pygame.K_DOWN)
        result = self.ball.move()

        if result == 'left':
            self.right_score += 1
            self.ball.reset()
            self.background_color = random.choice(colors)
        if result == 'right':
            self.left_score += 1
            self.ball.reset()
            self.background_color = random.choice(colors)

        if self.ball.rect.colliderect(self.left_paddle.rect) or self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.speed_x *= -1

# Bucle principal del juego
game = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.update()
    game.draw()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
