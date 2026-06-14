"""
Professional Snake game using Pygame

Run: python "19_github copilot.py"
Controls: Arrow keys or WASD to move, P to pause, Esc to quit.
"""
import os
import random
import sys

try:
	import pygame
except Exception:
	print("Pygame is required. Install with: pip install pygame")
	raise


BASE_DIR = os.path.dirname(__file__)
HIGHSCORE_PATH = os.path.join(BASE_DIR, "highscore.txt")

CELL = 20
GRID_W = 32  # 640 / 20
GRID_H = 24  # 480 / 20
WIDTH = GRID_W * CELL
HEIGHT = GRID_H * CELL

BLACK = (10, 10, 10)
DARK = (18, 18, 30)
WHITE = (240, 240, 240)
GREEN = (46, 204, 64)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
BLUE = (52, 152, 219)


def load_highscore():
	try:
		with open(HIGHSCORE_PATH, "r") as f:
			return int(f.read().strip() or 0)
	except Exception:
		return 0


def save_highscore(score: int):
	try:
		with open(HIGHSCORE_PATH, "w") as f:
			f.write(str(score))
	except Exception:
		pass


def draw_text(surf, text, size, pos, color=WHITE, center=False):
	font = pygame.font.SysFont("consolas", size)
	r = font.render(text, True, color)
	if center:
		rect = r.get_rect(center=pos)
	else:
		rect = r.get_rect(topleft=pos)
	surf.blit(r, rect)


class SnakeGame:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Snake — Python")
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()
		self.reset()
		self.state = "MENU"

	def reset(self):
		self.snake = [(GRID_W // 2, GRID_H // 2), (GRID_W // 2 - 1, GRID_H // 2), (GRID_W // 2 - 2, GRID_H // 2)]
		self.direction = (1, 0)
		self.next_dir = self.direction
		self.spawn_food()
		self.score = 0
		self.highscore = load_highscore()
		self.base_delay = 120  # ms between moves
		self.last_move = pygame.time.get_ticks()
		self.running = True
		# state is managed by caller (MENU, PLAYING, PAUSED, GAMEOVER)

	def spawn_food(self):
		while True:
			self.food = (random.randrange(GRID_W), random.randrange(GRID_H))
			if self.food not in self.snake:
				break

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				if event.key in (pygame.K_ESCAPE,):
					self.running = False
				if self.state == "MENU":
					if event.key in (pygame.K_RETURN, pygame.K_SPACE):
						self.reset()
						self.state = "PLAYING"
				elif self.state == "PLAYING":
					if event.key in (pygame.K_p,):
						self.state = "PAUSED"
					elif event.key in (pygame.K_UP, pygame.K_w):
						self.set_direction((0, -1))
					elif event.key in (pygame.K_DOWN, pygame.K_s):
						self.set_direction((0, 1))
					elif event.key in (pygame.K_LEFT, pygame.K_a):
						self.set_direction((-1, 0))
					elif event.key in (pygame.K_RIGHT, pygame.K_d):
						self.set_direction((1, 0))
				elif self.state == "PAUSED":
					if event.key in (pygame.K_p, pygame.K_RETURN, pygame.K_SPACE):
						self.state = "PLAYING"
				elif self.state == "GAMEOVER":
					if event.key in (pygame.K_RETURN, pygame.K_SPACE):
						self.reset()
						self.state = "PLAYING"

	def set_direction(self, d):
		# prevent reversing directly
		if (d[0] * -1, d[1] * -1) == self.direction:
			return
		self.next_dir = d

	def update(self):
		if self.state != "PLAYING":
			return
		now = pygame.time.get_ticks()
		# speed up as score increases
		delay = max(40, self.base_delay - (self.score // 5) * 6)
		if now - self.last_move < delay:
			return
		self.last_move = now
		self.direction = self.next_dir
		head = self.snake[0]
		new = ((head[0] + self.direction[0]) % GRID_W, (head[1] + self.direction[1]) % GRID_H)
		if new in self.snake:
			self.state = "GAMEOVER"
			if self.score > self.highscore:
				self.highscore = self.score
				save_highscore(self.highscore)
			return
		self.snake.insert(0, new)
		if new == self.food:
			self.score += 1
			self.spawn_food()
		else:
			self.snake.pop()

	def draw_grid(self):
		for x in range(0, WIDTH, CELL):
			pygame.draw.line(self.screen, (30, 30, 40), (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, CELL):
			pygame.draw.line(self.screen, (30, 30, 40), (0, y), (WIDTH, y))

	def draw(self):
		self.screen.fill(DARK)
		# play area border
		pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, HEIGHT))

		# grid subtle
		self.draw_grid()

		# food
		fx, fy = self.food
		pygame.draw.rect(self.screen, RED, (fx * CELL + 2, fy * CELL + 2, CELL - 4, CELL - 4), border_radius=4)

		# snake
		for i, (sx, sy) in enumerate(self.snake):
			rect = pygame.Rect(sx * CELL + 1, sy * CELL + 1, CELL - 2, CELL - 2)
			if i == 0:
				pygame.draw.rect(self.screen, YELLOW, rect, border_radius=6)
			else:
				pygame.draw.rect(self.screen, GREEN, rect, border_radius=6)

		# HUD
		draw_text(self.screen, f"Score: {self.score}", 18, (8, 8), WHITE)
		draw_text(self.screen, f"High: {self.highscore}", 18, (WIDTH - 110, 8), BLUE)

		if self.state == "MENU":
			draw_text(self.screen, "Snake", 48, (WIDTH // 2, HEIGHT // 2 - 40), WHITE, center=True)
			draw_text(self.screen, "Press Enter or Space to start", 20, (WIDTH // 2, HEIGHT // 2 + 10), WHITE, center=True)
			draw_text(self.screen, "Arrows / WASD to move — P to pause", 16, (WIDTH // 2, HEIGHT // 2 + 40), WHITE, center=True)
		elif self.state == "PAUSED":
			draw_text(self.screen, "Paused", 42, (WIDTH // 2, HEIGHT // 2), WHITE, center=True)
			draw_text(self.screen, "Press P/Enter/Space to resume", 18, (WIDTH // 2, HEIGHT // 2 + 36), WHITE, center=True)
		elif self.state == "GAMEOVER":
			draw_text(self.screen, "Game Over", 44, (WIDTH // 2, HEIGHT // 2 - 20), RED, center=True)
			draw_text(self.screen, f"Score: {self.score}  High: {self.highscore}", 22, (WIDTH // 2, HEIGHT // 2 + 16), WHITE, center=True)
			draw_text(self.screen, "Press Enter/Space to play again", 18, (WIDTH // 2, HEIGHT // 2 + 48), WHITE, center=True)

		pygame.display.flip()

	def run(self):
		while self.running:
			self.handle_events()
			self.update()
			self.draw()
			self.clock.tick(60)


def main():
	game = SnakeGame()
	game.run()
	pygame.quit()


if __name__ == "__main__":
	main()


