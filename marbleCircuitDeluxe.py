class Game():
    def __init__(self, board):
        self.board = board
        self.outcomes = [0, 0, 0, 0, 0, 0]
    
    def simulateBoard(self):
        self.calcBallPath(4, 0, '>')
        self.calcBallPath(3, 0, '>')
        self.calcBallPath(2, 0, '>')
        self.calcBallPath(1, 0, '>')
        self.calcBallPath(0, 0, '>')
        self.calcBallPath(0, 0, 'v')
        self.calcBallPath(0, 1, 'v')
        self.calcBallPath(0, 2, 'v')
        self.calcBallPath(0, 3, 'v')
        self.calcBallPath(0, 4, 'v')
        return ''.join(map(str, self.outcomes))

    
    def calcBallPath(self, row, col, dir):
        

        # If current ball positon is outside board, add to appropriate outcome
        if row == len(self.board):
            self.outcomes[0] += 1
            return
        elif col == len(self.board[row]):
            self.outcomes[col] += 1
            return

        # Assign piece based on board position
        piece = self.board[row][col]

        # Calculate ball movement
        if piece == '' or piece == 'o':
            return
        elif piece == 'v':
            row += 1
            dir = 'v'
        elif piece == '>':
            col += 1
            dir = '>'
        elif dir == 'v':
            if piece == '+':
                row += 1
                dir = 'v'
            elif piece == 'x':
                col += 1
                dir = '>'
        elif dir == '>':
            if piece == 'x':
                row += 1
                dir = 'v'
            elif piece == '+':
                col += 1
                dir = '>'

        return self.calcBallPath(row, col, dir)

#   |-------------------------------------------------------------------------------|
#   | Symbol representations of each piece type                                     |
#   |---------------|---------------|---------------|---------------|---------------|
#   |       +       |       x       |       v       |       >       |       o       |
#   |---------------|---------------|---------------|---------------|---------------|
#   |   #       #   |   #       #   |   #       #   |   #       #   |   #       #   |
#   |     #   #     |     #   #     |     #   #     |     #   #     |     #   #     |
#   |       #       |      # #      |       #       |       #       |    #######    |
#   |     #   #     |     #   #     |     #         |         #     |     #####     |
#   |   #       #   |   #       #   |   #           |           #   |               |
#   |---------------|---------------|---------------|---------------|---------------|

class PuzzleGenerator():
    def __init__(self):
        self.pieces = ['+', 'x', '>', 'v', 'o']
        self.outcomeMap = {}
        self.board =    [
                            ['', '', '', '', ''],
                            ['', '', '', ''],
                            ['', '', ''],
                            ['', ''],
                            ['']
                        ]
        self.puzzleCount = 0
    
    def runFullSimulation(self):
        self.generateCombinations(self.board, 0, 0)
        
        totalCombos = 0
        counter = 1
        sortedOutcomes = sorted(self.outcomeMap.items(), key=lambda item: (item[1], item[0]))
        flippedOutcomes = set()
        finalOutcomes = {}
        flipResult = True

        for key, value in sortedOutcomes:
            reversedKey = key[::-1]
            if key not in flippedOutcomes and reversedKey not in flippedOutcomes:
                finalOutcomes[key if flipResult else reversedKey] = value
                flippedOutcomes.add(key)
                flippedOutcomes.add(reversedKey)
                flipResult = not flipResult



        for key, value in finalOutcomes.items():
            totalCombos += value
            print(f"{counter}\t{key}\t{value}")
            counter += 1
        
        print('\nTotal combos ' + str(totalCombos))
    
    def isBoardValid(self, board):
        pieceMap = {'+': 3, 'x': 3, '>': 3, 'v': 3, 'o': 3}
        for row in range(0, len(board)):
            for col in range (0, len(board[row])):
                piece = board[row][col]
                if piece == '':
                    return True
                pieceMap[piece] -= 1
                if (pieceMap[piece] < 0):
                    return False
        self.puzzleCount += 1
        if self.puzzleCount % 336336 == 0:
            print(f"{(self.puzzleCount / 336336000) * 100:.2f}%")
            #Note: 168168000 = 2*15!/(3!)^5 = total number of permutations

        return True



    
    #Recursively generate all board configurations
    def generateCombinations(self, board, row=0, col=0):
        if (not self.isBoardValid(board)):
            return
        
        # Simulate ball paths for this board configuration
        if row == len(board):
            game = Game(self.board)
            result = game.simulateBoard()
            self.outcomeMap[result] = self.outcomeMap.get(result, 0) + 1
            return
        
        # Move to next row if current row is finished
        if col == len(board[row]):
            self.generateCombinations(board, row + 1, 0)
            return
        
        # For each possible piece in the list, set the current position
        for piece in self.pieces:
            board[row][col] = piece
            # Recursively set the next cell
            self.generateCombinations(board, row, col + 1)
            # Backtrack to explore other possibilities
            board[row][col] = ''  # Reset to an empty state to explore the next piece



# Run the game simulation
if __name__ == "__main__":
    puzzle = PuzzleGenerator()
    puzzle.runFullSimulation()
