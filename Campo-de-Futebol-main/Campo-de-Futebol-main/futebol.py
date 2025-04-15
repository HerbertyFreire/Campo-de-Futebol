import pygame
import sys
import math
import random

# Inicialização
pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ronaldinho Soccer 64 - 3x3 football")
font = pygame.font.SysFont(None, 40)
pygame.mixer.init()
pygame.mixer.music.load("ronaldinhoabertura.mp3")  
pygame.mixer.music.play()

# Cores
verde = (0, 128, 0)
branco = (255, 255, 255)
azul = (0, 0, 255)
vermelho = (255, 0, 0)
preto = (0, 0, 0)

# Jogador e bola
player_radius = 10
ball_radius = 8
ball_speed = 5

# Placar
placar = [0, 0]

# Algoritmo de Bresenham - Retas
def bresenham_line(x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        screen.set_at((x0, y0), color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# Algoritmo de Bresenham - Circunferência
def bresenham_circle(xc, yc, r, color):
    x = 0
    y = r
    d = 3 - 2 * r
    while x <= y:
        for dx, dy in [(x, y), (y, x), (-x, y), (-y, x), (-x, -y), (-y, -x), (x, -y), (y, -x)]:
            if 0 <= xc + dx < WIDTH and 0 <= yc + dy < HEIGHT:
                screen.set_at((xc + dx, yc + dy), color)
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1

# Campo com Bresenham
def desenhar_campo():
    screen.fill(verde)
    # Campo
    bresenham_line(50, 50, WIDTH - 50, 50, branco)
    bresenham_line(WIDTH - 50, 50, WIDTH - 50, HEIGHT - 50, branco)
    bresenham_line(WIDTH - 50, HEIGHT - 50, 50, HEIGHT - 50, branco)
    bresenham_line(50, HEIGHT - 50, 50, 50, branco)

    # Meio campo
    bresenham_line(WIDTH // 2, 50, WIDTH // 2, HEIGHT - 50, branco)
    bresenham_circle(WIDTH // 2, HEIGHT // 2, 50, branco)

    # Gols
    bresenham_line(50, 180, 100, 180, branco)
    bresenham_line(100, 180, 100, 320, branco)
    bresenham_line(100, 320, 50, 320, branco)

    bresenham_line(WIDTH - 50, 180, WIDTH - 100, 180, branco)
    bresenham_line(WIDTH - 100, 180, WIDTH - 100, 320, branco)
    bresenham_line(WIDTH - 100, 320, WIDTH - 50, 320, branco)

# Jogadores
players1 = [[100, 150], [100, HEIGHT//2], [100, 350]]
players2 = [[WIDTH-100, 150], [WIDTH-100, HEIGHT//2], [WIDTH-100, 350]]

# Bola
ball = [WIDTH//2, HEIGHT//2]
ball_vel = [0, 0]

# Placar
placar = [0, 0]

def mover_bola():
    global placar, ball, ball_vel
    ball[0] += ball_vel[0]
    ball[1] += ball_vel[1]

    # Colisão com parede
    if ball[1] - ball_radius <= 50 or ball[1] + ball_radius >= HEIGHT - 50:
        ball_vel[1] = 0

    # Gol time 1
    if ball[0] - ball_radius <= 50:
        if 180 < ball[1] < 320:
            placar[1] += 1
            resetar_bola()
        else:
            ball_vel[0] = 0

    # Gol time 2
    if ball[0] + ball_radius >= WIDTH - 50:
        if 180 < ball[1] < 320:
            placar[0] += 1
            resetar_bola()
        else:
            ball_vel[0] = 0

def resetar_bola():
    ball[0], ball[1] = WIDTH//2, HEIGHT//2
    ball_vel[0] = 0
    ball_vel[1] = 0

def desenhar_placar():
    texto = font.render(f"{placar[0]} x {placar[1]}", True, branco)
    screen.blit(texto, (WIDTH//2 - 30, 10))

def verificar_colisao_bola_jogador():
    global ball_vel
    for p in players1 + players2:
        dist = math.sqrt((ball[0] - p[0]) ** 2 + (ball[1] - p[1]) ** 2)
        if dist < (ball_radius + player_radius):
            # Colisão detectada, a bola para (não passa por cima do jogador)
            angle = math.atan2(ball[1] - p[1], ball[0] - p[0])
            ball[0] = p[0] + (ball_radius + player_radius) * math.cos(angle)
            ball[1] = p[1] + (ball_radius + player_radius) * math.sin(angle)
            ball_vel = [0, 0]
            break

def desenhar_jogadores():
    for p in players1:
        pygame.draw.circle(screen, azul, p, player_radius)
    for p in players2:
        pygame.draw.circle(screen, vermelho, p, player_radius)

# Loop principal
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    desenhar_campo()
    mover_bola()
    verificar_colisao_bola_jogador()
    desenhar_placar()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Teclas pressionadas para controlar a bola
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Cima (W)
        ball_vel[1] = -ball_speed
    elif keys[pygame.K_s]:  # Baixo (S)
        ball_vel[1] = ball_speed
    else:
        ball_vel[1] = 0

    if keys[pygame.K_a]:  # Esquerda (A)
        ball_vel[0] = -ball_speed
    elif keys[pygame.K_d]:  # Direita (D)
        ball_vel[0] = ball_speed
    else:
        ball_vel[0] = 0

    if keys[pygame.K_UP]:  # Cima (Seta para cima)
        ball_vel[1] = -ball_speed
    elif keys[pygame.K_DOWN]:  # Baixo (Seta para baixo)
        ball_vel[1] = ball_speed
    else:
        ball_vel[1] = 0

    if keys[pygame.K_LEFT]:  # Esquerda (Seta para esquerda)
        ball_vel[0] = -ball_speed
    elif keys[pygame.K_RIGHT]:  # Direita (Seta para direita)
        ball_vel[0] = ball_speed
    else:
        ball_vel[0] = 0

    # Desenhar jogadores (eles ficam parados)
    desenhar_jogadores()

    # Desenhar bola
    pygame.draw.circle(screen, branco, ball, ball_radius)

    pygame.display.flip()
