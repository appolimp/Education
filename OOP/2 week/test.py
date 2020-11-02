from ref import Vec2d, Polyline
import pygame

line = Polyline()



SCREEN_DIM = (800, 600)
pygame.init()
gameDisplay = pygame.display.set_mode(SCREEN_DIM)
working = True
hue = 0
color = pygame.Color(0)

while working:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            working = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                working = False
            if event.key == pygame.K_r:
                line.points = []
                # speeds = []
        if event.type == pygame.MOUSEBUTTONDOWN:
            line.add_point(Vec2d(*event.pos))

    gameDisplay.fill((0, 0, 0))
    hue = (hue + 1) % 360
    color.hsla = (hue, 100, 50, 100)
    line.graw_points(gameDisplay)
    line.graw_lines(gameDisplay)
    pygame.display.flip()

pygame.display.quit()
pygame.quit()
exit(0)