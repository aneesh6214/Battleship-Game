from battleship import configuration
from battleship import board
class game:

    def valid_orientation(self, orientation):
        '''Checks the validity of a specified orientation
            Args:
                orientation (string): the orientation of a ship
            Returns:
                boolean: if the orientation is a substring of "horizontal" or "vertical"
        '''
        if orientation.lower() in "horizontally" or orientation.lower() in "vertically":
            return True
        return False

    def valid_location(self, board, row, col, ship_size, ship_orientation):
        '''Checks if a ship can be placed at a specified location on a specified board
            Args:
                board (Board): the board the ship is placed on
                row (int): the x coordinate of the ship to be placed
                col (int): the y coordinate of the ship to be placed
                ship_size (int): the size of the ship to be placed
                ship_orientation (string): the orientation of the ship to be placed
            Returns:
                boolean: if the specified location is valid for a ship placement
        '''
        # Check if start position is on board
        if not board.is_on_board(row, col):
            return False

        # Check if the ship will fit on the board
        if ship_orientation == "horizontally" and col + ship_size > board.cols:
            return False
        elif ship_orientation == "vertically" and row + ship_size > board.rows:
            return False

        # Check if the squares the ship will occupy are already occupied
        if board.get_value(row, col) != "*":
            return False
        if ship_orientation == "horizontally":
            for i in range(ship_size):
                if board.get_value(row, col + i) != "*":
                    return False
        elif ship_orientation == "vertically":
            for i in range(ship_size):
                if board.get_value(row + i, col) != "*":
                    return False

        return True





    def coords_to_intlist(self, coords):
        '''Converts a string of coords to a pair of integers
            Args:
                coords (string): a string of 2 coordinates
            Returns:
                list: a list of length 2 representing a coordinate pair
        '''
        coord_list = coords.split()
        return [int(coord_list[0]), int(coord_list[1])]

    def ship_killed(self, board, row, col, ship_name):
        '''If a specified position on a specified board is a ship that has not been sunk
            Args:
                board (Board): the specified Board to look at
                row (int): the x coordinate where the ship was hit
                col (int): the y coordinate where the ship was hit
                ship_name (string): the name of the ship
            Returns:
                boolean: If the ship was sunk or not
        '''
        #check if the spot is an X
        if board.get_value(row, col) == 'X':
            #Check if all adjacent values are either * or X
            for val in board.get_adjacent(row, col):
                if val == ship_name:
                    return False

        return True


    def gameplay(self):
        '''Runs the actual gameplay w/setup and shooting
            Args: none
            Returns: none
        '''
        # ===================
        # ====== SETUP ======
        # ===================
        config = configuration.configuration() #creates a configuration object
        config.read_configuration_file() #asks & reads the config file, creating a config
        config.ask_names() #asks names & assigns values

        players = [config.player1_name, config.player2_name] #list of both players, index 0 is p1's name, index 1 is p2's name
        placement_boards = [board.board(config.board_rows, config.board_cols), board.board(config.board_rows, config.board_cols)] #creates both boards, index 0 is p1's board, index 1 is p2's board

        turn = 0 #keeps track of whos turn it is, 0 is p1 turn, 1 is p2 turn

        #places p1's ships in iteration 1, places p2's ships in iteration 2
        for i in range(2):
            print("{0}'s Placement Board".format(players[turn]))
            placement_boards[turn].print_board()
            for ship in config.ship_types:
                # =================================
                # ASK FOR ORIENTATION AND ASSIGN IT
                # =================================
                #print(players[turn], ", enter the orientation of your ", ship[0], " which is ", ship[1], " long: ", end='')
                print("{0}, enter the orientation of your {1}, which is {2} long: ".format(players[turn], ship[0], ship[1]), end='')
                orientation = input().strip()
                while(self.valid_orientation(orientation) != True):
                    print("INVALID. {0}, enter the orientation of your {1} which is {2} long: ".format(players[turn], ship[0], ship[1]), end='')
                    orientation = input().strip()

                # ==============================
                # ASK FOR LOCATION AND ASSIGN IT
                # ==============================
                #print("Enter the starting location for your ", ship[0], " which is ", ship[1], " long, in the form row col: ", end='')
                print("Enter the starting location for your {0}, which is {1} long, in the form row col: ".format(ship[0], ship[1]), end='')
                location = input()
                location = self.coords_to_intlist(location)
                row = int(location[0])
                col = int(location[1])
                while(self.valid_location(placement_boards[turn], row, col, ship[1], orientation) == False):
                    print("INVALID. Enter the starting location for your {0}, which is {1} long, in the form row col: ".format(ship[0], ship[1]), end='')
                    location = input()
                    location = self.coords_to_intlist(location)
                    row = int(location[0])
                    col = int(location[1])

                #once the location is valid
                if orientation.lower() in "horizontally":
                    for i in range(ship[1]):
                        placement_boards[turn].set_value(row, col + i, ship[0])

                if orientation.lower() in "vertically":
                    for i in range(ship[1]):
                        placement_boards[turn].set_value(row + i, col, ship[0])
                print("{0}'s Placement Board".format(players[turn]))
                placement_boards[turn].print_board()
            turn = 1 - turn #swaps turn

        # ====================
        # ===== SHOOTING =====
        # ====================
        firing_boards = [board.board(config.board_rows, config.board_cols), board.board(config.board_rows, config.board_cols)] #firing boards
        turn = 0 #reset the turn back to p1's turn, 1 - turn is the enemy turn
        places_fired = [[], []] #0 will be the places p1 shot, 1 will be the places p2 shot
        num_ships_destroyed = [0, 0]

        #actual shooting starts
        while (True):
            #print out firing and placement board before turn
            print("{0}'s Firing Board".format(players[turn]))
            firing_boards[turn].print_board()
            print("{0}'s Placement Board".format(players[turn]))
            placement_boards[turn].print_board()

            #start asking where they want to shoot
            print("{0}, enter the location you want to fire at in the form row col: ".format(players[turn]), end='')
            location_str = input()
            location = self.coords_to_intlist(location_str)
            row = int(location[0])
            col = int(location[1])

            #IF THEY ALREADY FIRED AT THAT POS OR THE POS IS NOT ON ENEMY BOARD ASK AGAIN
            fired = location_str in places_fired[turn]
            on_enemy_board = placement_boards[1-turn].is_on_board(row, col)
            while (fired == True) or (on_enemy_board == False):
                print("{0} enter the location you want to fire at in the form row col: ".format(players[turn]), end='')
                location_str = input()
                location = self.coords_to_intlist(location_str)
                row = int(location[0])
                col = int(location[1])
                fired = location_str in places_fired[turn]
                on_enemy_board = placement_boards[1 - turn].is_on_board(row, col)

            places_fired[turn].append(location_str) #places fired will track the positions entered, so if they entered a position they already did then it wont work
            pos = placement_boards[1-turn].get_value(row, col) #VALUE OF ENTERED POS AT ENEMY BOARD
            # ===========
            # === HIT ===
            # ===========
            if pos != '*':
                ship_name = placement_boards[1-turn].get_value(row, col)
                print("{0} hit {1}'s {2}!".format(players[turn], players[1-turn], ship_name))
                firing_boards[turn].set_value(row, col, 'X') #X represents a hit
                placement_boards[1-turn].set_value(row, col, 'X') #X represents a hit

                #if the ship was just destroyed, then print it out
                if self.ship_killed(placement_boards[1 - turn], row, col, ship_name):
                    print("{0} destroyed {1}'s {2}!".format(players[turn], players[1-turn], ship_name))
                    num_ships_destroyed[turn] += 1
                    #IF ALL SHIPS HAVE BEEN DESTROYED, END GAME
                    if(num_ships_destroyed[turn] >= config.num_ships):
                        #at end of game print out winners board and then that they won
                        print("{0}'s Firing Board".format(players[turn]))
                        firing_boards[turn].print_board()
                        print("{0}'s Placement Board".format(players[turn]))
                        placement_boards[turn].print_board()
                        print(players[turn], "won!")
                        break #the loop runs forever until we get here, which is when someone wins

            # ============
            # === MISS ===
            # ============
            if pos == '*':
                print("{0} missed.".format(players[turn]))
                firing_boards[turn].set_value(row, col, 'O')  # O represents a miss
                placement_boards[turn - 1].set_value(row, col, 'O')  # O represents a miss

            turn = 1 - turn
