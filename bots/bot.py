import random
from src.game_constants import SnipePriority, TowerType
from src.robot_controller import RobotController
from src.player import Player
from src.map import Map

import heapq
import sys

class Node:
    def __init__(self, x, y, cost=float('inf')):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent = None

    def __lt__(self, other):
        return self.cost < other.cost

class AStar:
    def __init__(self):
        pass

    def create_grid(self, rows, cols):
        return [[0 for _ in range(cols)] for _ in range(rows)]

    def get_neighbors(self, rows, cols, row, col):
        neighbors = []

        # Left
        if col > 0:
            neighbors.append((row, col - 1))
        # Up
        if row > 0:
            neighbors.append((row - 1, col))
        # Right
        if col < cols - 1:
            neighbors.append((row, col + 1))
        # Down
        if row < rows - 1:
            neighbors.append((row + 1, col))

        return neighbors

    def backward_a_star(self, rows, cols, start, goal):
        g_values = self.create_grid(rows, cols)
        heap = [(0, goal)]
        visited = set()

        while heap:
            current_g, current_node = heapq.heappop(heap)
            if current_node in visited:
                continue

            visited.add(current_node)
            row, col = current_node

            g_values[row][col] = current_g

            neighbors = self.get_neighbors(rows, cols, row, col)
            for neighbor in neighbors:
                if neighbor not in visited:
                    g_value = current_g + 1
                    heapq.heappush(heap, (g_value, neighbor))

        return g_values

class BotPlayer(Player):
    def __init__(self, map: Map):
        self.map = map

    def play_turn(self, rc: RobotController):
        # self.build_towers(rc)
        # self.towers_attack(rc)
        self.print_cost_map(*self.get_map(rc))

    def get_map(self, rc: RobotController):
        map = self.map
        H, W = map.height, map.width
        rows = map.height
        cols = map.width
        start, end = map.path[0], map.path[-1]
        start = (start[0], W - start[1] - 1) # flip row
        end = (end[0], W - end[1] - 1) # flip row
        print("start: ", start, "end: ", end)
        return rows, cols, start, end

    def print_cost_map(self, rows, cols, start, end):
        g_values = AStar().backward_a_star(rows, cols, start, end)

        print("Optimal g value cost map:")
        for row in g_values:
            print(row)

    def build_towers(self, rc: RobotController):
        x = random.randint(0, self.map.height-1)
        y = random.randint(0, self.map.height-1)
        tower = random.randint(1, 4) # randomly select a tower
        if (rc.can_build_tower(TowerType.GUNSHIP, x, y) and 
            rc.can_build_tower(TowerType.BOMBER, x, y) and
            rc.can_build_tower(TowerType.SOLAR_FARM, x, y) and
            rc.can_build_tower(TowerType.REINFORCER, x, y)
        ):
            if tower == 1:
                rc.build_tower(TowerType.BOMBER, x, y)
            elif tower == 2:
                rc.build_tower(TowerType.GUNSHIP, x, y)
            elif tower == 3:
                rc.build_tower(TowerType.SOLAR_FARM, x, y)
            elif tower == 4:
                rc.build_tower(TowerType.REINFORCER, x, y)
    
    def towers_attack(self, rc: RobotController):
        towers = rc.get_towers(rc.get_ally_team())
        for tower in towers:
            if tower.type == TowerType.GUNSHIP:
                rc.auto_snipe(tower.id, SnipePriority.FIRST)
            elif tower.type == TowerType.BOMBER:
                rc.auto_bomb(tower.id)
