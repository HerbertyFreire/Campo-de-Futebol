# ⚽ Campo de Futebol em OpenGL com Bresenham

Projeto feito em Python utilizando OpenGL e o algoritmo de Bresenham para desenhar um campo de futebol com movimentação de bola, placar e controle por teclado.

## ✨ Funcionalidades

- Desenho do campo de futebol utilizando o algoritmo de **Bresenham** para retas e circunferências.
- **Bola** desenhada com circunferência de Bresenham.
- Movimento da bola com **teclas direcionais (↑ ↓ ← →)** e também com **WASD**.
- **Placar** atualizado automaticamente quando a bola entra no gol.
- A bola retorna ao centro após o gol.
- Linhas de **gol** desenhadas com Bresenham.
- Exibição do placar usando **texto OpenGL (GLUT)**.

  ## 🧠 Controles

 - ← ou A	Move a bola para a esquerda
 - → ou D	Move a bola para a direita
 - ↑ ou W	Move a bola para cima
 - ↓ ou S	Move a bola para baixo
 - ESC	Sai do jogo (via botão de fechar)

## 📦 Requisitos

- Python 3.x
- Pygame
- PyOpenGL

## 🧪 Instalação

Instale as dependências com pip:

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate
