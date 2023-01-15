class configuration:

    #CONSTRUCTOR
    def __init__(self):
        '''Constructor, creates instance attributes with the game configuration.
            Args: none
            Returns: none
        '''
        #instance attributes
        self.board_rows = -1
        self.board_cols = -1
        self.num_ships = -1
        self.ship_types = [] #each ship is a list, length 2. first value
        self.player1_name = ''
        self.player2_name = ''
        self.board = ['']

    def read_configuration_file(self):
        '''Reads information from configuration file and assigns game information to respective variables.
            Args: none
            Returns: none
        '''
        config_path = input("Please enter the path to the configuration file for this game: ")
        f = open(config_path, "r")
        file = f.readlines()
        self.board_rows = int(file[0])
        self.board_cols = int(file[1])
        self.num_ships = int(file[2])

        for i in range(3, len(file)):
            self.ship_types.append([file[i][0], int(file[i][2])])

        f.close()

    def ask_names(self):
        '''Gets player names and assigns them to instance attributes.
            Args: none
            Returns: none
        '''
        self.player1_name = input("Player 1, please enter your name: ")
        self.player2_name = input("Player 2, please enter your name: ")
