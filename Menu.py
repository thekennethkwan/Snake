# Menu.py
import pygame

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(100, 100, 100)

def show_menu(screen, clock):
    pygame.font.init()
    width, height = 800, 600
    menu_font = pygame.font.SysFont('times new roman', 40)
    title_font = pygame.font.SysFont('times new roman', 60)
    options = ["Single Player vs AI", "Two Players", "Quit"]
    selected = 0

    while True:
        screen.fill(black)
        title = title_font.render('Snake Game Menu', True, white)
        title_rect = title.get_rect(center=(width // 2, height // 4))
        screen.blit(title, title_rect)

        for index, option in enumerate(options):
            color = white if index == selected else grey
            menu_item = menu_font.render(option, True, color)
            item_rect = menu_item.get_rect(center=(width // 2, height // 2 + 50 * index))
            screen.blit(menu_item, item_rect)

        pygame.display.flip()
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]