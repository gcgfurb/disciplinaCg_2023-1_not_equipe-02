import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Tamanho da janela
WIDTH = 800
HEIGHT = 600

# Configurações do cubo
cube_vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)
cube_faces = (
    (0, 1, 2, 3),  # Face 0
    (3, 2, 7, 6),  # Face 1
    (6, 7, 5, 4),  # Face 2
    (4, 5, 1, 0),  # Face 3
    (1, 5, 7, 2),  # Face 4
    (4, 0, 3, 6)   # Face 5
)
cube_faces_textures = (
    (0, 0),
    (1, 0),
    (1, 1),
    (0, 1)
)

# Carrega as imagens como texturas e redimensiona
def load_textures(filenames):
    texture_ids = []

    for filename in filenames:
        surface = pygame.image.load(filename)

        # Redimensiona a imagem para as novas dimensões
        surface = pygame.transform.scale(surface, (200, 200))

        texture_data = pygame.image.tostring(surface, "RGB", True)
        width = surface.get_width()
        height = surface.get_height()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

        texture_ids.append(texture_id)

    return texture_ids

# Inicialização do Pygame
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)

# Configurações de projeção
glViewport(0, 0, WIDTH, HEIGHT)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)

# Carrega as texturas para cada face do cubo
texture_filenames = [
    "imagem1.jpg",  # Face 0
    "imagem2.jpg",  # Face 1
    "imagem3.jpg",  # Face 2
    "imagem4.jpg",  # Face 3
    "imagem5.jpg",  # Face 4
    "imagem6.jpg"   # Face 5
]
texture_ids = load_textures(texture_filenames)

# Posição inicial do cubo
cube_x = 0
cube_y = 0

# Variáveis de controle de movimento do cubo
move_left = False
move_right = False
move_up = False
move_down = False
zoom_in = False
zoom_out = False

# Ângulo de rotação do cubo (em graus)
rotation_angle = 0

# Desabilita a iluminação
glDisable(GL_LIGHTING)

# Loop principal do jogo
clock = pygame.time.Clock()
running = True
current_texture_index = 0  # Índice da textura atual
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Tratamento de eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_right = True
            elif event.key == pygame.K_d:
                move_left = True
            elif event.key == pygame.K_w:
                move_up = True
            elif event.key == pygame.K_s:
                move_down = True
            elif event.key == pygame.K_q:
                zoom_in = True
            elif event.key == pygame.K_e:
                zoom_out = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_right = False
            elif event.key == pygame.K_d:
                move_left = False
            elif event.key == pygame.K_w:
                move_up = False
            elif event.key == pygame.K_s:
                move_down = False
            elif event.key == pygame.K_q:
                zoom_in = False
            elif event.key == pygame.K_e:
                zoom_out = False

    # Atualiza a posição do cubo de acordo com as teclas pressionadas
    if move_left:
        cube_x -= 0.1
    if move_right:
        cube_x += 0.1
    if move_up:
        cube_y += 0.1
    if move_down:
        cube_y -= 0.1

    # Limpa o buffer de cor e o buffer de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Posiciona a câmera para visualizar o cubo
    gluLookAt(0, 0, -10, 0, 0, 0, 0, 1, 0)

    # Atualiza a rotação do cubo com base no movimento do mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    glTranslatef(cube_x, cube_y, 0)
    glRotatef(mouse_x * 0.5, 0, 1, 0)
    glRotatef(mouse_y * 0.5, 1, 0, 0)
    glTranslatef(-cube_x, -cube_y, 0)

    # Renderiza o cubo com as texturas
    glEnable(GL_TEXTURE_2D)
    for i, surface in enumerate(cube_faces):
        glBindTexture(GL_TEXTURE_2D, texture_ids[i])  # Seleciona a textura correta para a face atual
        glBegin(GL_QUADS)
        for j in range(4):
            vertex = surface[j]
            texture_coord = cube_faces_textures[j]

            glTexCoord2fv(texture_coord)
            glVertex3fv(
                (cube_vertices[vertex][0] + cube_x, cube_vertices[vertex][1] + cube_y, cube_vertices[vertex][2]))
        glEnd()
    glDisable(GL_TEXTURE_2D)

    # Atualiza o ângulo de rotação
    rotation_angle += 1

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

    # Atualiza o índice da textura atual para a próxima textura
    current_texture_index = (current_texture_index + 1) % len(texture_filenames)
    texture_ids = load_textures(texture_filenames)  # Recarrega as texturas

# Encerra o Pygame
pygame.quit()
