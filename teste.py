import pygame
import os

running = True
verde_escuro = (0,128,0)

# Inicializa pygame
pygame.init();

# Inicializa janela com fundo verde escuro
screen = pygame.display.set_mode((1350, 700))
screen.fill(verde_escuro)

# Carrega uma imagem PNG com transparencia
img = pygame.image.load(os.path.join("Spirit", "tronco.png")).convert_alpha()

# Recupera as dimensoes da imagem
w, h = img.get_size()

# Escalas da imagem
scales = [ 0.5, 0.33, 0.25, 0.1 ]

# Exibe a mesma imagem, em escalas diferentes, lado a lado.
posx = 0
for s in scales:
    redim = pygame.transform.smoothscale( img, (int(w*s), int(h*s)) )
    screen.blit( redim, (posx, 0) )
    posx += int(w*s)

# Loop principal de eventos
clock = pygame.time.Clock()
while running:
    clock.tick(10)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    pygame.display.flip()

# Fim
pygame.exit()
sys.exit()
