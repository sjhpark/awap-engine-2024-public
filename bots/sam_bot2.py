from src.player import Player
from src.map import Map
from src.robot_controller import RobotController
from src.game_constants import TowerType, Team, Tile, GameConstants, SnipePriority, get_debris_schedule
from src.debris import Debris
from src.tower import Tower

import random
import itertools

class BotPlayer(Player):
    def __init__(self, map: Map):
        self.map = map

        # cooldowns and healths of debris to send
        self.cools = list(range(1, 5))
        self.hps = list(range(50,60))
    
    def play_turn(self, rc: RobotController):
        # self.test(rc)
        self.build_towers(rc)
        self.towers_attack(rc)
        self.send_debris(rc)

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
    
    def build_solar_farm(self, rc: RobotController):
        x = random.randint(0, self.map.height-1)
        y = random.randint(0, self.map.height-1)
        if rc.can_build_tower(TowerType.REINFORCER, x, y):
            print("build solar farm")
            rc.build_tower(TowerType.REINFORCER, x, y)

    def send_debris(self, rc: RobotController):
        us = rc.get_ally_team() # us
        for cool, hp in itertools.product(self.cools, self.hps):
            energy = rc.get_balance(us) # our current energy
            power = hp/cool # power to send debris
            if power <= energy/100 and rc.can_send_debris(cool, hp) == True:
                print("cool: ", cool, "hp: ", hp, "power: ", power, "energy: ", energy)
                rc.send_debris(cool, hp)
    
    def test(self, rc: RobotController):
        pass