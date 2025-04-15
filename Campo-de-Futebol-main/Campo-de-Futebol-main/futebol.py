import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

# Inicialização
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("ronaldinhoabertura.mp3")  
pygame.mixer.music.play()

WIDTH, HEIGHT = 900, 500
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Ronaldinho Soccer 64 - 3x3 Football")

# Definindo o sistema de coordenadas
gluOrtho2D(0, WIDTH, HEIGHT, 0)  # Y invertido para combinar com Pygame

# Cores
BRANCO = (1, 1, 1)
VERDE = (0, 0.5, 0)
AZUL = (0, 0, 1)
VERMELHO = (1, 0, 0)

# Jogadores e bola
player_radius = 10
ball_radius = 8
ball_speed = 5
placar = [0, 0]

# Jogadores time 1 (azul) - lado esquerdo
players1 = [
    [100, HEIGHT // 2],                        # Goleiro
    [180, 100], [180, 250], [180, 400],        # Defensores
    [260, 80], [260, 180], [260, 320], [260, 420],  # Meio-campistas
    [340, 120], [340, 250], [340, 380]         # Atacantes
]

# Jogadores time 2 (vermelho) - lado direito
players2 = [
    [WIDTH - 100, HEIGHT // 2],                        # Goleiro
    [WIDTH - 180, 100], [WIDTH - 180, 250], [WIDTH - 180, 400],  # Defensores
    [WIDTH - 260, 80], [WIDTH - 260, 180], [WIDTH - 260, 320], [WIDTH - 260, 420],  # Meio-campistas
    [WIDTH - 340, 120], [WIDTH - 340, 250], [WIDTH - 340, 380]   # Atacantes
]

ball = [WIDTH//2, HEIGHT//2]
ball_vel = [0, 0]

# Funções de desenho com OpenGL
def bresenham_line(x0, y0, x1, y1, color):
    glColor3fv(color)
    glBegin(GL_POINTS)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        glVertex2i(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    glEnd()

def bresenham_circle(xc, yc, r, color):
    x = 0
    y = r
    d = 3 - 2 * r
    glColor3fv(color)
    glBegin(GL_POINTS)
    while x <= y:
        for dx, dy in [(x, y), (y, x), (-x, y), (-y, x),
                       (-x, -y), (-y, -x), (x, -y), (y, -x)]:
            glVertex2i(xc + dx, yc + dy)
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    glEnd()

def desenhar_circulo_preenchido(xc, yc, r, color):
    glColor3fv(color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(xc, yc)
    for angle in range(0, 361, 5):
        rad = math.radians(angle)
        glVertex2f(xc + math.cos(rad) * r, yc + math.sin(rad) * r)
    glEnd()

def desenhar_campo():
    glClearColor(*VERDE, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    # Linhas do campo
    bresenham_line(50, 50, WIDTH - 50, 50, BRANCO)
    bresenham_line(WIDTH - 50, 50, WIDTH - 50, HEIGHT - 50, BRANCO)
    bresenham_line(WIDTH - 50, HEIGHT - 50, 50, HEIGHT - 50, BRANCO)
    bresenham_line(50, HEIGHT - 50, 50, 50, BRANCO)

    # Meio campo
    bresenham_line(WIDTH // 2, 50, WIDTH // 2, HEIGHT - 50, BRANCO)
    bresenham_circle(WIDTH // 2, HEIGHT // 2, 50, BRANCO)

    # Gols
    bresenham_line(50, 180, 100, 180, BRANCO)
    bresenham_line(100, 180, 100, 320, BRANCO)
    bresenham_line(100, 320, 50, 320, BRANCO)

    bresenham_line(WIDTH - 50, 180, WIDTH - 100, 180, BRANCO)
    bresenham_line(WIDTH - 100, 180, WIDTH - 100, 320, BRANCO)
    bresenham_line(WIDTH - 100, 320, WIDTH - 50, 320, BRANCO)

def desenhar_jogadores():
    for p in players1:
        desenhar_circulo_preenchido(p[0], p[1], player_radius, AZUL)
    for p in players2:
        desenhar_circulo_preenchido(p[0], p[1], player_radius, VERMELHO)

def desenhar_bola():
    desenhar_circulo_preenchido(ball[0], ball[1], ball_radius, BRANCO)

font = pygame.font.SysFont(None, 40)
def desenhar_placar():
    texto = font.render(f"{placar[0]} x {placar[1]}", True, (255, 255, 255), (0, 0, 0))
    texto_data = pygame.image.tostring(texto, "RGBA", True)
    glRasterPos2f(WIDTH//2 - texto.get_width() // 2, 40)
    glDrawPixels(texto.get_width(), texto.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, texto_data)


def mover_bola():
    global placar
    ball[0] += ball_vel[0]
    ball[1] += ball_vel[1]

    # Colisão com parede
    if ball[1] - ball_radius <= 50 or ball[1] + ball_radius >= HEIGHT - 50:
        ball_vel[1] = 0

    # Gol time 1
    if ball[0] - ball_radius <= 50 and 180 < ball[1] < 320:
        placar[1] += 1  # Time 2 marca
        resetar_bola()
    elif ball[0] - ball_radius <= 50:
        ball_vel[0] = 0

    # Gol time 2
    if ball[0] + ball_radius >= WIDTH - 50 and 180 < ball[1] < 320:
        placar[0] += 1  # Time 1 marca
        resetar_bola()
    elif ball[0] + ball_radius >= WIDTH - 50:
        ball_vel[0] = 0

def resetar_bola():
    ball[0], ball[1] = WIDTH // 2, HEIGHT // 2
    ball_vel[0], ball_vel[1] = 0, 0

def verificar_colisao_bola_jogador():
    global ball_vel
    for p in players1 + players2:
        dist = math.hypot(ball[0] - p[0], ball[1] - p[1])
        if dist < (ball_radius + player_radius):
            angle = math.atan2(ball[1] - p[1], ball[0] - p[0])
            ball[0] = p[0] + (ball_radius + player_radius) * math.cos(angle)
            ball[1] = p[1] + (ball_radius + player_radius) * math.sin(angle)
            ball_vel = [0, 0]
            break




# Loop principal
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    
    
    desenhar_campo()
    mover_bola()
    verificar_colisao_bola_jogador()
    desenhar_jogadores()
    desenhar_bola()
    desenhar_placar()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Controles
    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        ball_vel[1] = -ball_speed
    elif keys[K_s] or keys[K_DOWN]:
        ball_vel[1] = ball_speed
    else:
        ball_vel[1] = 0

    if keys[K_a] or keys[K_LEFT]:
        ball_vel[0] = -ball_speed
    elif keys[K_d] or keys[K_RIGHT]:
        ball_vel[0] = ball_speed
    else:
        ball_vel[0] = 0

