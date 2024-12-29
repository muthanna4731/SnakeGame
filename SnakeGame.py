import pygame
import random

pygame.init()

#screen dimensions
WIDTH = 800
HEIGHT = 800
GRID_SIZE = 40
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

#colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

#clock
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        #initial head position
        head = self.body[0]

        #new head position
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self):
        self.grow = True

    def check_collision(self):
        return len(set(self.body)) < len(self.body)


class Food:
    def __init__(self, snake_body):
        self.position = self.generate_food(snake_body)

    def generate_food(self, snake_body):
        while True:
            food_pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if food_pos not in snake_body:
                return food_pos


def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))


def main():
    snake = Snake()
    food = Food(snake.body)
    score = 0

    #game start
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        snake.move()

        if snake.body[0] == food.position:
            snake.grow_snake()
            food = Food(snake.body)
            score += 1

        if snake.check_collision():
            running = False

        screen.fill(BLACK)

        draw_grid()

        #drawing the snake and food
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN,
                             (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                              GRID_SIZE - 1, GRID_SIZE - 1))

        pygame.draw.rect(screen, RED,
                         (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE,
                          GRID_SIZE - 1, GRID_SIZE - 1))

        #refresh
        pygame.display.flip()

        clock.tick(8)  

    #game over
    pygame.quit()
    print("Game Over\nScore:", score)

if __name__ == "__main__":
    main()