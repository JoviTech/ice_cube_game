import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 700

# pygame.transform.scale(pygame.image.load(os.path.join("Spirit", "bg.png")),(0,0))
#pygame.transform.scale2x(pygame.image.load(os.path.join("Spirit", "base.png")))

IMAGEM_CAVALO = pygame.transform.scale(pygame.image.load(os.path.join("Spirit", "cavalo.jpg")),(80,80))
IMAGEM_BG = pygame.transform.scale2x(pygame.image.load(os.path.join("Spirit", "bg.png")))
IMAGEM_TRONCO = pygame.transform.scale(pygame.image.load(os.path.join("Spirit", "tronco.jpg")),(80,80))

IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join("Spirit", "base.png")))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join("Spirit", "base.png")))

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 40)

class Cavalo:
    IMGS = IMAGEM_CAVALO
    #ROTACAO_MAXIMA = 25
    #VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.imagem = self.IMGS

    def pular(self):
        self.velocidade = -10.5 #altura que pula
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento (S=So+vot+at^2/2)
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 10 #tempo de demora para cair

        self.y += deslocamento
#-------------------------------------------------------------------------------------------
       # if deslocamento < 0 or self.y < (self.altura + 50):
        #    if self.angulo < self.ROTACAO_MAXIMA:
         #       self.angulo = self.ROTACAO_MAXIMA
        #else:
         #   if self.angulo > -90:
          #      self.angulo -= self.VELOCIDADE_ROTACAO
#------------------------------------------------------------------------------------------
    def desenhar(self, tela):

        self.imagem = self.IMGS

        #desenhar a imagem ????????????????????????????????????????????????????????????????
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    # filtra por pixels dentro do retangulo do passaro
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Tronco:
    VELOCIDADE = 8
    ALTURA = 550 #LOCALIZAÇÃO NO EIXO Y

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_base = 0
        self.TRONCO = IMAGEM_TRONCO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        #self.largura = random.randrange(50, 350) localização aleatoria no eixo y
        self.pos_base = self.altura + self.ALTURA

    def mover(self):
        self.x -= self.VELOCIDADE # negativo pois anda para trás no eixo x

    def desenhar(self, tela):
        tela.blit(self.TRONCO, (self.x, self.pos_base))

    def colidir(self, cavalo):
        cavalo_mask = cavalo.get_mask()
        tronco_mask = pygame.mask.from_surface(self.TRONCO)

        distancia_tronco = (self.x - cavalo.x, self.pos_base - round(cavalo.y))

        #ver se bateu
        tronco_ponto = cavalo_mask.overlap(tronco_mask, distancia_tronco)

        if tronco_ponto:
            return True

class Chao:
    VELOCIDADE: 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO


    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA
        self.BASE = IMAGEM_CHAO
        self.pos_base = 0

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        elif self.x2 + self.LARGURA <0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

    def colidir(self, cavalo): #???????????????????????????????????????w
        cavalo_mask = cavalo.get_mask()
        base_mask = pygame.mask.from_surface(self.BASE)

        distancia_base = (self.x - cavalo.x, self.pos_base - round(cavalo.y))

        base_ponto = cavalo_mask.overlap(base_mask, distancia_base)

        if base_ponto:
            return True

    #def colidir(self, cavalo):
     #   cavalo_mask = cavalo.get_mask()
     #   tronco_mask = pygame.mask.from_surface(self.TRONCO)

     #   distancia_tronco = (self.x - cavalo.x, self.pos_base - round(cavalo.y))

        # ver se bateu
       # tronco_ponto = cavalo_mask.overlap(tronco_mask, distancia_tronco)

      #  if tronco_ponto:
        #    return True


def desenhar_tela(tela, cavalos, troncos, chao, pontos):
    tela.blit(IMAGEM_BG, (0,-300))
    for cavalo in cavalos:
        cavalo.desenhar(tela)
    for tronco in troncos:
        tronco.desenhar(tela)

    # "1" para arredondar a letra, 255... codigo da cor branca em RGB
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255,255,255))
    # largura da tela - 10 - lagura do texto, esse 10 é do eixo y
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    cavalos = [Cavalo(230, 250)]
    chao = Chao(630)
    troncos = [Tronco(600)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()
    posicao_cavalo = Cavalo(230, 250)

    rodando = True

    while rodando:
        #FPS()
        relogio.tick(30)

        #interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for cavalo in cavalos:
                        cavalo.pular()

        #mover as coisas
        for cavalo in cavalos:
            cavalo.mover()

        adicinar_tronco =False
        remover_troncos = []
        for tronco in troncos:
            for i, cavalo in enumerate(cavalos):
                if tronco.colidir(cavalo):
                    cavalos.pop(i)
                if not tronco.passou and cavalo.x > tronco.x:
                    tronco.passou = True
                    adicinar_tronco = True
            tronco.mover()
            if tronco.x + tronco.TRONCO.get_width() < 0:
                remover_troncos.append(tronco)




        if adicinar_tronco:
            pontos += 1
            troncos.append(Tronco(600))

        for tronco in remover_troncos:
            troncos.remove (tronco)

        desenhar_tela(tela, cavalos, troncos, chao, pontos)



if __name__ == '__main__':
    main()



