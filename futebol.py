import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, pi

# Inicialização
pygame.init()
largura, altura = 800, 600
pygame.display.set_mode((largura, altura), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Campo de Futebol em OpenGL")

# Placar
placar_esq = 0
placar_dir = 0

# Bola
bola_pos = [0, 0]
bola_raio = 10
velocidade_bola = 5

# Jogadores
jogador1 = {"x": -300, "y": 0, "w": 20, "h": 40}
jogador2 = {"x": 280, "y": 0, "w": 20, "h": 40}

# Desenhar retângulo


def desenhar_retangulo(x, y, w, h):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()

# Desenhar circunferência


def desenhar_circulo(x, y, raio):
    glBegin(GL_LINE_LOOP)
    for i in range(100):
        ang = 2 * pi * i / 100
        glVertex2f(x + raio * cos(ang), y + raio * sin(ang))
    glEnd()

# Desenhar o campo


def desenhar_campo():
    # Fundo verde
    glColor3f(0, 0.5, 0)
    desenhar_retangulo(-400, -300, 800, 600)

    # Linhas brancas
    glColor3f(1, 1, 1)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)  # Linha de fora
    glVertex2f(-400, -300)
    glVertex2f(400, -300)
    glVertex2f(400, 300)
    glVertex2f(-400, 300)
    glEnd()

    # Linha do meio
    glBegin(GL_LINES)
    glVertex2f(0, -300)
    glVertex2f(0, 300)
    glEnd()

    # Círculo central
    desenhar_circulo(0, 0, 60)

    # Áreas do gol
    glBegin(GL_LINE_LOOP)
    glVertex2f(-400, -100)
    glVertex2f(-320, -100)
    glVertex2f(-320, 100)
    glVertex2f(-400, 100)
    glEnd()

    glBegin(GL_LINE_LOOP)
    glVertex2f(400, -100)
    glVertex2f(320, -100)
    glVertex2f(320, 100)
    glVertex2f(400, 100)
    glEnd()

# Atualizar placar


def verificar_gol():
    global placar_esq, placar_dir, bola_pos
    if bola_pos[0] - bola_raio < -400 and -100 < bola_pos[1] < 100:
        placar_dir += 1
        bola_pos = [0, 0]
    elif bola_pos[0] + bola_raio > 400 and -100 < bola_pos[1] < 100:
        placar_esq += 1
        bola_pos = [0, 0]

# Loop principal


def main():
    global bola_pos
    gluOrtho2D(-400, 400, -300, 300)
    clock = pygame.time.Clock()

    while True:
        glClear(GL_COLOR_BUFFER_BIT)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                return

        # Teclas
        teclas = pygame.key.get_pressed()

        # Movimento bola (setas + wasd)
        if teclas[K_LEFT] or teclas[K_a]:
            bola_pos[0] -= velocidade_bola
        if teclas[K_RIGHT] or teclas[K_d]:
            bola_pos[0] += velocidade_bola
        if teclas[K_UP] or teclas[K_w]:
            bola_pos[1] += velocidade_bola
        if teclas[K_DOWN] or teclas[K_s]:
            bola_pos[1] -= velocidade_bola

        # Desenho campo
        desenhar_campo()

        # Bola
        glColor3f(1, 1, 1)
        desenhar_circulo(*bola_pos, bola_raio)

        # Jogador 1 (amarelo)
        glColor3f(1, 1, 0)
        desenhar_retangulo(jogador1["x"], jogador1["y"],
                           jogador1["w"], jogador1["h"])

        # Jogador 2 (azul)
        glColor3f(0, 0, 1)
        desenhar_retangulo(jogador2["x"], jogador2["y"],
                           jogador2["w"], jogador2["h"])

        # Placar e Gol
        verificar_gol()

        pygame.display.set_caption(
            f"Placar - Esq (Amarelo): {placar_esq} | Dir (Azul): {placar_dir}")
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
