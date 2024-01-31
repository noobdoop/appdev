import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('static/images/snakeGame_images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('static/images/snakeGame_images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('static/images/snakeGame_images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('static/images/snakeGame_images/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('static/images/snakeGame_images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('static/images/snakeGame_images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('static/images/snakeGame_images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('static/images/snakeGame_images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('static/images/snakeGame_images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('static/images/snakeGame_images/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('static/images/snakeGame_images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('static/images/snakeGame_images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('static/images/snakeGame_images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('static/images/snakeGame_images/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(egg, fruit_rect)

    # pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_over = False

    def update(self):
        if self.snake.direction != Vector2(0, 0):  # Only move if there is a direction set by the user
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        head = self.snake.body[0]
        if not 0 <= head.x < cell_number or not 0 <= head.y < cell_number:
            self.game_over = True
            self.show_game_over_screen()

        for block in self.snake.body[1:]:
            if block == head:
                self.game_over = True
                self.show_game_over_screen()

    # def game_over(self):
    #     self.snake.reset()
    def show_game_over_screen(self):
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Retry on Enter key
                        self.reset_game()

            # Draw game over screen elements
            screen.fill((175, 215, 70))
            game_over_text = game_font.render("Game Over", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 - 40))
            screen.blit(game_over_text, game_over_rect)

            score_text = f"Score: {len(self.snake.body) - 3}"
            score_surface = game_font.render(score_text, True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2))
            screen.blit(score_surface, score_rect)

            retry_text = game_font.render("Press Enter to Retry", True, (255, 255, 255))
            retry_rect = retry_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 + 40))
            screen.blit(retry_text, retry_rect)

            pygame.display.update()
            clock.tick(60)

    def reset_game(self):
        self.snake.reset()
        self.snake.direction = Vector2(0, 0)  # Reset the snake direction
        self.fruit.randomize()
        self.game_over = False


    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        egg_rect = egg.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(egg_rect.left, egg_rect.top, egg_rect.width + score_rect.width + 6,
                              egg_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(egg, egg_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def draw_score_chart(self):
        # Snegg title
        title_font = pygame.font.Font('static/PoetsenOne-Regular.ttf', 30)
        title_text = title_font.render("Snegg", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(cell_number * cell_size // 2, 20))
        screen.blit(title_text, title_rect)

        # Score display
        score_text = f"Score: {len(self.snake.body) - 3}"
        score_font = pygame.font.Font('static/PoetsenOne-Regular.ttf', 25)
        score_surface = score_font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(cell_number * cell_size // 2, 60))
        screen.blit(score_surface, score_rect)



pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
egg = pygame.image.load('static/images/snakeGame_images/egg.png').convert_alpha()
game_font = pygame.font.Font('static/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE and not main_game.game_over:
            main_game.update()
        if event.type == pygame.KEYDOWN and not main_game.game_over:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)