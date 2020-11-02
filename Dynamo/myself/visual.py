import pygame
from readerdxf import FindDxf
from itemprop import Polygon
import os.path

SCREEN_DIM = (1200, 800)


def export(path):
    file = FindDxf(path)
    polygons = file.find('LWPOLYLINE')
    return polygons


def draw_polygons(polygons, gameDisplay, width=0):
    for polygon in polygons:
        pygame.draw.polygon(gameDisplay, polygon.color, polygon.points, width)


def draw_help(gameDisplay):
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    font3 = pygame.font.SysFont('serif', 30)

    data = [["F1", "Show Help"],
            ["R", "Clear windows"],
            ["E", "Extract polygon"],
            ["Esc", "Quit"]
            ]

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (SCREEN_DIM[0], 0), SCREEN_DIM, (0, SCREEN_DIM[1])], 5)
    gameDisplay.blit(font3.render(
        'Introduction', True, (128, 128, 255)), (100, 100))

    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 150 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 150 + 30 * i))


def draw_stat(gameDisplay, polygons, path):
    """Показ статистики"""
    font = pygame.font.SysFont("serif", 14)
    left, top = SCREEN_DIM[0] - 200, 5
    data = [f'Файл: {os.path.basename(path)}',
            f'Extract polygon: {len(polygons)}',
            f'Начальная площадь: {100} м2'
            ]

    for i, text in enumerate(data):
        gameDisplay.blit(font.render(
            text, True, (255, 255, 255)), (left, top + 20 * i))


def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("Square")

    working = True
    polygons = []
    show_help = False

    path = os.path.abspath('primer.dxf')

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_F1:
                    show_help = not show_help

                if event.key == pygame.K_e:
                    polygons = export(path)
                if event.key == pygame.K_r:
                    polygons = []

        gameDisplay.fill((0, 0, 0))

        draw_polygons(polygons, gameDisplay)

        if show_help:
            draw_help(gameDisplay)

        draw_stat(gameDisplay, polygons, path)
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)


if __name__ == '__main__':
    main()
