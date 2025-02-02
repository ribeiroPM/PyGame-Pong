class Pc:
	"""docstring for ClassName"""
	def __init__(self, speed, screen_height, screen_width, pad_size, dificulty):
		self.speed = speed
		self.pad_center = pad_size//2
		self.dificulty = dificulty # 8: Fácil/ 7: Médio/ 6: Impossível
		self.screen_x = screen_width

	def moviment(self, ball_pos_y, ball_pos_x, pad_pos_y):
		if (self.dificulty*100) - ball_pos_x < 0:
			if pad_pos_y < ball_pos_y:
				return 2
			if pad_pos_y > ball_pos_y:
				return 1
		