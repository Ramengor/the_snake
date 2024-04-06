from random import randint, choice
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20  # РАЗМЕР СЕТКИ
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # ШИРИНА СЕТКИ 32
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # ВЫСОТА СЕТКИ 24

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Основной класс объекта"""

    def __init__(self, body_color=None):
        self.position = (
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2)
        )
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Случайное расположение яблока
        и было расположено в пределах поля
        """
        while True:
            self.position = (
                randint(0, GRID_HEIGHT) * GRID_SIZE,
                randint(0, GRID_WIDTH) * GRID_SIZE
            )
            if 0 <= self.position[0] < SCREEN_WIDTH and 0 <= self.position[1] < SCREEN_HEIGHT:
                break

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки"""
    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.next_direction = None
        self.direction = RIGHT  # Направление движения
        self.next_position = None
        self.body_color = (0, 250, 0)  # Цвет змейки
        self.last = None  # Последняя позиция змейки

    def update_direction(self):
        """ Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction  # Направление движения
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки"""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_position = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head_position)  # Добавляем голову в начало списка
        if len(self.positions) > self.length:
            self.positions.pop()  # Удаляем "хвост" из списка

    def draw(self):
        """Обрисовывает змейку на экране, затирая след """
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
        """Возвращает позицию головы змейки"""
        return self.positions[0]  # Позиция головы змейки

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения с собой"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])  # Направление движения змейки


def handle_keys(game_object):
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
    # Тут нужно создать экземпляры классов.
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)  # скорость змейки
        snake.move()  # Обновляет позицию змейки
        handle_keys(snake)  # Обработка нажатий клавиш
        snake.update_direction()  # Обновляет направление движения
        snake.get_head_position()  # Обновляет позицию головы змейки
        head_position = snake.get_head_position()  # Позиция головы змейки

        if head_position == apple.position:
            if snake.length == 1:
                snake.length += 1
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:-1]:
            snake.reset()  # Сбрасывает змейку в начальное состояние после столкновения с собой
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
