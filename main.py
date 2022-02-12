from utils import *
import tkinter as tk
from tkinter import colorchooser


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avis Designer")


def init_grid(rows, cols, colour):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(colour)

    return grid


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i *
                             PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, BLACK, (0, i * PIXEL_SIZE),
                             (WIDTH, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(win, BLACK, (i * PIXEL_SIZE, 0),
                             (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(WIN, grid)

    for button in buttons:
        button.draw(WIN)

    pygame.display.update()


def get_row_col_from_mouse_pos(pos):
    row = pos[1] // PIXEL_SIZE
    col = pos[0] // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError

    return row, col


def fill(row, col, target_colour, drawing_colour):
    if grid[row][col] != target_colour:
        return
    if grid[row][col] == drawing_colour:
        return
    grid[row][col] = drawing_colour
    fill(row + 1, col, target_colour, drawing_colour)
    fill(row - 1, col, target_colour, drawing_colour)
    fill(row, col + 1, target_colour, drawing_colour)
    fill(row, col - 1, target_colour, drawing_colour)

    return


def erase(row, col, target_colour, tool):
    if tool == "fill":
        if grid[row][col] != target_colour:
            return
        grid[row][col] = BG_COLOR
        erase(row + 1, col, target_colour, tool)
        erase(row - 1, col, target_colour, tool)
        erase(row, col + 1, target_colour, tool)
        erase(row, col - 1, target_colour, tool)

        return
    else:
        grid[row][col] = BG_COLOR


run = True
clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_colour = BLACK
tool = "pen"
erase_ = False

button_y = HEIGHT - TOOLBAR_HEIGHT/2 - 25
buttons = [
    Button(10, button_y, 50, 50, BLACK),
    Button(70, button_y, 50, 50, RED),
    Button(130, button_y, 50, 50, GREEN),
    Button(190, button_y, 50, 50, BLUE),
    Button(250, button_y, 50, 50, WHITE, "RGB", BLACK),
    Button(310, button_y, 50, 50, BG_COLOR, "Erase", BLACK),
    Button(370, button_y, 50, 50, BG_COLOR, "Clear", BLACK),
    Button(430, button_y, 50, 50, drawing_colour, "Pen", BLACK),
    Button(490, button_y, 50, 50, drawing_colour, "Fill", BLACK),
]


while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            try:
                row, col = get_row_col_from_mouse_pos(pos)
                if not erase_:
                    if tool == "pen":
                        grid[row][col] = drawing_colour
                    if tool == "fill":
                        fill(row, col, grid[row][col], drawing_colour)
                else:
                    erase(row, col, grid[row][col], tool)
            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue
                    if button.text == "Pen":
                        tool = "pen"
                    if button.text == "Fill":
                        tool = "fill"
                    if button.text == "Erase":
                        erase_ = not erase_     

                    drawing_colour = button.colour

                    if button.text == "RGB":
                        colour = colorchooser.askcolor(
                            initialcolor=BLACK)
                        if colour[0]:
                            drawing_colour = colour[1]

                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_colour = BLACK
                        break


    draw(WIN, grid, buttons)

pygame.quit()
