# Snake.py
import pygame
import heapq
import time
import random

from Menu import show_menu  # game menu

# Screen configuration
# Screen configuration
width, height = 800, 600
cellSize = 25
gridW = width // cellSize  # 32
gridH = height // cellSize  # 24
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
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
        self.ogColor = color
        self.color = color
        self.controls = controls
        self.controls = controls
        self.pos = [self.randPos()]
        self.direction = random.choice([up, down, left, right])
        self.double = False
        self.canmove = True

    def randPos(self):
        return (random.randint(5, gridW - 5), random.randint(5, gridH - 5))

        return (random.randint(5, gridW - 5), random.randint(5, gridH - 5))

    def move(self):
        head = self.pos[0]
        new_head = ((head[0] + self.direction[0]) % gridW, (head[1] + self.direction[1]) % gridH)
        new_head = ((head[0] + self.direction[0]) % gridW, (head[1] + self.direction[1]) % gridH)
        self.pos.insert(0, new_head)
        if len(self.pos) > 1:
            self.pos.pop()

    def change_direction(self, key):
        if key in self.controls:
            new_dir = self.controls[key]
            if len(self.pos) > 1 and new_dir == (-self.direction[0], -self.direction[1]):
                print("Reverse direction attempt blocked.")
            else:
                self.direction = new_dir

    def change_direction(self, key):
        if key in self.controls:
            new_dir = self.controls[key]
            if len(self.pos) > 1 and new_dir == (-self.direction[0], -self.direction[1]):
                print("Reverse direction attempt blocked.")
            else:
                self.direction = new_dir

    def grow(self):
        self.pos.append(self.pos[-1])
        if self.double:
            self.pos.append(self.pos[-1])

    def draw(self):
        for segment in self.pos:
            pygame.draw.rect(screen, self.color, (segment[0] * cellSize, segment[1] * cellSize, cellSize, cellSize))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in self.controls:
            self.change_direction(event.key)


class AISnake(Snake):
    def __init__(self, color, food, player):
        super().__init__(color, {})
        self.food = food
        self.playerSnake = player
        self.canmove = True

    def heuristic(self, pos):
        food = abs(pos[0] - self.food.pos[0]) + abs(pos[1] - self.food.pos[1])
        player = min(abs(pos[0] - p[0]) + abs(pos[1] - p[1]) for p in self.playerSnake.pos)
        penalty = max(0, 10 - player)
        return food + penalty

    def aStar(self, start, goal):
        openSet = set()
        closedSet = set()
        gScore = {start: 0}
        fScore = {start: self.heuristic(start)}
        pathTo = {}

        openSet.add(start)
        while openSet:
            current = min(openSet, key=lambda x: fScore[x])
            if current == goal:
                path = []
                while current in pathTo:
                    current = pathTo[current]
                    path.insert(0, current)
                return path

            openSet.remove(current)
            closedSet.add(current)

            for direction in [up, down, left, right]:
                neighbor = ((current[0] + direction[0]) % gridW, (current[1] + direction[1]) % gridH)
                if neighbor in closedSet or neighbor in self.pos[1:]:
                    continue

                tempgScore = gScore[current] + 1
                if neighbor in gScore and tempgScore >= gScore[neighbor]:
                    continue

                pathTo[neighbor] = current
                gScore[neighbor] = tempgScore
                fScore[neighbor] = tempgScore + self.heuristic(neighbor)

                openSet.add(neighbor)

    def move(self):
        path = self.aStar(self.pos[0], self.food.pos)
        if path and len(path) > 1:
            step = path[1]
            self.direction = (step[0] - self.pos[0][0], step[1] - self.pos[0][1])

        super().move()


class Food:
    def __init__(self, snakes):
        self.snakes = snakes
        self.pos = self.randPos()

    def randPos(self):
        while True:
            newPos = (random.randint(1, gridW - 5), random.randint(1, gridH - 5))
            # Make sure food does not spawn on any snake
            if not any(newPos in snake.pos for snake in self.snakes):
                return newPos

    def draw(self):
        pygame.draw.rect(screen, white, (self.pos[0] * cellSize, self.pos[1] * cellSize, cellSize, cellSize))


class Freeze_Power:
    def __init__(self, snakes):
        self.snakes = snakes
        self.pos = self.randPos()

    def randPos(self):
        while True:
            newPos = (random.randint(1, gridW - 5), random.randint(1, gridH - 5))
            # Make sure food does not spawn on any snake
            if not any(newPos in snake.pos for snake in self.snakes):
                return newPos

    def draw(self):
        pygame.draw.rect(screen, blue, (self.pos[0] * cellSize, self.pos[1] * cellSize, cellSize, cellSize))


class Double_Power:
    def __init__(self, snakes):
        self.snakes = snakes
        self.pos = self.randPos()

    def randPos(self):
        while True:
            newPos = (random.randint(1, gridW - 5), random.randint(1, gridH - 5))
            # Make sure food does not spawn on any snake
            if not any(newPos in snake.pos for snake in self.snakes):
                return newPos

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


def display_game_over(screen):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width / 2, height / 4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)  # Pause to show the message
    pygame.quit()
    exit()

def display_game_won(screen):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('You Win!', True, white)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width / 2, height / 4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)  # Pause to show the message
    pygame.quit()
    exit()


def game_over_condition(player_snake, wall):
    # Check if the snake's head collides with any part of its body
    head = player_snake.pos[0]
    if head in player_snake.pos[1:]:
        return True

    # Check if the snake's head hits the boundary or wall
    if head[0] < 1 or head[0] > gridW - 2 or head[1] < 1 or head[1] > gridH - 2:
        return True
    return False


def game_won_condition(player_snake, winning_score):
    # Assuming each food increases the snake's length by 1 and winning score is based on length
    if len(player_snake.pos) >= winning_score:
        return True
    return False


def gameAI():
    clock = pygame.time.Clock()
    tele_power = Tele_Power()
    wall = Wall()
    player_controls = {
        pygame.K_UP: up,
        pygame.K_DOWN: down,
        pygame.K_LEFT: left,
        pygame.K_RIGHT: right
    }
    player_snake = Snake(red, player_controls)
    ai_snake = AISnake(green, None, player_snake)
    snakes = [player_snake, ai_snake]

    fr_power = Freeze_Power(snakes)
    dbl_power = Double_Power(snakes)
    food = Food(snakes)

    for snake in snakes:
        if isinstance(snake, AISnake):
            snake.food = food

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
            if player_snake.pos[0][1] < 1 or player_snake.pos[0][1] > 22 or player_snake.pos[0][0] < 1 or \
                    player_snake.pos[0][0] > 30:
                display_game_over(screen)

        # check for if power is active
        if ai_snake.canmove:
            ai_snake.move()
        # Freeze time Powerup
        if player_snake.pos[0] == fr_power.pos:
            ai_snake.canmove = False
            fr_power = Freeze_Power(snakes)
            pygame.time.set_timer(UNFREEZE, 2000, loops=0)
        # Double growth powerup
        if player_snake.pos[0] == dbl_power.pos:
            player_snake.color = purple
            player_snake.double = True
            dbl_power = Double_Power(snakes)
            pygame.time.set_timer(DOUBLE, 3500, loops=0)
        # Teleport powerup
        if player_snake.pos[0] == tele_power.pos:
            wall.color = orange
            wall.wallUp = False
            tele_power = Tele_Power()
            pygame.time.set_timer(TELEPORT, 5000, loops=0)

        if player_snake.pos[0] == food.pos:
            player_snake.grow()
            food = Food(snakes)
            ai_snake.food = food
        elif ai_snake.pos[0] == food.pos:
            ai_snake.grow()
            food = Food(snakes)
            ai_snake.food = food

        for segment in ai_snake.pos:
            if player_snake.pos[0] == (segment[0], segment[1]):
                display_game_over(screen)

        for segment in player_snake.pos:
            if ai_snake.pos[0] == (segment[0], segment[1]):
                display_game_won(screen)

        for segment in player_snake.pos[2:]:
            if player_snake.pos[0] == (segment[0], segment[1]):
                display_game_over(screen)

        screen.fill(black)
        player_snake.draw()
        ai_snake.draw()
        food.draw()
        fr_power.draw()
        dbl_power.draw()
        tele_power.draw()
        wall.draw()
        my_font = pygame.font.SysFont('times new roman', 20)
        game_over_surface = my_font.render(f'player length: {len(player_snake.pos)}   AI length: {len(ai_snake.pos)}',
                                           True, white)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (140, 1)
        screen.blit(game_over_surface, game_over_rect)

        pygame.display.flip()
        clock.tick(15)


def gameTwoPlayers():
    clock = pygame.time.Clock()
    tele_power = Tele_Power()
    wall = Wall()

    player1_controls = {pygame.K_w: up, pygame.K_s: down, pygame.K_a: left, pygame.K_d: right}
    player2_controls = {pygame.K_UP: up, pygame.K_DOWN: down, pygame.K_LEFT: left, pygame.K_RIGHT: right}

    player_snake_1 = Snake(red, player1_controls)
    player_snake_2 = Snake(blue, player2_controls)
    snakes = [player_snake_1, player_snake_2]

    fr_power = Freeze_Power(snakes)
    dbl_power = Double_Power(snakes)
    food = Food(snakes)

    UNFREEZE = pygame.USEREVENT + 1
    DOUBLE = pygame.USEREVENT + 2
    TELEPORT = pygame.USEREVENT + 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == UNFREEZE:
                for snake in snakes:
                    if not snake.canmove:
                        snake.canmove = True
            elif event.type == DOUBLE:
                for snake in snakes:
                    if snake.double:
                        snake.double = False
                        snake.color = snake.ogColor
            elif event.type == TELEPORT:
                wall.wallUp = True
                wall.color = brown
            for snake in snakes:
                if event.type == pygame.KEYDOWN:
                    snake.change_direction(event.key)

        for snake in snakes:
            if snake.canmove:  # Check if snake frozen
                snake.move()

            # check if player hits a wall
            if wall.wallUp:
                if snake.pos[0][1] < 1 or snake.pos[0][1] > 22 or snake.pos[0][0] < 1 or snake.pos[0][0] > 30:
                    display_game_over(screen)

            other_snakes = [s for s in snakes if s != snake]
            # Freeze time Powerup
            if snake.pos[0] == fr_power.pos:
                for other_snake in other_snakes:
                    other_snake.canmove = False
                fr_power = Freeze_Power(snakes)
                pygame.time.set_timer(UNFREEZE, 2000, loops=0)
            # Double growth powerup
            if snake.pos[0] == dbl_power.pos:
                snake.color = purple
                snake.double = True
                dbl_power = Double_Power(snakes)
                pygame.time.set_timer(DOUBLE, 3500, loops=0)
            # Teleport powerup
            if snake.pos[0] == tele_power.pos:
                wall.color = orange
                wall.wallUp = False
                tele_power = Tele_Power()
                pygame.time.set_timer(TELEPORT, 5000, loops=0)

            if snake.pos[0] == food.pos:
                snake.grow()
                food = Food(snakes)

            for snake in other_snakes:
                for segment in snake.pos[2:]:
                    if snake.pos[0] == (segment[0], segment[1]):
                        display_game_over(screen)

        screen.fill(black)
        for snake in snakes:
            snake.draw()
        food.draw()
        fr_power.draw()
        dbl_power.draw()
        tele_power.draw()
        wall.draw()
        my_font = pygame.font.SysFont('times new roman', 20)
        game_over_surface = my_font.render(
            f' Player 1 length: {len(player_snake_1.pos)}   Player 2 length: {len(player_snake_2.pos)}', True, white)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (140, 1)
        screen.blit(game_over_surface, game_over_rect)

        pygame.display.flip()
        clock.tick(15)


def main():
    pygame.init()
    clock = pygame.time.Clock()

    mode = show_menu(screen, clock)  # Get the selected game mode from the menu
    if mode == "Quit":
        pygame.quit()
        return

    # Call the appropriate function based on the selected game mode
    if mode == "Single Player vs AI":
        gameAI()
    elif mode == "Two Players":
        gameTwoPlayers()


if __name__ == "__main__":
    main()  # Start the main game loop
