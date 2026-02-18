import Special_classes as spec
import random
import pygame
from pygame import MOUSEBUTTONUP

pygame.init()

class Maze:
    def __init__(self):
        """
        Class for maze generation and maze variable storage
        """
        self.player = Path()  # Path class
        self.maze, self.start, self.end, self.length = self.gen_mul_maze(6)
        """ List of maze matrixes, list of maze start points, List of maze end points, List of maze length"""

    def gen_mul_maze(self, times):
        """
        Generates all mazes matrixes and their parameters
        --------------------------------------------------
        :param times: int: Number of mazes
        --------------------------------------------------
        :return:
        -:param mazes: list: List of mazes
        -:param starts: list: List of start points
        -:param ends: list: List of end points
        -:param lengs: list: List of maze lengths
        """
        mazes = []  # List of mazes
        starts = []  # List of start points
        ends = []  # List of end points
        lengs = []  # List of lengths
        for i in range(times):
            maze, leng = self.gen_maze(i)
            start, end = self.gen_start_end(leng, maze)
            mazes.append(maze)
            starts.append(start)
            ends.append(end)
            lengs.append(leng)
        return mazes, starts, ends, lengs

    def gen_maze(self, i):
        """
        Generates specific maze
        --------------------------------------------------
        :param i: int: Maze number
        --------------------------------------------------
        :return:
        -:param maze: Maze matrix
        -:param length: Maze lengths - (row length, column length)
        """
        mazefile = open(f"maze{i}.txt", 'r')
        mazelines = mazefile.readlines()
        mazefile.close()
        maze = []
        length = []
        for i in range(len(mazelines)):
            maze.append([])
            for j in range(len(mazelines[i])):
                if mazelines[i][j] != '\n':
                    maze[i].append(mazelines[i][j])
                length.append(len(maze[i]))
        le = (max(length), len(maze))
        return maze, le

    def gen_start_end(self, length, lab):
        """
        Generates start and end points
        --------------------------------------------------
        :param length: tuple: Lengths of maze
        :param lab: class: Maze class
        --------------------------------------------------
        :return:
        -:param points[0]: tuple: Start point
        -:param points[1]: tuple: End point
        """
        points = []
        cha = ['@', " "]
        for i in range(2):
            tack = random.randint(0, 1)
            if tack:
                points.append(self.gen_coor(True, length, lab))
                lab[points[i][0]][points[i][1]] = cha[i]
            else:
                points.append(self.gen_coor(False, length, lab))
                lab[points[i][0]][points[i][1]] = cha[i]
        return points[0], points[1]

    def gen_coor(self, bool, le, lab):
        """
        Generates start or end point
        --------------------------------------------------
        :param bool: bool: Boolean for generation - If true generates on North or South border. If false generates on
        East or West border
        :param le: tuple: Length of the maze
        :param lab: class: Maze class
        --------------------------------------------------
        :return:
        -:param: tuple: Start or end point - (y, x)
        """
        if bool:
            point = (random.choice([0, le[1] - 1]), random.randint(1, le[0]-2))
            if point[0] == 0:
                if lab[point[0]][point[1]] != '#' or self.point_gen_check('N', point, '#', (1, 0), 0,
                                                                          lab):
                    return self.gen_coor(bool, le, lab)
            elif point[0] == le[1] - 1:
                if lab[point[0]][point[1]] != '#' or self.point_gen_check('S', point, '#', (-1, 0), le[0],
                                                                          lab):
                    return self.gen_coor(bool, le, lab)
        else:
            point = (random.randint(1, le[1] - 2), random.choice([0, le[0] - 1]))
            if point[1] == 0:
                if lab[point[0]][point[1]] != '#' or (self.point_gen_check('W', point, '#', (0, 1), 0,
                                                                           lab)):
                    return self.gen_coor(bool, le, lab)
            elif point[1] == le[0] - 1:
                if lab[point[0]][point[1]] != '#' or (self.point_gen_check('E', point, '#', (0, -1), le[0],
                                                                           lab)):
                    return self.gen_coor(bool, le, lab)
        return point

    def point_gen_check(self, dir, point, ch, diradd, mx, lab):
        """
        Used to check if the start or end points are generated correctly
        --------------------------------------------------
        :param dir: string: Direction for checking
        :param point: tuple: Position for checking
        :param ch: string: Character that's checked for
        :param diradd: tuple: For direction addition - (y +/- 1, x +/- 1)
        :param mx: int: Value for border checking
        :param lab: class: Maze class
        --------------------------------------------------
        :return: bool
        """
        if self.player.check_border(dir, point, mx):
            if lab[point[0] + diradd[0]][point[1] + diradd[1]] == ch:
                return True
        return False


class Path:
    def __init__(self, start=(1,1)):
        """
        Class for path finding
        --------------------------------------------------
        :param start: tuple: Start point
        """
        self.known = spec.Stack([start])  # Stack for path positions
        self.trail = ()  # previous move

    def move(self, move, ch, en, lab, ind, g):
        """
        Main recursive moving function
        --------------------------------------------------
        :param move: tuple: Next move position
        :param ch: string: Character for search
        :param en: string: Character of trail
        :param lab: class: Maze
        :param ind: int: Index of maze in list
        :param g: class: Game class
        --------------------------------------------------
        :return:
        """
        g.draw()
        lab.maze[ind][self.known.peek()[0]][self.known.peek()[1]] = en
        if ch == ' ':
            self.known.push(move)
        self.trail = move
        runi = self.narrower(lab, ind, move)
        if (move[0] < lab.length[ind][1] and move[0] >= 0) and (0 <= move[1] < lab.length[ind][0]) and runi != ():
            if lab.maze[ind][move[0]][move[1]] == ch and len(self.check_dir(ch, lab, ind, runi)) == 1:
                self.trail = move
                return self.move(self.narrower(lab, ind, move), ch, en, lab, ind, g)

    def check_dir(self, ch, lab, ind, loc):
        """
        Checks and gets all possible next moves
        --------------------------------------------------
        :param ch: string: Character for search
        :param lab: class: Maze class
        :param ind: int: Index of mazes in list
        :param loc: tuple: Origin position for check
        --------------------------------------------------
        :return:
        -:param pos: list: List of all possible next moves
        """
        pos = []
        if self.check_border('N', loc, 0):
            if lab.maze[ind][loc[0] - 1][loc[1]] == ch:
                pos.append((loc[0] - 1, loc[1]))
        if self.check_border('S', loc, lab.length[ind][1]):
            if (lab.maze[ind][loc[0] + 1][loc[1]]
                    == ch):
                pos.append((loc[0] + 1, loc[1]))
        if self.check_border('E', loc, lab.length[ind][0]):
            if (lab.maze[ind][loc[0]][loc[1] + 1]
                    == ch):
                pos.append((loc[0], loc[1] + 1))
        if self.check_border('W', loc, 0):
            if (lab.maze[ind][loc[0]][loc[1] - 1]
                    == ch):
                pos.append((loc[0], loc[1] - 1))
        return pos

    def check_border(self, dirs, thing, num):
        """
        Checks if next move is not outside of range
        --------------------------------------------------
        :param dirs: string: Direction for check
        :param thing: tuple: Position
        :param num: int: Number for range check
        --------------------------------------------------
        :return: bool
        """
        if dirs == "N" and thing[0] >= num:
            return True
        elif dirs == 'W' and thing[1] >= num:
            return True
        elif dirs == 'S' and thing[0] < num-1:
            return True
        elif dirs == 'E' and thing[1] < num-1:
            return True
        else:
            return False

    def valuator(self, pos, end):
        """
        Decides which of the next moves is closer to end point
        --------------------------------------------------
        :param pos: tuple: Next move positions
        :param end: tuple: End point
        --------------------------------------------------
        :return:
        - tuple: Chosen position
        """
        dist = []  # List of distances from next move positions to end point
        chosen = ()  # Chosen point
        for i in range(len(pos)):
            dist.append(abs(end[0] - pos[i][0]) + abs(end[1] - pos[i][1]))
        chosen = min(dist)
        return dist.index(chosen)

    def path_finder(self, lab, go, ind, g):
        """
        Main path finding function
        --------------------------------------------------
        :param lab: class: Maze class
        :param go: bool: Boolean for path finding
        :param ind: int: Index of mazes in list
        :param g: class: Game clas
        --------------------------------------------------
        :return:
        -:param go: bool: Boolean for path finding
        """
        if len(self.check_dir(' ', lab, ind, self.known.peek())) == 0:
            self.known.pop()
            lab.maze[ind][self.trail[0]][self.trail[1]] = '@'
            self.move(self.known.peek(), '*', '@', lab, ind, g)
        else:
            self.move(self.narrower(lab, ind, self.known.peek()), ' ', '*', lab, ind, g)
        if self.known.peek() == lab.end[ind]:
            go = False
            lab.maze[ind][self.known.peek()[0]][self.known.peek()[1]] = '*'
        return go

    def inter_check(self, pos):
        """
        Checks if there is intersection
        --------------------------------------------------
        :param pos: tuple: Next position
        --------------------------------------------------
        :return: bool
        """
        if len(pos) > 1:
            return True
        else:
            return False

    def narrower(self, lab, ind, loc):
        """
        Chooses the next move if there is more than one of possible positions
        --------------------------------------------------
        :param lab: class: Maze class
        :param ind: int: Index of maze in list
        :param loc: tuple: Position
        --------------------------------------------------
        :return:
        -:param posdir: tuple: Chosen position
        """
        posdirs = self.check_dir(' ', lab, ind, loc)
        posdir = ()
        if len(posdirs)==0:
            return ()
        elif self.inter_check(posdirs):
            posdir = posdirs[self.valuator(posdirs, lab.end[ind])]
        else:
            posdir = posdirs[0]
        return posdir


class Game:
    def __init__(self):
        """
        Main class
        """
        self.labyrinth = Maze()  # Maze class
        self.player = Path()  # Path class
        self.going = True  # Boolean for path finding
        self.startBool = True  # Boolean for start screen
        self.settingBool = False  # Boolean for setting screen
        self.tick = 0  # For speed of path finding
        self.ind = 0  # Index of maze in list

    def start_draw(self):
        """
        Function for drawing start screen and setting screen
        --------------------------------------------------
        :return: None
        """
        screen.fill((255, 255, 255))
        mousex, mousey = pygame.mouse.get_pos()
        if not self.settingBool:
            solve_rect = pygame.Rect((width / 2 - 110, height / 2 - 5), (105 * 2, 90))
            screen.blit(lar.render("Maze", True, (0, 0, 0)), (width / 2 - 100, 20))
            screen.blit(lar.render('Solver', True, (0, 0, 0)), (width / 2 - 105, height / 2))
            if pygame.Rect.collidepoint(solve_rect, (mousex, mousey)) and event.type == MOUSEBUTTONUP:
                self.settingBool = True
                pygame.time.wait(500)
        else:
            screen.blit(lar.render('Choose the size', True, (0, 0, 0)), (width / 2 - 250, height / 4))
            for i in range(6):
                map_rect = pygame.Rect((width / 7 + 100 * i, height / 2), (60, 90))
                screen.blit(lar.render(f'{i + 1}', True, (0, 0, 0)), (width / 7 + 100 * i, height / 2 + 5))
                if pygame.Rect.collidepoint(map_rect, (mousex, mousey)) and event.type == MOUSEBUTTONUP:
                    self.settingBool = False
                    self.startBool = False
                    self.ind = i
                    clock.tick((i+1) * 30)
                    self.player = Path(self.labyrinth.start[self.ind])
                    pygame.time.wait(1000)
        pygame.display.update()

    def draw(self):
        """
        Function for drawing maze
        :return: None
        """
        screen.fill((255, 255, 255))
        settingrect = pygame.Rect((0, 0), (
        width / len(self.labyrinth.maze[self.ind][0]), width / len(self.labyrinth.maze[self.ind][0])))
        for i in range(len(self.labyrinth.maze[self.ind])):
            for j in range(len(self.labyrinth.maze[self.ind][i])):
                settingrect = pygame.Rect(
                    (width / self.labyrinth.length[self.ind][0] * j, height / self.labyrinth.length[self.ind][1] * i),
                    (width / (self.labyrinth.length[self.ind][0] * 0.85),
                     height / (self.labyrinth.length[self.ind][1] * 0.85)))
                if self.labyrinth.maze[self.ind][i][j] == '#':
                    pygame.draw.rect(screen, (0, 0, 0), settingrect)
                elif self.labyrinth.maze[self.ind][i][j] == '*':
                    pygame.draw.rect(screen, (50, 50, 205), settingrect)
                elif (i, j) == self.labyrinth.start[self.ind] and self.going:
                    pygame.draw.rect(screen, (0, 150, 200), settingrect)
                elif (i, j) == self.labyrinth.end[self.ind] and self.going:
                    pygame.draw.rect(screen, (50, 255, 100), settingrect)
                elif self.labyrinth.maze[self.ind][i][j] == '@' and self.going:
                    pygame.draw.rect(screen, (200, 0, 0), settingrect)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), settingrect)
        pygame.display.update()

    def main(self, run):
        """
        Main
        --------------------------------------------------
        :param run: bool: Main run boolean
        --------------------------------------------------
        :return:
        -:param run: bool: Main run boolean
        """
        if self.startBool:
            self.start_draw()
        elif not self.startBool:
            self.draw()
            if self.going:
                self.going = self.player.path_finder(self.labyrinth,  self.going, self.ind, self)
                self.bool = False
            else:
                pygame.time.wait(1000)
                return False
        return run


run = True  # Main run boolean
width, height = 700, 700  # Width and height of the screen
lar = pygame.font.Font('Geo.ttf', 80)  # Font

clock = pygame.time.Clock()
game = Game()

screen = pygame.display.set_mode((width, height))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    run = game.main(run)

pygame.quit()
pygame.display.quit()
