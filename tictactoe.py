import random

# Constants for game parameters
NUM_PLAYERS = 2
FIELD_WIDTH = 10
GOAL_SIZE = 3
MAX_KICK_DISTANCE = 2

class Player:
    def __init__(self, name):
        self.name = name
        self.pos = [0, 0]
    
    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy
    
    def kick(self, dx, dy):
        distance = min(MAX_KICK_DISTANCE, ((dx ** 2) + (dy ** 2)) ** 0.5)
        ball_pos = [self.pos[0] + dx, self.pos[1] + dy]
        return (ball_pos, distance)
        

class Ball:
    def __init__(self):
        self.pos = [FIELD_WIDTH // 2, 0]
    
    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy


class Game:
    def __init__(self):
        self.players = []
        self.ball = None
        self.score = [0, 0]
    
    def setup(self):
        # Create players
        for i in range(NUM_PLAYERS):
            name = input(f"Enter name for player {i+1}: ")
            self.players.append(Player(name))
        
        # Create ball
        self.ball = Ball()
    
    def draw_field(self):
        for y in range(FIELD_WIDTH):
            row = ""
            for x in range(FIELD_WIDTH):
                if x == self.ball.pos[0] and y == self.ball.pos[1]:
                    row += "O"
                elif x == 0 and y == FIELD_WIDTH // 2:
                    row += "|"
                elif x == FIELD_WIDTH - 1 and y == FIELD_WIDTH // 2:
                    row += "|"
                else:
                    occupied = False
                    for player in self.players:
                        if player.pos[0] == x and player.pos[1] == y:
                            row += str(self.players.index(player))
                            occupied = True
                            break
                    if not occupied:
                        row += "."
            print(row)
    
    def check_goal(self):
        if self.ball.pos[1] == FIELD_WIDTH - 1 and abs(self.ball.pos[0] - (FIELD_WIDTH // 2)) < GOAL_SIZE:
            scoring_player = None
            for player in self.players:
                if player.pos == self.ball.pos:
                    scoring_player = self.players.index(player)
                    break
            if scoring_player is not None:
                self.score[scoring_player] += 1
            self.ball = Ball()
            print(f"Goal! Current score: {self.score[0]}-{self.score[1]}")
    
    def play_game(self):
        self.setup()
        current_player = 0
        
        while True:
            self.draw_field()
            
            player = self.players[current_player]
            print(f"It's {player.name}'s turn.")
            
            dx = int(input("Enter x distance to move: "))
            dy = int(input("Enter y distance to move: "))
            
            player.move(dx, dy)
            
            dx = int(input("Enter x distance to kick: "))
            dy = int(input("Enter y distance to kick: "))
            
            ball_pos, distance = player.kick(dx, dy)
            self.ball.move(dx, dy)
            
            if distance > MAX_KICK_DISTANCE:
                print("You kicked too hard!")
                self.ball = Ball()
            
            self.check_goal()
            
