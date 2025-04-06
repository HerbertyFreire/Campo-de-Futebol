import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

largura, altura = 800, 600
bola_x, bola_y = 400, 300
placar_esq, placar_dir = 0, 0


def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()


def bresenham_line(x0, y0, x1, y1):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx - dy

    while True:
        draw_pixel(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def bresenham_circle(xc, yc, r):
    x, y = 0, r
    d = 3 - 2 * r
    while y >= x:
        for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y),
                       (y, x), (-y, x), (y, -x), (-y, -x)]:
            draw_pixel(xc + dx, yc + dy)
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6


def desenha_campo():
    # Campo verde
    glColor3f(0.0, 0.7, 0.0)
    glBegin(GL_QUADS)
    glVertex2i(0, 0)
    glVertex2i(largura, 0)
    glVertex2i(largura, altura)
    glVertex2i(0, altura)
    glEnd()

    glColor3f(1, 1, 1)  # Linhas brancas

    # Contorno do campo
    bresenham_line(100, 50, 100, 550)
    bresenham_line(700, 50, 700, 550)
    bresenham_line(100, 50, 700, 50)
    bresenham_line(100, 550, 700, 550)

    # Linha do meio
    bresenham_line(400, 50, 400, 550)

    # Círculo central
    bresenham_circle(400, 300, 60)

    # Gol esquerdo
    bresenham_line(90, 250, 90, 350)      # vertical
    bresenham_line(90, 350, 100, 350)     # inferior
    bresenham_line(90, 250, 100, 250)     # superior

    # Gol direito
    bresenham_line(710, 250, 710, 350)    # vertical
    bresenham_line(700, 250, 710, 250)    # superior
    bresenham_line(700, 350, 710, 350)    # inferior


def desenha_bola():
    glColor3f(1, 1, 1)
    bresenham_circle(bola_x, bola_y, 10)


def render_text(x, y, text):
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def verifica_gol():
    global bola_x, bola_y, placar_esq, placar_dir
    if bola_x < 100:
        placar_dir += 1
        bola_x, bola_y = 400, 300
    elif bola_x > 700:
        placar_esq += 1
        bola_x, bola_y = 400, 300


def main():
    global bola_x, bola_y

    pygame.init()
    glutInit()
    pygame.display.set_caption("Campo de Futebol - OpenGL + Python")
    pygame.display.set_mode((largura, altura), DOUBLEBUF | OPENGL)
    gluOrtho2D(0, largura, 0, altura)

    clock = pygame.time.Clock()
    running = True

    while running:
        glClear(GL_COLOR_BUFFER_BIT)
        desenha_campo()
        desenha_bola()
        render_text(340, 570, f"Placar: {placar_esq} x {placar_dir}")
        verifica_gol()

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == QUIT:
                running = False
            elif evento.type == KEYDOWN:
                if evento.key in [K_LEFT, K_a]:
                    bola_x -= 10
                elif evento.key in [K_RIGHT, K_d]:
                    bola_x += 10
                elif evento.key in [K_UP, K_w]:
                    bola_y += 10
                elif evento.key in [K_DOWN, K_s]:
                    bola_y -= 10

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
