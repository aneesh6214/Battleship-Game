class board:

    #CONSTRUCTOR
    def __init__(self, rows, cols):
        '''Constructor, creates a 2d list representing a board.
            Args:
                rows (int): number of rows in matrix
                cols (int): number of cols in matrix
            Returns: none
        '''
        #self.board = [['*'] * cols] * rows
        self.board = [['*' for i in range(cols)] for j in range(rows)]
        self.board_rows = rows
        self.board_cols = cols

    def print_board(self):
        '''Prints out the board.
            Args: none
            Returns: none
        '''
        print('  ', end='')
        for i in range(self.board_cols):
            print(i, end=' ')
            # If this is the last number in the row, print a space after it
            if i == self.board_cols - 1:
                print(' ', end='')
        print()
        i = 0
        for row in self.board:
            print(i, end=' ')
            for pos in row:
                print(pos, end=' ')
            i += 1
            print()

    def set_value(self, row, col, value):
        '''Sets a certain position to a desired value.
            Args:
                row (int): x pos in matrix
                col (int): y pos in matrix
                value (string): the desired value to set it to
            Returns: none
        '''
        self.board[row][col] = value

    def get_value(self, row, col):
        '''Returns value at specified position.
            Args:
                row (int): int x pos in matrix
                col (int): y pos in matrix
            Returns:
                string: value at the specified position.
        '''
        return self.board[row][col]

    def is_on_board(self, row, col):
        '''Check if the specified position exists on the board.
            Args:
                row (int): x pos in matrix
                col (int): y pos in matrix
            Returns:
                boolean: if the specified position exists on the board
        '''
        if row < 0 or row > self.board_rows-1:
            return False
        if col < 0 or col > self.board_cols-1:
            return False

        return True

    def get_adjacent(self, row, col):
        '''Get the values of all adjacent coordinates of a specified position.
            Args:
                row (int): x pos in matrix
                col (int): y pos in matrix
            Returns:
                list: All values adjacent to the specified position.
        '''
        # HELPER METHOD FOR get_adjacent
        def is_valid_pos(i, j, n, m):
            '''General helper method to determine if coordinates are within the bounds of a 2d list
                Args:
                    i (int): x coordinate
                    j (int): y coordinate
                    n (int): # of rows in the 2d list
                    m (int): # of cols in the 2d list
                Returns:
                    boolean: if the specified position is valid
            '''
            if (i < 0 or j < 0 or i > n - 1 or j > m - 1):
                return False
            return True

        n = len(self.board)
        m = len(self.board[0])

        # array where all adjacent elements are stored
        out = []

        # check all possible adjacent pos
        if (is_valid_pos(row - 1, col - 1, n, m)):
            out.append(self.board[row - 1][col - 1])
        if (is_valid_pos(row - 1, col, n, m)):
            out.append(self.board[row - 1][col])
        if (is_valid_pos(row - 1, col + 1, n, m)):
            out.append(self.board[row - 1][col + 1])
        if (is_valid_pos(row, col - 1, n, m)):
            out.append(self.board[row][col - 1])
        if (is_valid_pos(row, col + 1, n, m)):
            out.append(self.board[row][col + 1])
        if (is_valid_pos(row + 1, col - 1, n, m)):
            out.append(self.board[row + 1][col - 1])
        if (is_valid_pos(row + 1, col, n, m)):
            out.append(self.board[row + 1][col])
        if (is_valid_pos(row + 1, col + 1, n, m)):
            out.append(self.board[row + 1][col + 1])

        return out
