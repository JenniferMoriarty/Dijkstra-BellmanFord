#Timberborn Shortest Path Demonstration Program
#by J. Moriarty, Spring 2024
#Note: code for class graph, vertex, and dijkstra and bellman-ford algorithms adapted from Lysecky & Vahid Design and Analysis of Algorithms Textbook.
#Other code credited with links above algorithms used.


import operator
import pygame
import math
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Dijkstra!')
font = pygame.font.Font('freesansbold.ttf', 15)

#get user input for dijkstra vs bellman-ford! #note: replace this with mouse input eventually
choice = int(input("choose 1 for dijkstra, 2 for bellman-ford"))

#game setup
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
counting_time = pygame.time.get_ticks() - start_time
font = pygame.font.SysFont(None, 32)
counting_minutes = 0
counting_seconds = 0
counting_milliseconds = 0

#class beaver: little guys that run from one building to another
class beaver:
    def __init__(self, x, y):
        self.xpos = x
        self.ypos = y
        
    def draw(self):
        pygame.draw.circle(screen, (100, 50, 0), (self.xpos, self.ypos), 15)
        pygame.draw.circle(screen, (255,255,255), (self.xpos, self.ypos), 15, 2)
        
    def move(self, vertex):
        #credit for this section: https://gamedev.stackexchange.com/questions/198473/pygame-having-trouble-with-implementing-movement-with-vectors
        speed = 1
        #calculate direction vector
        dx = vertex[0] - self.xpos
        dy = vertex[1] - self.ypos
        distance = dist(self.xpos, self.ypos, vertex[0], vertex[1])
        
        if distance>2:
            #normalize direction vector
            dx /= distance
            dy /= distance
            
            self.xpos += dx * speed
            self.ypos += dy * speed
        if dist(self.xpos, self.ypos, vertex[0], vertex[1]) > 2:
            return 1
        else:
            return 0
        
        
zoti = beaver(100,100)

#class vertex: represents nodes or city buildings in Timberborn------------------------------------------
class Vertex:
    def __init__(self, label, x, y):
        self.label = label
        self.xpos = x
        self.ypos = y
        self.distance = 99999999
        self.pred_vertex = None
        self.text_surface = font.render(label, False, (255,255,255))
        
    def draw(self):
        pygame.draw.circle(screen, (200, 50, 50), (self.xpos, self.ypos),20)
        screen.blit(self.text_surface, (self.xpos-20, self.ypos-0))
        
    def xCoord(self):
        return self.xpos
    def yCoord(self):
        return self.ypos

#class Graph: represents the entire city (buildings and roads)------------------------------------------
class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}     
  
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []
        
    def add_directed_edge(self, from_vertex, to_vertex, weight = 1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)
        
    def add_undirected_edge(self, vertex_a, vertex_b, weight = 1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)
        
    def draw(self):
        #draw the edges
        for i in self.edge_weights.keys():
            from_vertex, to_vertex = i #unpack the tuple (needed help with this)
            #get distance between vertices to impact color
            distance =  dist(from_vertex.xCoord(), from_vertex.yCoord(), to_vertex.xCoord(), to_vertex.yCoord())
            distance = (distance * 255) / 800
            #print(distance) #for testing
            pygame.draw.line(screen, (int(distance),int(255-distance), 0 ), (from_vertex.xCoord(), from_vertex.yCoord()), (to_vertex.xCoord(), to_vertex.yCoord()), 2)
            
        #draw the vertices
        for i in self.adjacency_list:
            i.draw()
            
    
    
#----------------------------------------------------------------------------
def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
#---------------------------------------------------------------------------
def bellman_ford(graph, start_vertex):
    # Initialize all vertex distances to infinity and
    # and predecessor vertices to None.
    for current_vertex in graph.adjacency_list:
      current_vertex.distance = float('inf') # Infinity
      current_vertex.pred_vertex = None

    # start_vertex has a distance of 0 from itself
    start_vertex.distance = 0                

    # Main loop is executed |V|-1 times to guarantee minimum distances.
    for i in range(len(graph.adjacency_list)-1):
        # The main loop.
        for current_vertex in graph.adjacency_list:
            for adj_vertex in graph.adjacency_list[current_vertex]:
                edge_weight = graph.edge_weights[(current_vertex, adj_vertex)]
                alternative_path_distance = current_vertex.distance + edge_weight
                      
                # If shorter path from start_vertex to adj_vertex is found,
                # update adj_vertex's distance and predecessor
                if alternative_path_distance < adj_vertex.distance:
                   adj_vertex.distance = alternative_path_distance
                   adj_vertex.pred_vertex = current_vertex

    # Check for a negative edge weight cycle
    for current_vertex in graph.adjacency_list:
        for adj_vertex in graph.adjacency_list[current_vertex]:
             edge_weight = graph.edge_weights[(current_vertex, adj_vertex)]
             alternative_path_distance = current_vertex.distance + edge_weight

             # If shorter path from start_vertex to adj_vertex is still found,
             # a negative edge weight cycle exists
             if alternative_path_distance < adj_vertex.distance:
                return False

    return True



#dijkstra's algorithm!-------------------------------------------------
def dijkstra_shortest_path(g, start_vertex):
    # Put all vertices in an unvisited queue.
    unvisited_queue = []
    for current_vertex in g.adjacency_list:
        unvisited_queue.append(current_vertex)

    # Start_vertex has a distance of 0 from itself
    start_vertex.distance = 0

    # One vertex is removed with each iteration; repeat until the list is
    # empty.
    while len(unvisited_queue) > 0:
        
        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)
        pygame.draw.circle(screen, (100, 100, 250), (current_vertex.xCoord(), current_vertex.yCoord()), 20)

        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in g.adjacency_list[current_vertex]:
            edge_weight = g.edge_weights[(current_vertex, adj_vertex)]
            alternative_path_distance = current_vertex.distance + edge_weight
                  
            # If shorter path from start_vertex to adj_vertex is found,
            # update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex
                
def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        print("go to", current_vertex.xpos, current_vertex.ypos)
        path = " -> " + str(current_vertex.label) + path
        current_vertex = current_vertex.pred_vertex
    path = start_vertex.label + path
    return path

def get_shortest_path_list(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = []
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        #print("go to", current_vertex.xpos, current_vertex.ypos)
        path.append((current_vertex.xpos, current_vertex.ypos)) 
        current_vertex = current_vertex.pred_vertex
    
    return path

        
# Program to find shortest paths from vertex A.
g = Graph()

vertex_a = Vertex("House", 100, 100)
vertex_b = Vertex("Farm", 500, 500)
vertex_c = Vertex("Sawmill", 500, 200)
vertex_d = Vertex("Water Pump", 200, 500)
vertex_e = Vertex("lumber yard", 300, 700)
vertex_f = Vertex("Storage Shed", 700, 100)
vertex_g = Vertex("Herbalist Hut", 700, 700)

g.add_vertex(vertex_a)
g.add_vertex(vertex_b)
g.add_vertex(vertex_c)
g.add_vertex(vertex_d)
g.add_vertex(vertex_e)
g.add_vertex(vertex_f)
g.add_vertex(vertex_g)

g.add_undirected_edge(vertex_a, vertex_b, dist(vertex_a.xpos, vertex_a.ypos, vertex_b.xpos, vertex_b.ypos))
g.add_undirected_edge(vertex_a, vertex_c, dist(vertex_a.xpos, vertex_a.ypos, vertex_c.xpos, vertex_c.ypos))
g.add_undirected_edge(vertex_a, vertex_d, dist(vertex_a.xpos, vertex_a.ypos, vertex_d.xpos, vertex_d.ypos))
g.add_undirected_edge(vertex_b, vertex_c, dist(vertex_b.xpos, vertex_b.ypos, vertex_c.xpos, vertex_c.ypos))
g.add_undirected_edge(vertex_b, vertex_d, dist(vertex_b.xpos, vertex_b.ypos, vertex_d.xpos, vertex_d.ypos))
g.add_undirected_edge(vertex_c, vertex_d, dist(vertex_c.xpos, vertex_c.ypos, vertex_d.xpos, vertex_d.ypos))
g.add_undirected_edge(vertex_c, vertex_e, dist(vertex_c.xpos, vertex_c.ypos, vertex_e.xpos, vertex_e.ypos))
g.add_undirected_edge(vertex_c, vertex_f, dist(vertex_c.xpos, vertex_c.ypos, vertex_f.xpos, vertex_f.ypos))
g.add_undirected_edge(vertex_b, vertex_f, dist(vertex_b.xpos, vertex_b.ypos, vertex_f.xpos, vertex_f.ypos))
g.add_undirected_edge(vertex_e, vertex_f, dist(vertex_e.xpos, vertex_e.ypos, vertex_f.xpos, vertex_f.ypos))
g.add_undirected_edge(vertex_e, vertex_b, dist(vertex_e.xpos, vertex_e.ypos, vertex_b.xpos, vertex_b.ypos))
g.add_undirected_edge(vertex_g, vertex_f, dist(vertex_g.xpos, vertex_g.ypos, vertex_f.xpos, vertex_f.ypos))
g.add_undirected_edge(vertex_g, vertex_e, dist(vertex_g.xpos, vertex_g.ypos, vertex_f.xpos, vertex_f.ypos))


# Run the algorithms
if choice == 1:
    dijkstra_shortest_path(g, vertex_a)
else:
    bellman_ford(g, vertex_a)

# Sort the vertices by the label for convenience; display shortest path for each vertex
# from vertex_a.    
for v in sorted(g.adjacency_list, key=operator.attrgetter("label")):
    if v.pred_vertex is None and v is not vertex_a:
        print("House to %s: no path exists" % v.label)
    else:
        print("House to %s: %s (total weight: %g)" % (v.label, get_shortest_path(vertex_a, v), v.distance))

print("going from house to hut:", (get_shortest_path(vertex_a, vertex_g)))
print(get_shortest_path_list(vertex_a, vertex_g))
beaverPath = get_shortest_path_list(vertex_a, vertex_g)
counter = 1

nextNode = beaverPath[len(beaverPath)-counter]
print("heading towards", nextNode)


running = True
while running:
    clock.tick(60)
    # Input section
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #update section
    if(zoti.move(nextNode) == 0):
        nextNode = beaverPath[len(beaverPath)-counter]
        if counter < len(beaverPath):
            counter+=1
    
    else:
        counting_time = pygame.time.get_ticks() - start_time
    #credit for this section: https://stackoverflow.com/questions/20359845/how-would-i-add-a-running-timer-that-shows-up-on-the-screen-in-pygame
    counting_minutes = str(counting_time // 60000)
    counting_seconds = str( (counting_time % 60000)//1000 )
    counting_milliseconds = str(counting_time % 1000)

        
    #render section       
    screen.fill((0, 0, 0))  # Clear screen
    
    #draw nodes
    g.draw()
    zoti.draw()
    counting_string = "%s: %s: %s" % (counting_minutes, counting_seconds, counting_milliseconds)
    counting_text = font.render(str(counting_string), 1, (255,255,255))
    counting_rect = counting_text.get_rect(center = (150,10))
    screen.blit(counting_text, counting_rect)

        
    pygame.display.flip()  # Update screen

pygame.quit()

