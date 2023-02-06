import numpy as np
class Environment:
    total_players = 2
    def __init__(self) -> None:
        pass

    def run(self):
        self.start_game()

    def start_game(self):
        # Initialze Rummikub
        self.initialize()

        # Let each player play until finished
        current_player = 0
        not_finished = True
        while(not_finished):
            #print("Now playing player: " + str(Board.players[current_player].id))
            # Determine if the player wants to place a move or if they want to draw a new piece.
                # With every possible move, you have to make a collection of all possible continuous moves.
                # This includes overlapping ones.

                # Every piece has to be checked if it is a:
                # - connector piece for the hand
                # - part of 3-4 color set
                # - part of 3+ numerical set

                # This should give a value to the expected utility of said piece.
            
            hand = Board.players[current_player].hand
            for tile in hand:
                # Caluculate all the possible moves:
                # 3+ numerical set
                if check_if_tile_in_deck(tile.value-1, tile.color, hand) and check_if_tile_in_deck(tile.value+1, tile.color, hand):
                    # Play the tile(s)
                    hand = Board.play_set(Board, [[tile.value-1, tile.color], [tile.value, tile.color], [tile.value+1, tile.color]], hand)
                    Board.players[current_player].plays += 1

                # Connector piece
                #'''
                for iter in range(len(Board.field)):
                    tail = Board.field[iter][0]
                    head = Board.field[iter][-1]
                    if tail[0] == tile.value + 1 and tail[1] == tile.color:
                        # Appendable before this combination
                        #hand = Board.play_connector(Board, tile, hand, 0),
                        hand = Board.play_connector(Board, iter, 0, tile ,hand)
                        pass
                    elif head[0] == tile.value - 1 and tail[1] == tile.color:
                        # Appendable after this combination
                        pass                
                #'''
                # 3-4 Color set


                # If you play a tile, color set or numerical set, save the hand and calculate the rewarding from future runs.
                # then also save the 


                # If possible to play, save the state. Then, continue with a new run (funtioncall) with the new board (calculating reward).
                # then, continue with the current board.

            # Draw or move
            Board.players[current_player].draw()

            # Check if finished
            if len(Board.deck) == 0:
                not_finished = False

            # Select next player
            if current_player+1 == self.total_players:
                current_player = 0
            else:
                current_player += 1

        # Analyze the score
        print("Final board looks like this:")
        for combination in Board.field:
            print(combination)

        print("")
        print("Final player decks looks like:")
        for player in Board.players:
            print(player.hand)
            hand_score = 0
            for tile in player.hand:
                hand_score += tile.value
            print(f"Player {player.id} ended with score: {hand_score} (plays: {player.plays})")
        pass
    
    # Create the board
    def initialize(self):
        board = Board
        board.setup(self)

class Player:
    plays = 0
    hand = []
    id = -1
    def __init__(self, id) -> None:
        self.hand = []
        self.id = id
        for tile in range(14):
            self.draw()
        pass

    def draw(self):
        tile_drawn = Board.deck[0]
        Board.deck.pop(0)
        self.hand.append(tile_drawn)
    
    def __repr__(self) -> str:
        result = "Player: " + str(self.id) + " "
        for tile in self.hand:
            result += tile.get_data() + " "
        return result

class Board:
    deck = []
    players = []
    field = []
    def __init__(self) -> None:
        pass
    
    def setup(self):
        # Add 
        for number in range(1, 13):
            for color in range(1,4):
                Board.deck.append(Tile(number, color))
                Board.deck.append(Tile(number, color))
        
        # Add Jokers
        Board.deck.append(Tile(20, 0))
        Board.deck.append(Tile(20, 1))
        np.random.shuffle(Board.deck)

        # Add players
        for player in range(Environment.total_players):
            new_player = Player(player)
            Board.players.append(new_player)
    
    def play_set(self, tiles, hand):
        self.field.append(tiles)
        for tile in tiles:
            hand = remove_card(hand, tile[0], tile[1])
        return hand

    def play_connector(self, field_location, insert_location, tile, hand):
        self.field[field_location].insert(insert_location, [tile.value, tile.color])
        hand = remove_card(hand, tile.value, tile.color)
        return hand

class Tile:
    value = None
    color = None
    def __init__(self, value, color) -> None:
        self.value = value
        self.color = self.determine_tile(color)

    def determine_tile(self, color):
        colors = ["Red","Black", "Blue", "Orange"]
        return colors[color]

    def convert_information_to_tile(self, value, color):
        self.value = value
        self.color = color
    
    def get_data(self):
        return self.color + str(self.value)

    def __repr__(self) -> str:
        return self.get_data()
        pass

def check_if_tile_in_deck(value, color, deck):
    for tile in deck:
        if tile.value is value and tile.color is color:
            return True
    return False # Possibly?

def check_if_tile_is_edge(value, color, field):
    for combination in field:
        if combination[0].value == value and combination[0].color == color:
            return True
        if combination[-1].value == value and combination[-1].color == color:
            return True
    return False

def remove_card(hand, value, color):
    for tile in range(len(hand)):
        if hand[tile].color == color and hand[tile].value == value:
            hand.pop(tile)
            break
    return hand