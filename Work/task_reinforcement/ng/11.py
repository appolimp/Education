import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode([300, 300])


def random_point_coud_2D(n, radius=10, deviation=3):
    pts = [(0, 0)] * n
    for i in range(n):
        angle = random.random() * 2 * math.pi
        rad = random.gauss(radius, deviation)
        pts[i] = (math.cos(angle) * rad, math.sin(angle) * rad)
    return pts


def translate_pts(pts, shift):
    return [(pt[0] + shift[0], pt[1] + shift[1]) for pt in pts]


def translate_edges(edges, shift):
    tx, ty = shift
    return [((ptA[0] + tx, ptA[1] + ty), (ptB[0] + tx, ptB[1] + ty)) for (ptA, ptB) in edges]


def pt_center(pts):
    if (len(pts) == 0):
        return (0, 0)
    sum_x = 0
    sum_y = 0
    for (x, y) in pts:
        sum_x += x
        sum_y += y
    return (sum_x / len(pts), sum_y / len(pts))


def dot(ptA, ptB):
    return ptA[0] * ptB[0] + ptA[1] * ptB[1]


def crossz(ptA, ptB):
    return ptA[0] * ptB[1] - ptA[1] * ptB[0]


def norm(vec):
    l = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
    return (vec[0] / l, vec[1] / l)


def point_in_triangle(pt, edges):
    for (ptA, ptB) in edges:
        vecside = norm((ptB[0] - ptA[0], ptB[1] - ptA[1]))
        vecpt = norm((pt[0] - ptA[0], pt[1] - ptA[1]))
        side = (crossz(vecside, vecpt) > 0)  # pt is on correct side of this edge
        proj = 0 <= dot(vecside, vecpt) and dot(vecside, vecpt) <= 1  # pt lies between A and B in projection
        if (not (side and proj)):
            # test failed for any edge.. fails overall
            return False
    return True


# this is a hack. horrible n^3 time
def get_center_triangle(pts):
    # sort points in terms of angle from x-axis
    pts.sort()
    # test every combination of 3 points
    for i in range(len(pts)):
        ptA = pts[i]
        for j in range(len(pts)):
            if j == i:
                continue
            ptB = pts[j]
            for k in range(len(pts)):
                if k == j or k == i:
                    continue
                ptC = pts[k]
                if point_in_triangle((0, 0), [(ptA, ptB), (ptB, ptC), (ptC, ptA)]):
                    return (ptA, ptB, ptC)
    print("NO CENTER TRIANGLE FOUND")
    return None


def surface(pts):
    center = pt_center(pts)
    tx = -center[0]
    ty = -center[1]
    pts = translate_pts(pts, (tx, ty))
    # tricky part: initialization
    # initialize edges such that you have a triangle with the origin inside of it
    # in 3D, this will be a tetrahedron.
    ptA, ptB, ptC = get_center_triangle(pts)
    print(ptA, ptB, ptC)
    # tracking edges we've already included (triangles in 3D)
    edges = [(ptA, ptB), (ptB, ptC), (ptC, ptA)]
    # loop over all other points
    pts.remove(ptA)
    pts.remove(ptB)
    pts.remove(ptC)
    draw_scene(translate_pts(pts, (-tx, -ty)), translate_edges(edges, (-tx, -ty)))
    pygame.event.wait()
    for pt in pts:
        ptA = (0, 0)
        ptB = (0, 0)
        # find the edge that this point will be splitting
        for (ptA, ptB) in edges:
            if crossz(ptA, pt) > 0 and crossz(pt, ptB) > 0:
                break
        edges.remove((ptA, ptB))
        edges.append((ptA, pt))
        edges.append((pt, ptB))
        draw_scene(translate_pts(pts, (-tx, -ty)), translate_edges(edges, (-tx, -ty)))
        pygame.event.wait()

    # translate everything back
    edges = translate_edges(edges, (-tx, -ty))
    return edges


# PYGAME/GRAPHICS

def clear_screen():
    screen.fill([255, 255, 255])


def draw_pts(pts, clear=True, size=1):
    if clear:
        clear_screen()
    for pt in pts:
        pygame.draw.circle(screen, (0, 0, 0), (int(pt[0]), int(pt[1])), size)


def draw_lines(lines, clear=True, size=1):
    if clear:
        clear_screen()
    for line in lines:
        pygame.draw.line(screen, (0, 0, 0), (int(line[0][0]), int(line[0][1])), (int(line[1][0]), int(line[1][1])),
                         size)


def draw_scene(pts, lines):
    draw_pts(pts, size=3)
    draw_lines(lines, clear=False)
    pygame.display.update()


if __name__ == '__main__':
    pts = random_point_coud_2D(100, radius=100, deviation=10)
    pts = translate_pts(pts, (150, 150))
    # draw_scene(pts, [])
    # pause = raw_input()
    draw_scene(pts, surface(pts))
    pygame.image.save(screen, 'point_cloud_demo.jpg')
    pygame.quit()
