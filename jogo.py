import pygame
from sys import exit
from random import randint

# DEFINE A ANIMAÇÃO DO PROTAGONISTA
def animacao_protagonista():
    global protagonista_superficies, protagonista_index

    # Animação do personagem andando no chão, pulando e atacando.
    # Só ataca quando está no chão.
    if(protagonista_retangulo.bottom < 440):
        protagonista_superficies = protagonista_pulando_superficie[int(protagonista_index)]
    else: 
        protagonista_index += 0.1
        if protagonista_index >= len(protagonista_andando_superficie): protagonista_index = 0
        protagonista_superficies = protagonista_andando_superficie[int(protagonista_index)]

    # Faz o owlet aparecer na tela.
    tela.blit(protagonista_superficies, protagonista_retangulo)


# DEFINE O MOVIMENTO DOS OBSTÁCULOS
def obstaculos(lista_obstaculos):
    # Confere se há algum obstáculo na lista.
    if lista_obstaculos:
        for obstaculo_retangulo in lista_obstaculos:

            # Se for no chão, faz aparecer os spikes.
            if obstaculo_retangulo.bottom == 490: 
                tela.blit(spikes_superficie, obstaculo_retangulo)
                obstaculo_retangulo.x -= 7
            # Se for no ar, aparece as pedras voadoras.
            else: 
                tela.blit(pedras_superficie, obstaculo_retangulo)
                obstaculo_retangulo.x -= 5

        lista_obstaculos = [obstaculo for obstaculo in lista_obstaculos if obstaculo.x > -100]
        return lista_obstaculos
    
    else:
        return []
    

# CRIA A COLISÃO DOS OBJETOS COM O PROTAGONISTA
def colisao(protagonista, obstaculos):
    if obstaculos:
        for obstaculo_retangulo in obstaculos:
            if protagonista.colliderect(obstaculo_retangulo): return False
    return True




# INICIALIZA O PYGAME
pygame.init()

# CRIANDO A TELA DO JOGO E DEFININDO SEU NOME E TAMANHO
tamanho_tela = (960, 540)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("OWLET ULTRA ADVENTURES")

# IMPORTANDO ARQUIVOS DE IMAGEM DO JOGUIN
plano_fundo = pygame.image.load('assets/fundo/fundo-sem-camadas.png').convert()

# IMPORTANDO ARQUIVOS DE FONTES
youngserif_font = pygame.font.Font('assets/fonts/YoungSerif-Regular.ttf', 80)
youngserif_peq_font = pygame.font.Font('assets/fonts/YoungSerif-Regular.ttf', 40)

# DEIXANDO OS TAMANHOS DE ACORDO COM O TAMANHO DA TELA
plano_fundo = pygame.transform.scale(plano_fundo, tamanho_tela)


# VERIFICA SE O JOGO ESTÁ RODANDO 
jogo_rodando = True

# CARREGANDO IMAGENS DE ANIMAÇÃO DO PERSONAGEM
protagonista_index = 0
protagonista_andando_superficie = []
protagonista_pulando_superficie = []
protagonista_ataque_superficie = []

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
    # Redimensionando para o ataque.
    img = pygame.transform.scale(img, (128, 128))
    protagonista_ataque_superficie.append(img)

# Carrega o projétil que o protagonista atira.
projetil_frames = []
projetil_index = 0
for imagem in range(1, 5):
    img = pygame.image.load(f'assets/protagonista/projetil_ataque/owl_projetil{imagem}.png').convert_alpha()
    projetil_frames.append(img)

# RETÂNGULO DE COLISÃO DO PROTAGONISTA
protagonista_superficies = protagonista_andando_superficie[protagonista_index]
protagonista_retangulo = protagonista_superficies.get_rect(midbottom = (100, 450))
protagonista_retangulo = protagonista_retangulo.inflate(-36, -62)
protagonista_gravidade = 0





# CARREGA AS IMAGENS DOS OBSTÁCULOS
# Spikes
spikes_frames_superficie = []
spikes_index = 0
for imagem in range(1, 4):
    img = pygame.image.load(f'assets/boss/ataque-chao/boss_groundslam{imagem}.png').convert_alpha()
    # Redimensionando para ficar do mesmo tamanho das pedras.
    img = pygame.transform.scale(img, (108, 108))
    spikes_frames_superficie.append(img)

# Pedras voadoras
pedras_index = 0
pedras_superficie = pygame.image.load(f'assets/boss/ataque-pedra/pedracast1.png').convert_alpha()
pedras_superficie = pygame.transform.scale(pedras_superficie, (84, 84))

spikes_superficie = spikes_frames_superficie[spikes_index]
lista_retang_obstaculos = []


# CRIA O TIMER DOS OBSTÁCULOS
obstaculos_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstaculos_timer, 900)

spikes_timer = pygame.USEREVENT + 2
pygame.time.set_timer(spikes_timer, 320)

pedras_timer = pygame.USEREVENT + 3
pygame.time.set_timer(pedras_timer, 10)



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

        if jogo_rodando:
            jogo_rodando = True
            # CONTROLA O PULO DO PROTAGONISTA
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and protagonista_retangulo.bottom >= 440:
                    protagonista_gravidade = -19

            if evento.type == pygame.KEYUP:
                protagonista_superficies = protagonista_andando_superficie[int(protagonista_index)]

         # CRIA EVENTOS REFERENTES AOS OBSTÁCULOS
            if evento.type == obstaculos_timer:
                if randint(0, 2):
                    # Retângulo dos spikes.
                    spikes_retangulo = spikes_superficie.get_rect(bottomright = (randint(960, 1000), 490))
                    spikes_retangulo = spikes_retangulo.inflate(-62, 0)
                    lista_retang_obstaculos.append(spikes_retangulo)
                    # Retângulo das pedras.
                    pedras_retangulo = pedras_superficie.get_rect(bottomright = (randint(960, 1200), 188))
                    pedras_retangulo = pedras_retangulo.inflate(-5, -5)
                    lista_retang_obstaculos.append(pedras_retangulo)
        
            if evento.type == spikes_timer:
                if spikes_index == 0: spikes_index = 1
                else: spikes_index = 0
                spikes_superficie = spikes_frames_superficie[spikes_index]

            if evento.type == pedras_timer:
                if pedras_index == 0: pedras_index = 1
                else: pedras_index = 0
                pedras_superficie = pedras_superficie

        else:
            jogo_rodando = False


    if jogo_rodando:
        # FAZ OS ELEMENTOS APARECEREM NA TELA
        tela.blit(plano_fundo, (0,0))

        # CHAMA A ANIMAÇÃO DO PROTAGONISTA
        protagonista_gravidade += 0.9
        protagonista_retangulo.y += protagonista_gravidade
        if protagonista_retangulo.bottom >= 440: protagonista_retangulo.bottom = 440
        animacao_protagonista()

        # CHAMA A FUNÇÃO DOS OBSTÁCULOS SE MOVENDO
        lista_retang_obstaculos = obstaculos(lista_retang_obstaculos)
    
        # FAZ AS COLISOES ACONTECEREM
        jogo_rodando = colisao(protagonista_retangulo, lista_retang_obstaculos)

    # TELA DE GAME OVER
    else:
        tela.blit(plano_fundo, (0,0))
        # texto de game over
        gameover_texto = youngserif_font.render(f'game over', False, (255, 255, 255))
        gameover_texto_retangulo = gameover_texto.get_rect(center = (480, 150))
        tela.blit(gameover_texto, gameover_texto_retangulo)
        # texto de 'tente novamente'
        restart_texto = youngserif_peq_font.render(f'aperte ESPAÇO para jogar novamente', False, (255, 255, 255))
        restart_texto_retangulo = restart_texto.get_rect(center = (480, 250))
        tela.blit(restart_texto, restart_texto_retangulo)
        


    # ATUALIZA A TELA COM O CONTEÚDO
    pygame.display.update()

    # QUANTIDADE DE FRAMES POR SEGUNDO
    relogio.tick(60)