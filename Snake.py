import pygame
import time
import random

pygame.init()

# Screen
width, height = 800, 600
cellSize = 25
gridW = width // cellSize
gridH = height // cellSize
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

# Colors for bg/players/food
black = pygame.Color(0, 0, 0)   # Background
white = pygame.Color(255, 255, 255) # Food
red = pygame.Color(255, 0, 0)   # Snake 1
green = pygame.Color(0, 255, 0) # Snake 2

# Directions
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

class Snake:
    def __init__(self, color):
        self.color = color
        self.pos = [self.randPos()]
        self.direction = random.choice([up, down, left, right])

    def randPos(self):
            return (random.randint(0, gridW - 1), random.randint(0, gridH - 1))
    
    def move(self):
        head = self.pos[0]
        dx, dy = self.direction
        x, y = head
        new_head = ((x + dx) % gridW, (y + dy) % gridH)
        self.pos.insert(0, new_head)
        self.pos.pop()

    def grow(self):
        self.pos.append(self.pos[-1])

    def draw(self):
        for segment in self.pos:
            x, y = segment
            pygame.draw.rect(screen, self.color, (x * cellSize, y * cellSize, cellSize, cellSize))
    
class Food:
    def __init__(self):
        self.pos = self.randPos()

    def randPos(self):
        return (random.randint(0, gridW - 5), random.randint(0, gridH - 5))

    def draw(self):
        x, y = self.pos
        pygame.draw.rect(screen, white, (x * cellSize, y * cellSize, cellSize, cellSize))

def main():
    clock = pygame.time.Clock()
    snake = Snake(red)
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != down:
                    snake.direction = up
                elif event.key == pygame.K_LEFT and snake.direction != right:
                    snake.direction = left
                elif event.key == pygame.K_DOWN and snake.direction != up:
                    snake.direction = down
                elif event.key == pygame.K_RIGHT and snake.direction != left:
                    snake.direction = right
        snake.move()

        screen.fill(black)  # Black background following snakes movement

        # Filler game over condition
        if snake.pos[0] in snake.pos[1:]:
            my_font = pygame.font.SysFont('times new roman', 50)
            
            # creating a text surface on which text 
            # will be drawn
            game_over_surface = my_font.render(
                'Game Over', True, red)
            
            # create a rectangular object for the text 
            # surface object
            game_over_rect = game_over_surface.get_rect()
            
            # setting position of the text
            game_over_rect.midtop = (width/2, height/4)
            
            # blit will draw the text on screen
            screen.blit(game_over_surface, game_over_rect)
            pygame.display.flip()
            
            # after 2 seconds we will quit the program
            time.sleep(2)
            
            # deactivating pygame library
            pygame.quit()

        if snake.pos[0] == food.pos:
            snake.grow()
            food.pos = food.randPos()

        snake.draw()
        food.draw()

        clock.tick(15)
        pygame.display.flip()
        

if __name__ == "__main__":
    main()
