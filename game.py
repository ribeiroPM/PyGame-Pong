from pygame.locals import *
import pygame
from pc import Pc

class Pad:
	def __init__(self, pos_x, screen_height, color):
		self.pos_x = pos_x
		self.pos_y = int(screen_height/2-100)
		self.color = color
		self.speed = 10
		self.screen_height = screen_height
		self.size = 200
		self.rect = None

	def draw(self, screen):
		self.rect =pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, 20, self.size))

	def update(self, command):
		if command == 1 and self.pos_y > 10: # Movimento para Cima
			self.pos_y -= self.speed
		elif command == 2 and self.pos_y < self.screen_height-10-self.size: # Movimento para Baixo
			self.pos_y += self.speed

	def get_points(self):
		return [[self.pos_x, y] for y in range(self.pos_y, self.pos_y+self.size+1)]


def reset_ball():
	return 10, 10, [screen_x/2-10, screen_y/2-10]

def ball_scape_pad(ball_pos_x, pad1_pos_x, pad2_pos_x, ball_size):
	# Verifica se a bola passou pela palheta sem tocar na superfície frontal
	result = None
	if ball_pos_x < pad1_pos_x + ball_size//2:
		result = 2 # Se passou do valo direito, ponto para o lado esquerdo e vice versa
	if	ball_pos_x > pad2_pos_x - ball_size//2:
		result = 1
	return result


# Iniciando o pygame e demais funções
pygame.init()
pygame.display.set_caption("Pong")

# Fonte para exibir a pontuação
font = pygame.font.Font(None, 400)

# Tamanho da janela
screen_x = 1080
screen_y = 720

# Cores a serem usadas
screen_fg = (22, 31, 101)
ball_color = (222, 2, 49)
pad_color = (255, 255, 255)
white = (255, 255, 255)
score_color = (84, 44, 181)

# Definindo informações da janela
screen = pygame.display.set_mode((screen_x, screen_y))

# Instanciando as Palhetas
pad1 = Pad(10, screen_y, pad_color)
pad2 = Pad(screen_x-30, screen_y, pad_color)

# Movimentação do pad pelo Computador
pc = Pc(10, screen_y, screen_x, 200, 7)
pc2 = Pc(10, screen_y, screen_x, 200, 5)

# Definindo a bolinha
ball_pos = [screen_x/2-10, screen_y/2-10]
ball_size = 20
ball_speed_x = 10
ball_speed_y = 10

# Definindo o limitador de quadros
clock = pygame.time.Clock()

# Pontuação
score_1 = 0
score_2 = 0

# Escolhe se sera 1x1 ou 1xPc
game_mode = 2 # 1: 1x1 / 2: 1xPc / 3: PcxPc (Teste)

run = True
while run:
	# Checagem de eventos
	for event in pygame.event.get():
		if event.type == QUIT:
			run = False

	### Movimentando as Palhetas
	# Palheta 1
	if game_mode == 1 or game_mode == 2:
		if pygame.key.get_pressed()[K_w]:
			pad1.update(1)
		elif pygame.key.get_pressed()[K_s]:
			pad1.update(2)
	# Palheta 2
	if game_mode == 1:
		if pygame.key.get_pressed()[K_o]:
			pad2.update(1)
		elif pygame.key.get_pressed()[K_l]:
			pad2.update(2)
	if game_mode == 2 or game_mode == 3:
		pad2.update(pc.moviment(ball_pos[1], ball_pos[0], pad2.pos_y))
	if game_mode == 3:
		pad1.update(pc2.moviment(ball_pos[1], ball_pos[0], pad1.pos_y))

	# Limpando a tela
	screen.fill(screen_fg)

	# Divisor de tela
	pygame.draw.rect(screen, white, (screen_x//2, 0, 5, screen_y))
	
	# Desenhando as palhetas na tela
	pad1.draw(screen)
	pad2.draw(screen)

	# Atualizando posição da bolinha
	ball_pos[0] += ball_speed_x
	ball_pos[1] += ball_speed_y

	# Exibe a pontuação
	score_text1 = font.render(f"{score_1:0>2}", True, score_color)
	score_text2 = font.render(f"{score_2:0>2}", True, score_color)
	screen.blit(score_text1, (screen_x // 2 - 400, screen_y // 2 - 140))
	screen.blit(score_text2, (screen_x // 2 + 105, screen_y // 2 - 140))

	# Desenhando a bolinha
	ball_circle = pygame.draw.circle(screen, ball_color, ball_pos, ball_size)

	## Atualizando direção da bolinha
	# Eixo y
	if ball_pos[1] > screen_y - ball_size or ball_pos[1] < 0 + ball_size:
		ball_speed_y *= -1
	# Eixo x
	if pad1.rect.colliderect(ball_circle) or pad2.rect.colliderect(ball_circle):
		ball_speed_x *= -1

	# Resetando posição da bolinha e definindo pontuação
	if ball_pos[0] > screen_x - ball_size or ball_scape_pad(ball_pos[0], pad1.pos_x, pad2.pos_x, ball_size) == 1:
		ball_speed_x, ball_speed_y, ball_pos = reset_ball()
		score_1 += 1
	elif ball_pos[0] < 0 + ball_size or ball_scape_pad(ball_pos[0], pad1.pos_x, pad2.pos_x, ball_size) == 2:
		ball_speed_x, ball_speed_y, ball_pos = reset_ball()
		score_2 += 1

	# Definindo a quantidade de quadros po segundo (FPS)
	clock.tick(60)

	# Atualizando a tela
	pygame.display.update()

pygame.quit()