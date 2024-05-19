import pygame
import heapq
import time
import random

pygame.init()

# Screen configuration
width, height = 800, 600
cellSize = 25
gridW = width // cellSize #32
gridH = height // cellSize #24
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
yellow = pygame.Color(240, 255, 0)
blue = pygame.Color(0, 170, 255)
purple = pygame.Color(185, 0, 255)
brown = pygame.Color(125, 90, 25)
orange = pygame.Color(255, 139, 0)

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
        self.direction = random.choice([up, down, left, right]) # Random start direction
        self.double = False

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
        #if double power is active, grow twice
        if self.double:
            self.pos.append(self.pos[-1])

    def draw(self):
        for segment in self.pos:
            pygame.draw.rect(screen, self.color, (segment[0] * cellSize, segment[1] * cellSize, cellSize, cellSize))

class AISnake(Snake):
    def __init__(self, color, food, player):
        super().__init__(color, {})
        self.food = food
        self.player = player
        self.canmove = True

    def heuristic(self, pos):
        food = abs(pos[0] - self.food.pos[0]) + abs(pos[1] - self.food.pos[1])  # Manhattan distance to food
        player = min(abs(pos[0] - p[0]) + abs(pos[1] - p[1]) for p in self.player.pos)  # Manhattan distance to player
        penalty = max(0, 15 - player) # Penalty to avoid player
        return food + penalty

    def aStar(self, start, goal):
        openSet = set()
        closedSet = set()
        gScore = {start: 0} 
        fScore = {start: self.heuristic(start)} 
        pathTo = {} 

        openSet.add(start)
        while openSet:
            current = min(openSet, key=lambda x: fScore[x]) # Node with lowest fScore
            if current == goal: # Goal reached
                path = []
                while current in pathTo:    # Reconstruct path
                    current = pathTo[current]
                    path.insert(0, current)
                return path
            
            openSet.remove(current) # Remove current from openSet
            closedSet.add(current)  # Add current to closedSet

            for direction in [up, down, left, right]:
                neighbor = ((current[0] + direction[0]) % gridW, (current[1] + direction[1]) % gridH)   
                if neighbor in closedSet or neighbor in self.pos[1:]:   # Skip if neighbor is in closedSet or in itself
                    continue

                tempgScore = gScore[current] + 1
                if neighbor in gScore and tempgScore >= gScore[neighbor]:   # Skip if neighbor is already evaluated and has higher gScore
                    continue

                pathTo[neighbor] = current  
                gScore[neighbor] = tempgScore
                fScore[neighbor] = tempgScore + self.heuristic(neighbor)    

                openSet.add(neighbor)   # Add neighbor to openSet

    def move(self):
        path = self.aStar(self.pos[0], self.food.pos)
        if path and len(path) > 1:
            step =  path[1]
            self.direction = (step[0] - self.pos[0][0], step[1] - self.pos[0][1])   
        
        super().move()  

class Food:
    def __init__(self):
        self.pos = self.randPos()

    def randPos(self):
        return (random.randint(1, gridW - 5), random.randint(1, gridH - 5))

    def draw(self):
        pygame.draw.rect(screen, white, (self.pos[0] * cellSize, self.pos[1] * cellSize, cellSize, cellSize))

class Freeze_Power:
    def __init__(self):
        self.pos = self.randPos()

    def randPos(self):
        return (random.randint(1, gridW - 5), random.randint(1, gridH - 5))

    def draw(self):
        pygame.draw.rect(screen, blue, (self.pos[0] * cellSize, self.pos[1] * cellSize, cellSize, cellSize))

class Double_Power:
    def __init__(self):
        self.pos = self.randPos()

    def randPos(self):
        return (random.randint(1, gridW - 5), random.randint(1, gridH - 5))

    def draw(self):
        pygame.draw.rect(screen, yellow, (self.pos[0] * cellSize, self.pos[1] * cellSize, cellSize, cellSize))

class Tele_Power:
    def __init__(self):
        self.pos = self.randPos()

    def randPos(self):
        return (random.randint(1, gridW - 5), random.randint(1, gridH - 5))

    def draw(self):
        pygame.draw.rect(screen, orange, (self.pos[0] * cellSize, self.pos[1] * cellSize, cellSize, cellSize))

class Wall:
    def __init__(self):
        self.color = brown
        self.wallUp = True

    def draw(self):
        pygame.draw.rect(screen, self.color, (0, 0, width, cellSize))
        pygame.draw.rect(screen, self.color, (0, 575, width, cellSize))
        pygame.draw.rect(screen, self.color, (0, 0, cellSize, height))
        pygame.draw.rect(screen, self.color, (775, 0, cellSize, height))


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

def display_game_won():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('You Win!', True, white)
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
    fr_power = Freeze_Power()
    dbl_power = Double_Power()
    tele_power = Tele_Power()
    wall = Wall()
    player_controls = {
        pygame.K_UP: up,
        pygame.K_DOWN: down,
        pygame.K_LEFT: left,
        pygame.K_RIGHT: right
    }
    player_snake = Snake(red, player_controls)
    ai_snake = AISnake(green, food, player_snake)
    UNFREEZE = pygame.USEREVENT + 1
    DOUBLE = pygame.USEREVENT + 2
    TELEPORT = pygame.USEREVENT + 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                player_snake.change_direction(event.key)
            elif event.type == UNFREEZE:
                ai_snake.canmove = True
            elif event.type == DOUBLE:
                player_snake.double = False
                player_snake.color = red
            elif event.type == TELEPORT:
                wall.wallUp = True
                wall.color = brown

        player_snake.move()

        # check if player hits a wall
        if wall.wallUp:
            if player_snake.pos[0][1] < 1 or player_snake.pos[0][1] > 22 or player_snake.pos[0][0] < 1 or player_snake.pos[0][0] > 30:
                display_game_over()

        # check for if power is active
        if ai_snake.canmove:
            ai_snake.move()
       # Freeze time Powerup
        if player_snake.pos[0] == fr_power.pos:
            ai_snake.canmove = False
            fr_power = Freeze_Power()
            pygame.time.set_timer(UNFREEZE, 2000, loops=0)
        #Double growth powerup
        if player_snake.pos[0] == dbl_power.pos:
            player_snake.color = purple
            player_snake.double = True
            dbl_power = Double_Power()
            pygame.time.set_timer(DOUBLE, 3500, loops=0)
        #Teleport powerup
        if player_snake.pos[0] == tele_power.pos:
            wall.color = orange
            wall.wallUp = False
            tele_power = Tele_Power()
            pygame.time.set_timer(TELEPORT, 5000, loops=0)

        if player_snake.pos[0] == food.pos:
            player_snake.grow()
            food = Food()
            ai_snake.food = food
        elif ai_snake.pos[0] == food.pos:
            ai_snake.grow()
            food = Food()
            ai_snake.food = food

        for segment in ai_snake.pos:
            if player_snake.pos[0]  == (segment[0], segment[1]):
                display_game_over()

        for segment in player_snake.pos:
            if ai_snake.pos[0] == (segment[0], segment[1]):
                display_game_won()

        for segment in player_snake.pos[2:]:
            if player_snake.pos[0] == (segment[0], segment[1]):
                display_game_over()

        screen.fill(black)
        player_snake.draw()
        ai_snake.draw()
        food.draw()
        fr_power.draw()
        dbl_power.draw()
        tele_power.draw()
        wall.draw()
        my_font = pygame.font.SysFont('times new roman', 20)
        game_over_surface = my_font.render(f'player length: {len(player_snake.pos)}   AI length: {len(ai_snake.pos)}', True, white)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (140, 1)
        screen.blit(game_over_surface, game_over_rect)

        pygame.display.flip()
        clock.tick(15)

if __name__ == "__main__":
    main()
