import random
import pygame

# Here we will define some global variables which will be used throughout the program
white = (255, 255, 255)
black = (0, 0, 0)
width, height = 800,800 
size_of_square = 10  # size of each grid square
x_cells_count = width // size_of_square
y_cells_count = height // size_of_square
lifetime = 5  # This the time in which the pheremon will decay


class Pheromone:
    '''
        This contains the pheromone released by the ans 
        which will have a color and an age
    '''
    def __init__(self, color):
        self.color = color
        self.age = 0

    def decay(self):
        self.age += 1
        if self.age > lifetime:
            return True
        return False


class ant:
    '''
        This class contains the ant and the functions to control its motion
    '''
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color # The color which will be R or G
        """The pointer below represents directions:
                0 -> up
                1 -> right
                2 -> down
                3 -> left
        """
        self.pointer = 0

    def turn_clockwise(self):
        self.pointer = (self.pointer + 1) % 4

    def turn_counterclockwise(self):
        self.pointer = (self.pointer - 1) % 4

    def move(self):
        if self.pointer == 0:
            self.y += 1
        elif self.pointer == 1:
            self.x += 1
        elif self.pointer == 2:
            self.y -= 1
        else:
            self.x -= 1

class langston_ant_start:
    def __init__(self):
        """
        In initializaiton we are gonna create :
        1) A grid which will store the color of each square.
        2) A dictionary called pheromones which will store tuple of (x,y) as key and pheremone type as value.

        """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        # Initialize grid and ants
        self.grid = [
            [white for i in range(y_cells_count)] for i in range(x_cells_count)
        ]
        self.pheromones = {}
        self.ant1 = ant(x_cells_count // 2, y_cells_count // 2, "R")
        self.ant2 = ant(x_cells_count // 3 ,y_cells_count // 3, "G")
        self.ants = [self.ant1, self.ant2]

    def release_pheromone(self, ant):
        '''
            This is simply gonna store the applied pheromone is the dictionary
        '''
        if ant.color == "R":
            new_pheromone = Pheromone("R")
        else:
            new_pheromone = Pheromone("G")
        self.pheromones[(ant.x, ant.y)] = new_pheromone

    def update_grid_by_ant(self, ant):
        '''
            this will change the color of the grid and turn the ant accordingly
        '''
        if self.grid[ant.x % x_cells_count][ant.y % y_cells_count] == white:
            ant.turn_clockwise()
            self.grid[ant.x % x_cells_count][ant.y % y_cells_count] = black
        else:
            self.grid[ant.x % x_cells_count][ant.y % y_cells_count] = white
            ant.turn_counterclockwise()

    def update_ants(self):
        '''
            this is the function that will apply the turning rule
        '''
        for ant in self.ants:
            pheromone_found = False
            self_phermone = False

            if (ant.x, ant.y) in self.pheromones:
                pheromone_found = True
                if self.pheromones[(ant.x, ant.y)].color == ant.color:
                    self_phermone = True

            self.release_pheromone(ant)

            if not pheromone_found:
                self.update_grid_by_ant(ant)
            else:
                if self_phermone:
                    if random.random() >= 0.8:
                        self.update_grid_by_ant(ant)
                else:
                    if random.random() >= 0.2:
                        self.update_grid_by_ant(ant)
            ant.move()

    def decay_pheromones(self):
        for pos, pheromone in list(self.pheromones.items()):
            pheromone.decay()
            if pheromone.age > lifetime:
                del self.pheromones[pos]

    def draw_grid(self):
        for x in range(x_cells_count):
            for y in range(y_cells_count):
                rect_obj = (
                    x * size_of_square,
                    y * size_of_square,
                    size_of_square,
                    size_of_square,
                )
                # This will simply draw squares of color which is stored in grid matrix
                pygame.draw.rect(self.screen, self.grid[x][y], rect_obj)
        for x in range(x_cells_count):
            pygame.draw.line(
                self.screen,
                black,
                (x * size_of_square, 0),
                (x * size_of_square, height),
            )
        for y in range(y_cells_count):
            pygame.draw.line(
                self.screen, black, (0, y * size_of_square), (width, y * size_of_square)
            )

    def draw_ants(self):
        # The following draws two rectangle on the screen with the color Red and Green,
        # For this we define two rectangles which are mentioned below
        rect_obj1 = (
            self.ant1.x * size_of_square,
            self.ant1.y * size_of_square,
            size_of_square,
            size_of_square,
        )
        rect_obj2 = (
            self.ant2.x * size_of_square,
            self.ant2.y * size_of_square,
            size_of_square,
            size_of_square,
        )
        pygame.draw.rect(self.screen, (255, 0, 0), rect_obj1)  # Red ant
        pygame.draw.rect(self.screen, (0, 255, 0), rect_obj2)  # Green ant

    def run(self):
        # Setting the following variables to global scope to use them in other functions:
        running = True
        while running:
            self.screen.fill(white)
            self.draw_grid()
            self.draw_ants()

            self.update_ants()
            self.decay_pheromones()

            pygame.display.update()
            self.clock.tick(100000)  # Control the simulation speed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


if __name__ == "__main__":
    run = langston_ant_start()
    run.run()
