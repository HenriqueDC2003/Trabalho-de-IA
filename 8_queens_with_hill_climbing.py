import pygame
import sys
import random

# Configurações
TAM_CELULA = 60
NUM_RAINHAS = 8
LARGURA = TAM_CELULA * NUM_RAINHAS
ALTURA = TAM_CELULA * NUM_RAINHAS + 45
LARGURA_BOTAO = LARGURA
ALTURA_BOTAO = 45

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("8 Rainhas - Hill Climbing")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Calcula o número de conflitos entre rainhas
def contar_conflitos(solucao):
    conflitos = 0
    for i in range(NUM_RAINHAS):
        for j in range(i + 1, NUM_RAINHAS):
            if solucao[i] == solucao[j] or abs(solucao[i] - solucao[j]) == abs(i - j):
                conflitos += 1
    return conflitos

# Hill Climbing para encontrar uma solução
def hill_climbing():
    estado_atual = [random.randint(0, NUM_RAINHAS - 1) for _ in range(NUM_RAINHAS)]
    while True:
        conflitos_atual = contar_conflitos(estado_atual)
        if conflitos_atual == 0:
            return estado_atual  # Solução encontrada

        melhor_estado = list(estado_atual)
        melhor_conflitos = conflitos_atual

        for coluna in range(NUM_RAINHAS):
            original = estado_atual[coluna]
            for linha in range(NUM_RAINHAS):
                if linha == original:
                    continue
                estado_atual[coluna] = linha
                novos_conflitos = contar_conflitos(estado_atual)
                if novos_conflitos < melhor_conflitos:
                    melhor_conflitos = novos_conflitos
                    melhor_estado = list(estado_atual)
            estado_atual[coluna] = original  # Restaura a posição original

        if melhor_conflitos >= conflitos_atual:
            return estado_atual  # Ótimo local atingido
        estado_atual = melhor_estado

# Funções de desenho
def desenhar_tabuleiro():
    for linha in range(NUM_RAINHAS):
        for coluna in range(NUM_RAINHAS):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            rect = pygame.Rect(coluna * TAM_CELULA, linha * TAM_CELULA, TAM_CELULA, TAM_CELULA)
            pygame.draw.rect(screen, cor, rect)

def desenhar_rainhas(solucao):
    for coluna, linha in enumerate(solucao):
        center_x = coluna * TAM_CELULA + TAM_CELULA // 2
        center_y = linha * TAM_CELULA + TAM_CELULA // 2
        pygame.draw.circle(screen, VERMELHO, (center_x, center_y), TAM_CELULA // 3)

def desenhar_botao():
    botao_rect = pygame.Rect(LARGURA // 2 - LARGURA_BOTAO // 2, ALTURA - ALTURA_BOTAO, LARGURA_BOTAO, ALTURA_BOTAO)
    pygame.draw.rect(screen, AZUL, botao_rect)
    font = pygame.font.Font(None, 36)
    texto = font.render("Nova Solução", True, BRANCO)
    screen.blit(texto, (botao_rect.x + (botao_rect.width - texto.get_width()) // 2, 
                        botao_rect.y + (botao_rect.height - texto.get_height()) // 2))

# Loop principal
def main():
    solucao = hill_climbing()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                botao_rect = pygame.Rect(LARGURA // 2 - LARGURA_BOTAO // 2, ALTURA - ALTURA_BOTAO, LARGURA_BOTAO, ALTURA_BOTAO)
                if botao_rect.collidepoint(mouse_x, mouse_y):
                    solucao = hill_climbing()

        screen.fill(BRANCO)
        desenhar_tabuleiro()
        desenhar_rainhas(solucao)
        desenhar_botao()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
