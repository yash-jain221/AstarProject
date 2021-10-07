import pygame
import math
from queue import PriorityQueue

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Visualizer")

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = (255, 255, 255)
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def gpos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == (150, 150, 150)

    def is_open(self):
        return self.color == (128, 0, 128)

    def is_barrier(self):
        return self.color == (101, 67, 33)

    def is_start(self):
        return self.color == (64, 224, 208)

    def is_end(self):
        return self.color == (255, 0, 0)

    def make_open(self):
        self.color = (128, 0, 128)

    def make_closed(self):
        self.color = (150, 150, 150)

    def make_barrier(self):
        self.color = (101, 67, 33)

    def make_start(self):
        self.color = (64, 224, 208)

    def make_end(self):
        self.color = (255, 0, 0)

    def make_path(self):
        self.color = (65, 65, 65)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def reset(self):
        self.color = (255, 255, 255)

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def tracePath(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def Astar(draw, grid, start, end):

    count = 0
    openList = PriorityQueue()

    openList.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.gpos(), end.gpos())

    closed_set = {start}

    while not openList.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openList.get()[2]
        closed_set.remove(current)

        if current == end:
            tracePath(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbour in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.gpos(), end.gpos())
                if neighbour not in closed_set:
                    count += 1
                    openList.put((f_score[neighbour], count, neighbour))
                    closed_set.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, (128, 128, 128), (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, (128, 128, 128), (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill((255, 255, 255))

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):

    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            node = grid[row][col]

            if pygame.mouse.get_pressed()[0]:

                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    Astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)


