import pygame
import time
import random

pygame.init()

# Screen configuration
width, height = 800, 600
cellSize = 25
gridW = width // cellSize
gridH = height // cellSize
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Directions
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

class Snake:
    def __init__(self, color, controls):
        self.color = color
        self.controls = controls
        self.pos = [self.randPos()]
        self.direction = right  # Start moving to the right by default

    def randPos(self):
        return (random.randint(5, gridW - 5), random.randint(5, gridH - 5))

    def move(self):
        head = self.pos[0]
        new_head = ((head[0] + self.direction[0]) % gridW, (head[1] + self.direction[1]) % gridH)
        self.pos.insert(0, new_head)
        if len(self.pos) > 1:  # Avoid tail eating immediately after start
            self.pos.pop()

    def change_direction(self, key):
        if key in self.controls:
            new_dir = self.controls[key]
            if len(self.pos) > 1 and new_dir == (-self.direction[0], -self.direction[1]):
                print("Reverse direction attempt blocked.")
            else:
                self.direction = new_dir

    def grow(self):
        self.pos.append(self.pos[-1])

    def draw(self):
        for segment in self.pos:
            pygame.draw.rect(screen, self.color, (segment[0] * cellSize, segment[1] * cellSize, cellSize, cellSize))

class AISnake(Snake):
    def __init__(self, color, food):
        super().__init__(color, {})
        self.food = food

    def move(self):
        head_x, head_y = self.pos[0]
        food_x, food_y = self.food.pos

        if head_x < food_x and (len(self.pos) == 1 or not (head_x + 1, head_y) == self.pos[1]):
            self.direction = right
        elif head_x > food_x and (len(self.pos) == 1 or not (head_x - 1, head_y) == self.pos[1]):
            self.direction = left
        elif head_y < food_y and (len(self.pos) == 1 or not (head_x, head_y + 1) == self.pos[1]):
            self.direction = down
        elif head_y > food_y and (len(self.pos) == 1 or not (head_x, head_y - 1) == self.pos[1]):
            self.direction = up

        super().move()

class Food:
    def __init__(self):
        self.pos = self.randPos()

    def randPos(self):
        return (random.randint(0, gridW - 5), random.randint(0, gridH - 5))

    def draw(self):
        pygame.draw.rect(screen, white, (self.pos[0] * cellSize, self.pos[1] * cellSize, cellSize, cellSize))

def display_game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width / 2, height / 4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    exit()

def main():
    clock = pygame.time.Clock()
    food = Food()
    player_controls = {
        pygame.K_UP: up,
        pygame.K_DOWN: down,
        pygame.K_LEFT: left,
        pygame.K_RIGHT: right
    }
    player_snake = Snake(red, player_controls)
    ai_snake = AISnake(green, food)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                player_snake.change_direction(event.key)

        player_snake.move()
        ai_snake.move()

        if player_snake.pos[0] == food.pos:
            player_snake.grow()
            food = Food()
            ai_snake.food = food
        elif ai_snake.pos[0] == food.pos:
            ai_snake.grow()
            food = Food()
            ai_snake.food = food

        screen.fill(black)
        player_snake.draw()
        ai_snake.draw()
        food.draw()

        pygame.display.flip()
        clock.tick(15)

if __name__ == "__main__":
    main()
