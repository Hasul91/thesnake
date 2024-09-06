"""game snake."""
import pygame as pg
from random import randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
POINTER = tuple[int, int]
UP: POINTER = (0, -1)
DOWN: POINTER = (0, 1)
LEFT: POINTER = (-1, 0)
RIGHT: POINTER = (1, 0)

ColorRGB = tuple[int, int, int]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: ColorRGB = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: ColorRGB = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: ColorRGB = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: ColorRGB = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Основная."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """Инициализирует объект."""
        self.body_color = body_color
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self):
        """метода для отрисовки объекта."""
        raise NotImplementedError('метод будет реализован в подклассах')


class Apple(GameObject):
    """экземпляров класса Apple."""

    def __init__(self, occupied_positions=None, body_color=APPLE_COLOR):
        """Инициализирует объект."""
        super().__init__(body_color)
        # создаем инииализатор для яблоки
        self.occupied_positions = occupied_positions

    def draw(self):
        """Отрисовка объектов."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, occupied_positions:
                           set[tuple[int, int]] | None = None):
        """Позиция яблоки."""
        occupied_positions = occupied_positions or set()
        while True:
            new_position = (GRID_SIZE * randint(0, GRID_WIDTH - 1),
                            GRID_SIZE * randint(0, GRID_HEIGHT - 1))
            if new_position not in occupied_positions:
                self.position = new_position
                break


class Snake(GameObject):
    """экземпляров класса Snake."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует объект."""
        super().__init__(body_color)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """обновляет направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)  # Добавляем новую голову
        if len(self.positions) > self.length:
            self.positions.pop()  # Убираем конец (если длина превышает)

    def get_head_position(self):
        """возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.next_direction = None
        self.length = 1

    def draw(self):
        """отрисовывает змейку на экране."""
        for position in self.positions[:]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


key_directions = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT
}

opposite_directions = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}


def handle_keys(game_object):
    """Обрабатка события клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key in key_directions:
                new_direction = key_directions[event.key]
                # Упрощенная проверка на противоположное направление
                if new_direction != opposite_directions.get(game_object.
                                                            direction):
                    game_object.direction = new_direction


def main():
    """Основной цикл."""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
