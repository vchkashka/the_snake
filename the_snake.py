from random import choice, randint
import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех обьектов игры."""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод рисования обьекта."""
        pass


class Apple(GameObject):
    """Класс, представляющий собой еду для змейки - яблоки"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__()
        self.body_color = body_color

    def randomize_position(self):
        """Метод, генерирующий положение обьекта Apple."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Метод рисования обьекта Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self, length=1,
                 positions=[((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))],
                 direction=RIGHT, next_direction=None, body_color=SNAKE_COLOR):
        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.body_color = body_color
        self.last = None

    def update_direction(self):
        """Метод, изменяющий направление обьекта Snake."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, отвечающий за передвижение обьекта Snake."""
        head_position = self.get_head_position()
        new_position_x, new_position_y = head_position

        if self.direction == LEFT:
            new_position_x -= GRID_SIZE
        elif self.direction == RIGHT:
            new_position_x += GRID_SIZE
        elif self.direction == UP:
            new_position_y -= GRID_SIZE
        else:
            new_position_y += GRID_SIZE

        new_position_x %= SCREEN_WIDTH
        new_position_y %= SCREEN_HEIGHT

        new_head_position = (new_position_x, new_position_y)
        self.positions.insert(0, new_head_position)

        if new_head_position in self.positions[2:]:
            self.reset()
        else:
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self):
        """Метод рисования обьекта Snake."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод, возвращающий первый элемент обьекта Snake."""
        return self.positions[0]

    def reset(self):
        """Метод, возвращающий обьект Snake в исходное состояние."""
        self.length = 1
        self.positions.clear()
        self.positions.insert(0, ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)))
        self.direction = choice(UP, DOWN, RIGHT, LEFT)


def handle_keys(game_object):
    """Функция, обрабатывающая действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция, содержащая основной игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position()
        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    main()
