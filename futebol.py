import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from math import sin, cos

# Dimensões
WIDTH, HEIGHT = 1000, 600
ball_radius = 10
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = 5

# Jogadores
player_width, player_height = 10, 30
players_team1 = [[100, 100], [100, HEIGHT//2], [100, HEIGHT-100]]
players_team2 = [[WIDTH-110, 100],
                 [WIDTH-110, HEIGHT//2], [WIDTH-110, HEIGHT-100]]

# Gol
goal_width = 10
goal_height = 150
goal_top = (HEIGHT - goal_height) // 2

# Placar
goals = {'azul': 0, 'vermelho': 0}


def desenhar_retangulo(x, y, w, h, cor):
    glColor3f(*cor)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


def desenhar_circulo(x, y, r, cor, segmentos=32):
    glColor3f(*cor)
    glBegin(GL_LINE_LOOP)
    for i in range(segmentos):
        theta = 2.0 * 3.1415926 * i / segmentos
        dx = r * cos(theta)
        dy = r * sin(theta)
        glVertex2f(x + dx, y + dy)
    glEnd()


def desenhar_texto(x, y, texto, cor=(1, 1, 1)):
    glColor3f(*cor)
    glRasterPos2f(x, y)
    for ch in texto:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def desenhar_campo():
    glClear(GL_COLOR_BUFFER_BIT)

    # Fundo verde
    glClearColor(0, 0.6, 0, 1)

    # Gols
    desenhar_retangulo(0, goal_top, goal_width, goal_height, (1, 1, 1))
    desenhar_retangulo(WIDTH - goal_width, goal_top,
                       goal_width, goal_height, (1, 1, 1))

    # Linha do meio
    desenhar_retangulo(WIDTH//2 - 1, 0, 3, HEIGHT, (1, 1, 1))

    # Círculo central
    desenhar_circulo(WIDTH//2, HEIGHT//2, 70, (1, 1, 1))


def desenhar_jogadores():
    for player in players_team1:
        desenhar_retangulo(*player, player_width, player_height, (0, 0, 1))
    for player in players_team2:
        desenhar_retangulo(*player, player_width, player_height, (1, 0, 0))


def desenhar_bola():
    desenhar_circulo(ball_pos[0], ball_pos[1], ball_radius, (1, 1, 1))


def checar_colisoes():
    for team in [players_team1, players_team2]:
        for player in team:
            if (player[0] <= ball_pos[0] <= player[0]+player_width and
                    player[1] <= ball_pos[1] <= player[1]+player_height):
                return True
    return False


def checar_gol():
    global ball_pos
    if ball_pos[0] - ball_radius <= goal_width and goal_top <= ball_pos[1] <= goal_top + goal_height:
        goals['vermelho'] += 1
        ball_pos = [WIDTH // 2, HEIGHT // 2]
    elif ball_pos[0] + ball_radius >= WIDTH - goal_width and goal_top <= ball_pos[1] <= goal_top + goal_height:
        goals['azul'] += 1
        ball_pos = [WIDTH // 2, HEIGHT // 2]


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    gluOrtho2D(0, WIDTH, HEIGHT, 0)  
    glutInit()

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            ball_pos[1] -= ball_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            ball_pos[1] += ball_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            ball_pos[0] -= ball_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            ball_pos[0] += ball_speed

        if checar_colisoes():
            ball_pos[0] -= ball_speed if keys[pygame.K_d] or keys[pygame.K_RIGHT] else 0
            ball_pos[0] += ball_speed if keys[pygame.K_a] or keys[pygame.K_LEFT] else 0
            ball_pos[1] -= ball_speed if keys[pygame.K_s] or keys[pygame.K_DOWN] else 0
            ball_pos[1] += ball_speed if keys[pygame.K_w] or keys[pygame.K_UP] else 0

        checar_gol()

        desenhar_campo()
        desenhar_jogadores()
        desenhar_bola()

        # Desenhar placar
        placar = f"Azul {goals['azul']} x {goals['vermelho']} Vermelho"
        text_width = len(placar) * 9  
        desenhar_texto((WIDTH - text_width) // 2, 30, placar)

        pygame.display.flip()


if __name__ == '__main__':
    main()
