from random import choice, randint
import pygame as pg

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
GRID_WIDTH = 32  # ШИРИНА СЕТКИ
GRID_HEIGHT = 24  # ВЫСОТА СЕТКИ
GRID_SIZE = 20  # РАЗМЕР СЕТКИ
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE

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
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Основной класс объекта."""

    def __init__(self, body_color=None):
        self.position = (
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2)
        )
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта."""
        raise NotImplementedError(
            f'{self.__class__.__name__} is not implemented.'
        )


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, position=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(position)

    def randomize_position(self, position=None):
        """Случайное расположение яблока
        и было расположено в пределах поля.
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in self.position:
                self.position = new_position
                break

    def draw(self):
        """Отрисовка яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.next_direction = None
        self.direction = RIGHT
        self.next_position = None
        self.body_color = (0, 250, 0)
        self.last = None
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction  # Направление движения
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_position = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()  # Удаляем "хвост" из списка

    def draw(self):
        """Обрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
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

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit  # Завершение при ESCAPE


class Stone(GameObject):
    """Класс камня."""

    def __init__(self, snake=None):
        super().__init__(body_color=(128, 128, 128))
        self.positions = []
        self.generetion_positions(snake)

    def generetion_positions(self, snake):
        """Генерирует позиции камня."""
        self.positions.clear()
        for _ in range(4):
            while True:
                new_position = (
                    randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                    randint(0, GRID_HEIGHT - 1) * GRID_SIZE
                )
                if new_position not in self.positions:
                    self.positions.append(new_position)
                if new_position not in snake.positions:
                    self.position = new_position
                    break

    def draw(self):
        """Отрисовка камней."""
        for self.position in self.positions:
            rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    """Главная функция."""
    pg.init()

    snake = Snake()
    apple = Apple(position=snake.get_head_position())
    stone = Stone(snake)

    while True:
        clock.tick(SPEED)
        snake.move()
        handle_keys(snake)
        snake.update_direction()
        head_position = snake.get_head_position()

        if head_position == apple.position:
            if snake.length == 1:
                snake.length += 1
            snake.length += 1
            apple.randomize_position(snake)
            stone.generetion_positions(snake)
        elif head_position in stone.positions:
            snake.reset()
            apple.randomize_position(snake)
            stone.generetion_positions(snake)
        elif snake.get_head_position() in snake.positions[1:-1]:
            snake.reset()
            apple.randomize_position(snake)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        stone.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
