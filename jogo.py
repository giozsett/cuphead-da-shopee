import pygame
from sys import exit

# DEFINE A ANIMAÇÃO DO PROTAGONISTA
def animacao_protagonista():
    global protagonista_superficies, protagonista_index


    # Animação do personagem andando no chão e pulando.
    if(protagonista_retangulo.bottom < 470):
        protagonista_superficies = protagonista_pulando_superficie[int(protagonista_index)]
    else: 
        protagonista_index += 0.1
        if protagonista_index >= len(protagonista_andando_superficie): protagonista_index = 0
        protagonista_superficies = protagonista_andando_superficie[int(protagonista_index)]

    # Faz o owlet aparecer na tela.
    tela.blit(protagonista_superficies, protagonista_retangulo)




# INICIALIZA O PYGAME
pygame.init()

# CRIANDO A TELA DO JOGO E DEFININDO SEU NOME E TAMANHO
tamanho_tela = (960, 540)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Hollownait")

# IMPORTANDO ARQUIVOS DE IMAGEM DO JOGUIN
plano_fundo = pygame.image.load('assets/fundo/fundo-sem-camadas.png').convert()

# DEIXANDO OS TAMANHOS DE ACORDO COM O TAMANHO DA TELA
plano_fundo = pygame.transform.scale(plano_fundo, tamanho_tela)

# CARREGANDO IMAGENS DE ANIMAÇÃO DO PERSONAGEM
protagonista_index = 0
protagonista_andando_superficie = []
protagonista_pulando_superficie = []
protagonista_atacando_superficie = []

# CARREGA O PROTAGONISTA ATRAVÉS DE UMA LISTA
# Protagonista andando
for imagem in range(1, 7):
    img = pygame.image.load(f'assets/protagonista/corrida/owlet_walk{imagem}.png').convert_alpha()
    # Redimensionando pois o owlet está muito grande.
    img = pygame.transform.scale(img, (128, 128))
    protagonista_andando_superficie.append(img)
    
# Protagonista pulando
for imagem in range(1, 9):
    img = pygame.image.load(f'assets/protagonista/pulo/owlet_jump{imagem}.png').convert_alpha()
    # Redimensionando para o pulo.
    img = pygame.transform.scale(img, (128, 128))
    protagonista_pulando_superficie.append(img)
    

# Protagonista atacando
for imagem in range(1, 7):
    img = pygame.image.load(f'assets/protagonista/ataque/owlet_attack{imagem}.png').convert_alpha()

# RETÂNGULO DE COLISÃO DO PROTAGONISTA
protagonista_superficies = protagonista_andando_superficie[protagonista_index]
protagonista_retangulo = protagonista_superficies.get_rect(midbottom = (100, 470))
protagonista_gravidade = 0


# CRIA O RELÓGIO QUE CONTROLA O FPS
relogio = pygame.time.Clock()

# CRIA O LOOP PRINCIPAL DO JOGO
while True:

    # IMPLEMENTA OS EVENTOS PRESENTES NO JOGO
    for evento in pygame.event.get():

        # FECHA A JANELA DO JOGO
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        # CONTROLA O PULO DO PROTAGONISTA
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and protagonista_retangulo.bottom >= 470:
                protagonista_gravidade = -20



    # FAZ OS ELEMENTOS APARECEREM NA TELA
    tela.blit(plano_fundo, (0,0))

    # CHAMA A ANIMAÇÃO DO PROTAGONISTA
    protagonista_gravidade += 1
    protagonista_retangulo.y += protagonista_gravidade
    if protagonista_retangulo.bottom >= 470: protagonista_retangulo.bottom = 470
    animacao_protagonista()
    

    # ATUALIZA A TELA COM O CONTEÚDO
    pygame.display.update()

    # QUANTIDADE DE FRAMES POR SEGUNDO
    relogio.tick(60)