
import pygame
import random
import math
from PIL import Image, ImageDraw

class Node:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def inBounds (self, w, h):
		return self.x >= 0 and self.x < w and self.y >= 0 and self.y < h

	def toString (self):
		return f"({self.x}, {self.y})"

class Link:
	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

	def reverse (self):
		return Link(self.x2, self.y2, self.x1, self.x2)
	
	def contains (self, n):
		return (self.x1 == n.x and self.y1 == n.y) or (self.x2 == n.x and self.y2 == n.y)

	def toString (self):
		return f"({self.x1}, {self.y1}) -> ({self.x2}, {self.y2})"

def generateTrack (w, h, scale):

	links = []
	iterations = 0
	for y in range(h): # initializing links

		for x in range(w - 1):
			links.append(Link(x, y, x + 1, y))

		if y < h - 1 and y % 2 == 0:
			links.append(Link(0, y, 0, y + 1))
		elif y < h - 1:
			links.append(Link(w - 1, y, w - 1, y + 1))


	def findEnds (): # finds and returns all non-looping nodes
	
		ends = []
		for y in range(h):
			for x in range(w):

				connected_nodes = 0
				for link in links:
					if (link.x1 == x and link.y1 == y) or (link.x2 == x and link.y2 == y):
						connected_nodes += 1
				
				if connected_nodes == 1:
					ends.append(Node(x, y))
				elif connected_nodes == 0:
					raise ValueError('While checking end nodes, found a node with no links')	
		return ends


	# the backbite <<<<<<
	while True:

		ends = findEnds()

		if iterations > 1000 and math.dist((ends[0].x, ends[0].y), (ends[1].x, ends[1].y)) <= 1:
			# print(f"\nends: {ends[0].toString()}, {ends[1].toString()}")
			break
		
		# choosing an end node
		end_node = random.choice(ends)

		# finding the end node's link
		end_link = None
		for link in links:
			if link.contains(end_node):
				end_link = link
		
		# gathering neighbor cells of the end node
		potential_neighbors = []
		potential_neighbors.append(Node(end_node.x, end_node.y - 1))
		potential_neighbors.append(Node(end_node.x + 1, end_node.y))
		potential_neighbors.append(Node(end_node.x, end_node.y + 1))
		potential_neighbors.append(Node(end_node.x - 1, end_node.y))

		# filtering and choosing neighbor cells
		neighbors = []
		for node in potential_neighbors:
			if (not end_link.contains(node)) and node.inBounds(w, h):
				neighbors.append(node)

		# choosing the backbite node
		backbite_node = random.choice(neighbors)
		# gathering its links
		potential_backbite_links = []
		for link in links:
			if link.contains(backbite_node):
				potential_backbite_links.append(link)

		link_to_remove = None
		for link in potential_backbite_links:

			last_node = backbite_node
			current_link = link

			while True:
				if current_link.contains(end_node):
					link_to_remove = link
					break

				if current_link.x1 == last_node.x and current_link.y1 == last_node.y:
					last_node = Node(current_link.x2, current_link.y2)
				else:
					last_node = Node(current_link.x1, current_link.y1)

				new_link = None
				for potential_link in links:
					if potential_link.contains(last_node) and potential_link != current_link:
						new_link = potential_link
						break
				
				if new_link == None:
					break
				
				current_link = new_link
				
		links.remove(link_to_remove)
		links.append(Link(end_node.x, end_node.y, backbite_node.x, backbite_node.y))
		iterations += 1

	ends = findEnds()

	# converting into a node array
	current_node = ends[1]
	last_node = Node(-1, -1)
	node_array = []

	while True:

		for link in links:
			if link.contains(current_node) and not link.contains(last_node):

				node_array.append(current_node)

				last_node = current_node
				if link.x1 == current_node.x and link.y1 == current_node.y:
					current_node = Node(link.x2, link.y2)
				else:
					current_node = Node(link.x1, link.y1)
				
				break
		if current_node.x == ends[0].x and current_node.y == ends[0].y:
			node_array.append(ends[0])
			node_array.append(ends[1])
			break
			
	# converting into array of cardinal directions (vector arry)
	vector_array = []
	last_direction = None
	for i in range(len(node_array) - 1):
		direction = None
		if node_array[i + 1].y < node_array[i].y: # north
			direction = 0
		elif node_array[i + 1].x > node_array[i].x: # east
			direction = 1
		elif node_array[i + 1].y > node_array[i].y: # south
			direction = 2
		elif node_array[i + 1].x < node_array[i].x: # west
			direction = 3
		else:
			raise ValueError('Couldnt parse node array')
		
		vector_array.append((direction, last_direction))
		last_direction = direction
	vector_array[0] = (vector_array[0][0], vector_array[-1][0])


	possible_start_nodes = []

	# drawing the track
	current_node = ends[1]
	img = Image.new('1', (w * scale, h * scale))
	draw = ImageDraw.Draw(img)
	for segment in vector_array:

		x = current_node.x
		y = current_node.y

		if (segment[0] == 0 or segment[0] == 2) and (segment[1] == 0 or segment[1] == 2): # |
			draw.rectangle((x * scale + scale / 4, y * scale, x * scale + 3 * scale / 4, y * scale + scale), fill=1)
			possible_start_nodes.append((Node(x, y), False))

		elif (segment[0] == 1 or segment[0] == 3) and (segment[1] == 1 or segment[1] == 3): # --
			draw.rectangle((x * scale, y * scale + scale / 4, x * scale + scale, y * scale + 3 * scale / 4), fill=1)
			possible_start_nodes.append((Node(x, y), True))

		elif (segment[0] == 0 and segment[1] == 3) or (segment[0] == 1 and segment[1] == 2): # L
			draw.pieslice([x * scale + scale / 4, y * scale - 3 * scale / 4, x * scale + 7 * scale / 4, y * scale + 3 * scale / 4], 90, 180, fill=1)
			draw.pieslice([x * scale + 3 * scale / 4, y * scale - scale / 4, x * scale + 5 * scale / 4, y * scale + scale / 4], 90, 180, fill=0)

		elif (segment[0] == 1 and segment[1] == 0) or (segment[0] == 2 and segment[1] == 3): # upside down L
			draw.pieslice([x * scale + scale / 4, y * scale + scale / 4, x * scale + 7 * scale / 4, y * scale + 7 * scale / 4], 180, 270, fill=1)
			draw.pieslice([x * scale + 3 * scale / 4, y * scale + 3 * scale / 4, x * scale + 5 * scale / 4, y * scale + 5 * scale / 4], 180, 270, fill=0)


		elif (segment[0] == 3 and segment[1] == 0) or (segment[0] == 2 and segment[1] == 1): # backwards upside down L
			draw.pieslice([x * scale - 3 * scale / 4, y * scale + scale / 4, x * scale + 3 * scale / 4, y * scale + 7 * scale / 4], 270, 0, fill=1)
			draw.pieslice([x * scale - scale / 4, y * scale +  + 3 * scale / 4, x * scale + scale / 4, y * scale + 5 * scale / 4], 270, 0, fill=0)


		elif (segment[0] == 0 and segment[1] == 1) or (segment[0] == 3 and segment[1] == 2): # backwards L
			draw.pieslice([x * scale - 3 * scale / 4, y * scale - 3 * scale / 4, x * scale + 3 * scale / 4, y * scale + 3 * scale / 4], 0, 90, fill=1)
			draw.pieslice([x * scale - scale / 4, y * scale - scale / 4, x * scale + scale / 4, y * scale + scale / 4], 0, 90, fill=0)

		if segment[0] == 0:
			current_node.y -= 1
		elif segment[0] == 1:
			current_node.x += 1
		if segment[0] == 2:
			current_node.y += 1
		elif segment[0] == 3:
			current_node.x -= 1

	#print([node.toString() for node in node_array])
	checkpoints = [(node.x * scale + scale / 2, node.y * scale + scale / 2) for node in node_array[:-1]]
	return img, random.choice(possible_start_nodes), checkpoints

if __name__ == "__main__":
	print("\n\n\n")

	w = 6
	h = 4
	scale = 100

	track, start, checkpoints = generateTrack(w, h, scale)
	track.save("track.png", format="PNG")
	print("done generating")
	
	"""pygame.init()
	screen = pygame.display.set_mode([w * scale, h * scale])
	running = True



	frame = 0
	while running:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		screen.fill((230, 230, 230))

		# draw links
		for link in links:
			pygame.draw.line(screen, (60, 60, 60), (link.x1 * scale + scale / 2, link.y1 * scale + scale / 2), (link.x2 * scale + scale / 2, link.y2 * scale + scale / 2), 8)

		# draw nodes
		for y in range(h):
			for x in range(w):
				pygame.draw.rect(screen, (30, 30, 30), (x * scale + scale / 3, y * scale + scale / 3, scale / 3, scale / 3), 0)
				
		#pygame.quit()
		pygame.display.flip()

	pygame.quit()"""