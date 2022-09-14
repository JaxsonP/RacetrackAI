
from turtle import back
import pygame
import random
import math

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

def generateTrack (w, h):

	track = []
	link_history = []
	links = []
	iterations = 0
	for y in range(h): # initializing links and track

		track.append([])
		for x in range(w):
			track[y].append(0)

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
			print(f"\nends: {ends[0].toString()}, {ends[1].toString()}")
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


	return links

if __name__ == "__main__":
	print("\n\n\n")

	w = 10
	h = 7
	scale = 50

	links = generateTrack(w, h)
	
	#[print(row) for row in track]
	#[print(f"({link.x1}, {link.y1}) -> ({link.x2}, {link.y2})") for link in links]
	
	pygame.init()
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

	pygame.quit()