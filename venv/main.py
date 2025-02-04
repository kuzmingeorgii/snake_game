import pygame
import pygame_gui
import sys
import random
import time


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
BLOCK_SIZE = 20
FPS = 60
SCORE = 0
BLOCKED_CELLS = []
PICTURE_DIR = "data/"
MAPS_DIR = "game_maps/"
SOUND_DIR = "sound_effects/"
FOOD_PIC = "food.png"
FON_PIC = "start_fon.jpg"
BORDER_PIC = "border.png"
CRASHED_PIC = "crashed.png"
CLASSIC_MAP = "classic.txt"
EAT_SOUND = "eat_sound.wav"
CRASH_SOUND = "crash_sound.wav"

game_sound = True
classic_type = True
labyrinth_type = None

all_sprites = pygame.sprite.Group()
borders_sprite = pygame.sprite.Group()
snake_spite = pygame.sprite.Group()
food_spite = pygame.sprite.Group()
crash_sprite = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(pic):
    return pygame.image.load(PICTURE_DIR + pic).convert_alpha()


def generate_level(level):
    global BLOCKED_CELLS
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "#":
                Border(x, y)
                blocked_x = 20 + x * BLOCK_SIZE
                blocked_y = 40 + y * BLOCK_SIZE
                BLOCKED_CELLS.append((blocked_x, blocked_y))


def load_level(filename):
    filename = MAPS_DIR + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def type_of_game_screen(screen):
    global classic_type, labyrinth_type
    black_color = (0, 0, 0)

    typy_of_game_manager = pygame_gui.UIManager(WINDOW_SIZE)

    fon = pygame.transform.scale(load_image(FON_PIC), WINDOW_SIZE)

    font = pygame.font.Font(None, 50)
    type_of_game_string = font.render("Тип игры", True, black_color)
    type_of_game_string_rect = type_of_game_string.get_rect()
    type_of_game_string_x = (WINDOW_WIDTH - type_of_game_string_rect.width) // 2
    type_of_game_string_y = 50

    labyrinth_btn_group = list()

    button_width = 220
    button_height = 50
    button_x = (WINDOW_WIDTH - button_width) // 2

    classic_type_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_x, 100), (button_width, button_height)),
        text="Классический",
        manager=typy_of_game_manager
    )
    if classic_type:
        classic_type_btn.select()

    labyrinth_type_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_x, 160), (button_width, button_height)),
        text="Лабиринт",
        manager=typy_of_game_manager
    )

    font_2 = pygame.font.Font(None, 25)
    select_type_string = font_2.render("Выберите тип лабиринта:", True, black_color)
    select_type_string_rect = select_type_string.get_rect()
    select_type_string_x = (WINDOW_WIDTH - select_type_string_rect.width) // 2
    select_type_string_y = 220

    tunnel_labyrinth_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_x, 240), (button_width, button_height)),
        text="Туннель",
        manager=typy_of_game_manager
    )
    if labyrinth_type == "Tunnel":
        tunnel_labyrinth_btn.select()
    labyrinth_btn_group.append(tunnel_labyrinth_btn)

    mill_labyrinth_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_x, 300), (button_width, button_height)),
        text="Мельница",
        manager=typy_of_game_manager
    )
    if labyrinth_type == "Mill":
        mill_labyrinth_btn.select()
    labyrinth_btn_group.append(mill_labyrinth_btn)

    back_btn_x = 350
    back_btn_y = 400
    back_btn_width = 100
    back_btn_height = 35

    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((back_btn_x, back_btn_y), (back_btn_width, back_btn_height)),
        text="Назад",
        manager=typy_of_game_manager
    )

    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == classic_type_btn:
                        classic_type = True
                        labyrinth_type = None
                        classic_type_btn.select()
                        for btn in labyrinth_btn_group:
                            btn.unselect()
                    if event.ui_element == labyrinth_type_btn:
                        classic_type = False
                        if labyrinth_type is None:
                            labyrinth_type = "Tunnel"
                            tunnel_labyrinth_btn.select()
                            classic_type_btn.unselect()
                    if event.ui_element == tunnel_labyrinth_btn:
                        classic_type = False
                        labyrinth_type = "Tunnel"
                        for btn in labyrinth_btn_group:
                            btn.unselect()
                        tunnel_labyrinth_btn.select()
                        classic_type_btn.unselect()
                    if event.ui_element == mill_labyrinth_btn:
                        classic_type = False
                        labyrinth_type = "Mill"
                        for btn in labyrinth_btn_group:
                            btn.unselect()
                        mill_labyrinth_btn.select()
                        classic_type_btn.unselect()
                    if event.ui_element == back_btn:
                        return
            typy_of_game_manager.process_events(event)
        screen.blit(fon, (0, 0))
        if any([btn.is_selected for btn in labyrinth_btn_group]):
            for btn in labyrinth_btn_group:
                btn.show()
            screen.blit(select_type_string, (select_type_string_x, select_type_string_y))
        else:
            for btn in labyrinth_btn_group:
                btn.hide()
        screen.blit(type_of_game_string, (type_of_game_string_x, type_of_game_string_y))
        typy_of_game_manager.update(time_delta)
        typy_of_game_manager.draw_ui(screen)
        pygame.display.flip()


def options_screen(screen):
    global game_sound

    black_color = (0, 0, 0)

    options_manager = pygame_gui.UIManager(WINDOW_SIZE)

    fon = pygame.transform.scale(load_image(FON_PIC), WINDOW_SIZE)

    font = pygame.font.Font(None, 50)
    option_string = font.render("Опции", True, black_color)
    option_string_rect = option_string.get_rect()
    option_string_x = (WINDOW_WIDTH - option_string_rect.width) // 2
    option_string_y = 50

    sound_btn_x = 125
    sound_btn_y = 100
    sound_btn_width = 150
    sound_btn_height = 40

    game_sound_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((sound_btn_x, sound_btn_y), (sound_btn_width, sound_btn_height)),
        text="Звук игры",
        manager=options_manager
    )

    back_btn_x = 350
    back_btn_y = 400
    back_btn_width = 100
    back_btn_height = 35

    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((back_btn_x, back_btn_y), (back_btn_width, back_btn_height)),
        text="Назад",
        manager=options_manager
    )

    def get_sound_status_text():
        return font.render("Вкл." if game_sound else "Выкл.", True, black_color)

    sound_status_string = get_sound_status_text()
    sound_status_x = 290
    sound_status_y = 105

    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == game_sound_btn:
                        game_sound = not game_sound
                        sound_status_string = font.render("Вкл." if game_sound else "Выкл.", True, black_color)
                    if event.ui_element == back_btn:
                        return
            options_manager.process_events(event)
        screen.blit(fon, (0, 0))
        screen.blit(option_string, (option_string_x, option_string_y))
        screen.blit(sound_status_string, (sound_status_x, sound_status_y))
        options_manager.update(time_delta)
        options_manager.draw_ui(screen)
        pygame.display.flip()


def start_screen(screen):
    fon = pygame.transform.scale(load_image(FON_PIC), WINDOW_SIZE)

    manager = pygame_gui.UIManager(WINDOW_SIZE)

    button_width = 220
    button_height = 50
    button_x = (WINDOW_WIDTH - button_width) // 2

    new_game_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_x, 55), (button_width, button_height)),
        text="Новая игра",
        manager=manager
    )

    type_of_game = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_x, 135), (button_width, button_height)),
        text="Тип игры",
        manager=manager
    )

    options_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_x, 250), (button_width, button_height)),
        text="Опции",
        manager=manager
    )

    clock = pygame.time.Clock()
    while True:
        delta_time = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == new_game_btn:
                        return
                    if event.ui_element == type_of_game:
                        type_of_game_screen(screen)
                    if event.ui_element == options_btn:
                        options_screen(screen)
            manager.process_events(event)
        screen.blit(fon, (0, 0))
        manager.update(delta_time)
        manager.draw_ui(screen)
        pygame.display.flip()


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, borders_sprite)
        self.x = 20 + x * BLOCK_SIZE
        self.y = 40 + y * BLOCK_SIZE
        self.image = pygame.transform.scale(load_image(BORDER_PIC), (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y, block_size):
        super().__init__(all_sprites, snake_spite)
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 0
        self.block_size = block_size
        self.alive = True
        self.body = [(self.x, self.y)]
        self.length = 1
        self.image = pygame.Surface((block_size, block_size))
        self.image.fill((0, 255, 0))  # Зеленый цвет для тела змейки
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.eat_sound = None
        self.crash_sound = None

    def move(self):
        if not self.alive:
            return
        self.x += self.dx * self.block_size
        self.y += self.dy * self.block_size
        self.body.append((self.x, self.y))
        if len(self.body) > self.length:
            self.body.pop(0)
        self.rect.topleft = (self.x, self.y)
        if pygame.sprite.spritecollideany(self, borders_sprite):
            self.alive = False
            Crashed(self.x, self.y)
            if self.crash_sound:
                self.crash_sound.play()

        if pygame.sprite.spritecollideany(self, food_spite):
            global SCORE
            if self.eat_sound:
                self.eat_sound.play()
            SCORE += 1
            self.length += 1
            food_spite.empty()
            new_food = Food()
            while (new_food.x, new_food.y) in self.body:
                food_spite.empty()
                new_food = Food()

        if (self.x, self.y) in self.body[:-1]:
            self.alive = False
            Crashed(self.x, self.y)
            if self.crash_sound:
                self.crash_sound.play()

    def draw(self, screen):
        for block in self.body[:-1]:
            pygame.draw.rect(screen, (0, 255, 0), (block[0], block[1], self.block_size, self.block_size))
            pygame.draw.rect(screen, (255, 255, 255), (block[0], block[1], self.block_size, self.block_size), 1)

        head_x, head_y = self.body[-1]
        pygame.draw.rect(screen, (0, 0, 255), (head_x, head_y, self.block_size, self.block_size))
        pygame.draw.rect(screen, (255, 255, 255), (head_x, head_y, self.block_size, self.block_size), 1)

    def set_sounds(self, *sounds):
        self.eat_sound = sounds[0]
        self.crash_sound = sounds[1]


class Crashed(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, crash_sprite)
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(load_image(CRASHED_PIC), (BLOCK_SIZE + 15, BLOCK_SIZE + 15))
        self.rect = self.image.get_rect(topleft=(self.x - 7.5, self.y - 7.5))


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, food_spite)
        self.image = pygame.transform.scale(load_image(FOOD_PIC), (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect()

        max_attempts = 100
        for _ in range(max_attempts):
            self.x = random.randrange(40, WINDOW_WIDTH - 40, BLOCK_SIZE)
            self.y = random.randrange(60, WINDOW_HEIGHT - 40, BLOCK_SIZE)
            self.rect.topleft = (self.x, self.y)
            if not pygame.sprite.spritecollideany(self, borders_sprite):
                break
        else:
            raise ValueError("Не удалось найти подходящее место для еды.")


class ScoreString:
    def __init__(self):
        self.score = 0
        self.color = (255, 0, 0)
        self.font = pygame.font.Font(None, 25)
        self.string = self.font.render(f"SCORE: {self.score}", True, self.color)
        self.rect = self.string.get_rect()
        self.x = 30
        self.y = 10

    def update(self, score):
        self.score = score
        self.string = self.font.render(f"SCORE: {self.score}", True, self.color)
        self.rect = self.string.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.string, (self.x, self.y))


def lose_screen(screen):
    global SCORE, BLOCKED_CELLS

    red_color = (255, 0, 0)

    font = pygame.font.Font(None, 70)

    end_string = font.render("Ваш счет", True, red_color)
    end_string_rect = end_string.get_rect()
    end_string_x = (WINDOW_WIDTH - end_string_rect.width) // 2
    end_string_y = 130

    end_string_2 = font.render(f"{SCORE}", True, red_color)
    end_string_rect_2 = end_string_2.get_rect()
    end_string_x_2 = (WINDOW_WIDTH - end_string_rect_2.width) // 2
    end_string_y_2 = 200

    font_2 = pygame.font.Font(None, 35)

    end_string_3 = font_2.render("Нажмите любую клавишу", True, red_color)
    end_string_rect_3 = end_string_3.get_rect()
    end_string_x_3 = (WINDOW_WIDTH - end_string_rect_3.width) // 2
    end_string_y_3 = 270

    end_string_4 = font_2.render("для выхода в меню", True, red_color)
    end_string_rect_4 = end_string_4.get_rect()
    end_string_x_4 = (WINDOW_WIDTH - end_string_rect_4.width) // 2
    end_string_y_4 = 300

    screen.blit(end_string, (end_string_x, end_string_y))
    screen.blit(end_string_2, (end_string_x_2, end_string_y_2))
    screen.blit(end_string_3, (end_string_x_3, end_string_y_3))
    screen.blit(end_string_4, (end_string_x_4, end_string_y_4))

    pygame.display.flip()
    break_flag = False
    time.sleep(1.5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                break_flag = True
        if break_flag:
            break
    all_sprites.empty()
    borders_sprite.empty()
    snake_spite.empty()
    food_spite.empty()
    crash_sprite.empty()
    SCORE = 0
    BLOCKED_CELLS = []
    return main()


def win_screen(screen):
    global SCORE, BLOCKED_CELLS

    red_color = (255, 0, 0)

    font = pygame.font.Font(None, 70)

    end_string = font.render("Вы выиграли", True, red_color)
    end_string_rect = end_string.get_rect()
    end_string_x = (WINDOW_WIDTH - end_string_rect.width) // 2
    end_string_y = 130

    end_string_2 = font.render(f"Ваш счет: {SCORE}", True, red_color)
    end_string_rect_2 = end_string_2.get_rect()
    end_string_x_2 = (WINDOW_WIDTH - end_string_rect_2.width) // 2
    end_string_y_2 = 200

    font_2 = pygame.font.Font(None, 35)

    end_string_3 = font_2.render("Нажмите любую клавишу", True, red_color)
    end_string_rect_3 = end_string_3.get_rect()
    end_string_x_3 = (WINDOW_WIDTH - end_string_rect_3.width) // 2
    end_string_y_3 = 270

    end_string_4 = font_2.render("для выхода в меню", True, red_color)
    end_string_rect_4 = end_string_4.get_rect()
    end_string_x_4 = (WINDOW_WIDTH - end_string_rect_4.width) // 2
    end_string_y_4 = 300

    screen.blit(end_string, (end_string_x, end_string_y))
    screen.blit(end_string_2, (end_string_x_2, end_string_y_2))
    screen.blit(end_string_3, (end_string_x_3, end_string_y_3))
    screen.blit(end_string_4, (end_string_x_4, end_string_y_4))

    pygame.display.flip()
    break_flag = False
    time.sleep(1.5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                break_flag = True
        if break_flag:
            break
    all_sprites.empty()
    borders_sprite.empty()
    snake_spite.empty()
    food_spite.empty()
    crash_sprite.empty()
    SCORE = 0
    BLOCKED_CELLS = []
    return main()


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SRCALPHA)
    pygame.display.set_caption("Змейка")

    start_screen(screen)

    black_color = (0, 0, 0)
    red_color = (255, 0, 0)

    if classic_type:
        fon = pygame.transform.scale(load_image(FON_PIC), WINDOW_SIZE)
        font = pygame.font.Font(None, 50)
        wait_string = font.render("Загружаем игру...", True, black_color)
        wait_string_rect = wait_string.get_rect()
        wait_string_x = (WINDOW_WIDTH - wait_string_rect.width) // 2
        wait_string_y = 90
        screen.blit(fon, (0, 0))
        screen.blit(wait_string, (wait_string_x, wait_string_y))
        pygame.display.flip()

        level = load_level("classic.txt")
        generate_level(level)

    if labyrinth_type:
        fon = pygame.transform.scale(load_image(FON_PIC), WINDOW_SIZE)
        font = pygame.font.Font(None, 50)
        wait_string = font.render("Загружаем игру...", True, black_color)
        wait_string_rect = wait_string.get_rect()
        wait_string_x = (WINDOW_WIDTH - wait_string_rect.width) // 2
        wait_string_y = 90
        screen.blit(fon, (0, 0))
        screen.blit(wait_string, (wait_string_x, wait_string_y))
        pygame.display.flip()

        level = load_level(labyrinth_type + ".txt")
        generate_level(level)

    if labyrinth_type:
        fon = pygame.transform.scale(load_image(FON_PIC), WINDOW_SIZE)
        font = pygame.font.Font(None, 50)
        wait_string = font.render("Загружаем игру...", True, black_color)
        wait_string_rect = wait_string.get_rect()
        wait_string_x = (WINDOW_WIDTH - wait_string_rect.width) // 2
        wait_string_y = 90
        screen.blit(fon, (0, 0))
        screen.blit(wait_string, (wait_string_x, wait_string_y))
        pygame.display.flip()

        level = load_level(labyrinth_type + ".txt")
        generate_level(level)

    snake = Snake(100, 100, BLOCK_SIZE)
    food = Food()
    score_string = ScoreString()

    if game_sound:
        pygame.mixer.init()
        eat_sound = pygame.mixer.Sound(SOUND_DIR + EAT_SOUND)
        crash_sound = pygame.mixer.Sound(SOUND_DIR + CRASH_SOUND)
        snake.set_sounds(eat_sound, crash_sound)

    direction = {
        "RIGHT": True,
        "LEFT": False,
        "UP": True,
        "DOWN": True
    }

    clock = pygame.time.Clock()
    while True:
        flag = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction["LEFT"]:
                    snake.dx = -1
                    snake.dy = 0
                    direction = {
                        "RIGHT": False,
                        "LEFT": False,
                        "UP": True,
                        "DOWN": True
                    }
                    flag = False
                    screen.fill(black_color)
                    borders_sprite.draw(screen)
                    snake.move()
                    snake.draw(screen)
                    food_spite.draw(screen)
                    crash_sprite.draw(screen)
                    score_string.update(SCORE)
                    score_string.draw(screen)
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction["RIGHT"]:
                    snake.dx = 1
                    snake.dy = 0
                    direction = {
                        "RIGHT": False,
                        "LEFT": False,
                        "UP": True,
                        "DOWN": True
                    }
                    flag = False
                    screen.fill(black_color)
                    borders_sprite.draw(screen)
                    snake.move()
                    snake.draw(screen)
                    food_spite.draw(screen)
                    crash_sprite.draw(screen)
                    score_string.update(SCORE)
                    score_string.draw(screen)
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction["UP"]:
                    snake.dx = 0
                    snake.dy = -1
                    direction = {
                        "RIGHT": True,
                        "LEFT": True,
                        "UP": False,
                        "DOWN": False
                    }
                    flag = False
                    screen.fill(black_color)
                    borders_sprite.draw(screen)
                    snake.move()
                    snake.draw(screen)
                    food_spite.draw(screen)
                    crash_sprite.draw(screen)
                    score_string.update(SCORE)
                    score_string.draw(screen)
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction["DOWN"]:
                    snake.dx = 0
                    snake.dy = 1
                    direction = {
                        "RIGHT": True,
                        "LEFT": True,
                        "UP": False,
                        "DOWN": False
                    }
                    flag = False
                    screen.fill(black_color)
                    borders_sprite.draw(screen)
                    snake.move()
                    snake.draw(screen)
                    food_spite.draw(screen)
                    crash_sprite.draw(screen)
                    score_string.update(SCORE)
                    score_string.draw(screen)
        if flag:
            screen.fill(black_color)
            borders_sprite.draw(screen)
            snake.move()
            if len(snake.body) == 420 and classic_type:
                win_screen(screen)
            if len(snake.body) == 372 and labyrinth_type == "Tunnel":
                win_screen(screen)
            if len(snake.body) == 391 and labyrinth_type == "Mill":
                win_screen(screen)
            snake.draw(screen)
            food_spite.draw(screen)
            crash_sprite.draw(screen)
            score_string.update(SCORE)
            score_string.draw(screen)

        if not snake.alive:
            lose_screen(screen)

        pygame.display.flip()
        clock.tick(5)


if __name__ == "__main__":
    main()
