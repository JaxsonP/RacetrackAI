import pygame
import random

def hamiltonian_vector_field (w, h):

	w = int(w)
	h = int(h)
	print('\n\n\n> creating ham field that is ' + str(w) + ' by ' + str(h))

	if w % 2 != 0 and h % 2 != 0: # checking for double odds
		return False

	field = [None for i in range(h)] # generating zigzag
	for y in range(h):
		if y % 2 == 0:
			field[y] = [1 for i in range(w)]
			field[y][w - 1] = 2
		else:
			field[y] = [3 for i in range(w)]
			field[y][0] = 2

	
	cur = (0, 0)
	last_cur = cur
	end = (0, 0)
	while True: # identifying endpoint
		try:
			if field[cur[1]][cur[0]] == 0:
				last_cur = cur
				cur = (cur[0], cur[1] - 1)
			elif field[cur[1]][cur[0]] == 1:
				last_cur = cur
				cur = (cur[0] + 1, cur[1])
			elif field[cur[1]][cur[0]] == 2:
				last_cur = cur
				cur = (cur[0], cur[1] + 1)
			elif field[cur[1]][cur[0]] == 3:
				last_cur = cur
				cur = (cur[0] - 1, cur[1])
		except (IndexError):
			end = last_cur
			field[end[1]][end[0]] = 4
			break
	
	for i in range(0):
		
		for y in range(len(field)): # relocating the end
			for x in range(len(field[y])):
				if field[y][x] == 4:
					end = (x, y)
					print('found end at ' + str(end))
	
		potential_neighbors = [(end[0], end[1] - 1), (end[0] + 1, end[1]), (end[0], end[1] + 1), (end[0] - 1, end[1])] # getting potential neighbors
		neighbors = []
		for neighbor in potential_neighbors:
			if neighbor[0] >= 0 and neighbor[0] < w and neighbor[1] >= 0 and neighbor[1] < h: # weeding out out of bounds neighbors
				if field[neighbor[1]][neighbor[0]] == 0 and end == (neighbor[0], neighbor[1] - 1): # excluding prior cell
					continue
				elif field[neighbor[1]][neighbor[0]] == 1 and end == (neighbor[0] + 1, neighbor[1]):
					continue
				elif field[neighbor[1]][neighbor[0]] == 2 and end == (neighbor[0], neighbor[1] + 1):
					continue
				elif field[neighbor[1]][neighbor[0]] == 3 and end == (neighbor[0] - 1, neighbor[1]):
					continue
				neighbors.append(neighbor)
		
		to_switch = random.choice(neighbors) # choosing a neighbor

		next_end = (0, 0)
		if field[to_switch[1]][to_switch[0]] == 0: # locating end
			next_end = (to_switch[0], to_switch[1] - 1)
		elif field[to_switch[1]][to_switch[0]] == 1:
			next_end = (to_switch[0] + 1, to_switch[1])
		elif field[to_switch[1]][to_switch[0]] == 2:
			next_end = (to_switch[0], to_switch[1] + 1)
		elif field[to_switch[1]][to_switch[0]] == 3:
			next_end = (to_switch[0] - 1, to_switch[1])

		if to_switch[1] < end[1]: # connecting end and to_switch
			field[to_switch[1]][to_switch[0]] = 2
		elif to_switch[0] > end[0]:
			field[to_switch[1]][to_switch[0]] = 3
		elif to_switch[1] > end[1]:
			field[to_switch[1]][to_switch[0]] = 0
		elif to_switch[0] < end[0]:
			field[to_switch[1]][to_switch[0]] = 1

		cur = end
		end = next_end
		field[end[1]][end[0]] = 4 # marking end

		next_cur = cur
		last_cur
		while True: # redirecting affected path
			found = False
			try:
				if field[cur[1] - 1][cur[0]] == 2 and last_cur != (cur[0], cur[1] - 1):
					next_cur = (cur[0], cur[1] - 1)
					field[cur[1]][cur[0]] = 0
					found = True 
			except: pass
			try:
				if field[cur[1]][cur[0] + 1] == 3 and last_cur != (cur[0] + 1, cur[1]):
					next_cur = (cur[0] + 1, cur[1])
					field[cur[1]][cur[0]] = 1
					found = True
			except: pass
			try:
				if field[cur[1] + 1][cur[0]] == 0 and last_cur != (cur[0], cur[1] + 1):
					next_cur = (cur[0], cur[1] + 1)
					field[cur[1]][cur[0]] = 2
					found = True
			except: pass
			try:
				if field[cur[1]][cur[0] - 1] == 1 and last_cur != (cur[0] - 1, cur[1]):
					next_cur = (cur[0] - 1, cur[1])
					field[cur[1]][cur[0]] = 3
					found = True
			except: pass
			if found == False: # redirecting the last cell
				try:
					if field[cur[1] - 1][cur[0]] == 4:
						field[cur[1]][cur[0]] = 0
				except: pass
				try:
					if field[cur[1]][cur[0] + 1] == 4:
						field[cur[1]][cur[0]] = 1
				except: pass
				try:
					if field[cur[1] + 1][cur[0]] == 4:
						field[cur[1]][cur[0]] = 2
				except: pass
				try:
					if field[cur[1]][cur[0] - 1] == 4:
						field[cur[1]][cur[0]] = 3
				except: pass
				break
			else:
				last_cur = cur
				cur = next_cur
		
		start = end
		cur = end
		next_cur = cur
		last_cur
		while True: # reversing everything
			found = False
			try:
				if field[cur[1] - 1][cur[0]] == 2 and last_cur != (cur[0], cur[1] - 1):
					next_cur = (cur[0], cur[1] - 1)
					field[cur[1]][cur[0]] = 0
					found = True 
			except: pass
			try:
				if field[cur[1]][cur[0] + 1] == 3 and last_cur != (cur[0] + 1, cur[1]):
					next_cur = (cur[0] + 1, cur[1])
					field[cur[1]][cur[0]] = 1
					found = True
			except: pass
			try:
				if field[cur[1] + 1][cur[0]] == 0 and last_cur != (cur[0], cur[1] + 1):
					next_cur = (cur[0], cur[1] + 1)
					field[cur[1]][cur[0]] = 2
					found = True
			except: pass
			try:
				if field[cur[1]][cur[0] - 1] == 1 and last_cur != (cur[0] - 1, cur[1]):
					next_cur = (cur[0] - 1, cur[1])
					field[cur[1]][cur[0]] = 3
					found = True
			except: pass
			if found == False: # found the end
				end = cur
				break
			else:
				last_cur = cur
				cur = next_cur
		field[end[1]][end[0]] = 4
		print('new end: ' + str(end))
		print('> Finished backbite #' + str(i))

	print('> Done')
	return field

width = 450
height = 300
scale = 50

pygame.init()
screen = pygame.display.set_mode([width, height])
running = True
vf = hamiltonian_vector_field(width / scale, height / scale)
while running:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	screen.fill((240, 240, 240))

	for y in range(len(vf)):
		for x in range(len(vf[y])):
			pygame.draw.rect(screen, (200, 200, 200), (x * 50, y * 50, x * 50 + 50, y * 50 + 50), 1)

			if vf[y][x] == 0:
				pygame.draw.line(screen, (0, 0, 0), (50 * x + 25, 50 * y + 25), (50 * x + 25, 50 * y))
			elif vf[y][x] == 1:
				pygame.draw.line(screen, (0, 0, 0), (50 * x + 25, 50 * y + 25), (50 * x + 50, 50 * y + 25))
			elif vf[y][x] == 2:
				pygame.draw.line(screen, (0, 0, 0), (50 * x + 25, 50 * y + 25), (50 * x + 25, 50 * y + 50))
			elif vf[y][x] == 3:
				pygame.draw.line(screen, (0, 0, 0), (50 * x + 25, 50 * y + 25), (50 * x, 50 * y + 25))
			
	#pygame.quit()
	pygame.display.flip()

pygame.quit()