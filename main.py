class Board:
  def __init__(self):
      self.board = [[' ' for _ in range(3)] for _ in range(3)]

  def print_board(self):
      for row in self.board:
          print('|'.join(row))
          print('-' * 5)

  def make_move(self, row, col, symbol):
      if self.board[row][col] == ' ':
          self.board[row][col] = symbol
          return True
      return False

  def check_winner(self, symbol):
      # Check rows
      for row in range(3):
          if all(self.board[row][col] == symbol for col in range(3)):
              return True
      # Check columns
      for col in range(3):
          if all(self.board[row][col] == symbol for row in range(3)):
              return True
      # Check diagonals
      if all(self.board[i][i] == symbol for i in range(3)):
          return True
      if all(self.board[i][2 - i] == symbol for i in range(3)):
          return True
      return False

  def is_full(self):
      return all(self.board[row][col] != ' ' for row in range(3) for col in range(3))


class Player:
  def __init__(self, symbol):
      self.symbol = symbol

  def get_move(self, board):
      raise NotImplementedError("This method should be overridden in subclasses")


class HumanPlayer(Player):
    def get_move(self, board):
        while True:
            try:
                # Ask user for their move
                row, col = map(int, input(f"Enter your move (row, col) for {self.symbol}: ").split())

                # Convert the input from 1-based index to 0-based index
                row -= 1
                col -= 1

                # Make move if valid
                if board.make_move(row, col, self.symbol):
                    return
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Invalid input, please enter two integers for row and col.")


class AIPlayer(Player):
    def get_move(self, board):
        best_move = self.find_best_move(board)
        board.make_move(best_move[0], best_move[1], self.symbol)

    def find_best_move(self, board):
        best_score = float('-inf')
        best_move = None

        # Iterate through each cell on the board
        for row in range(3):
            for col in range(3):
                if board.board[row][col] == ' ':
                    # Temporarily make a move
                    board.board[row][col] = self.symbol
                    # Calculate the score of the move using Minimax
                    score = self.minimax(board, 0, False)
                    # Undo the move
                    board.board[row][col] = ' '

                    # Update the best score and move if this move is better
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move

    def minimax(self, board, depth, is_maximizing):
        # Check if there's a winner
        if board.check_winner(self.symbol):
            return 1  # AI wins
        if board.check_winner(self.opponent_symbol()):
            return -1  # Opponent wins
        if board.is_full():
            return 0  # Draw

        # Minimax algorithm
        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = self.symbol
                        score = self.minimax(board, depth + 1, False)
                        board.board[row][col] = ' '
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = self.opponent_symbol()
                        score = self.minimax(board, depth + 1, True)
                        board.board[row][col] = ' '
                        best_score = min(best_score, score)
            return best_score

    def opponent_symbol(self):
        return 'X' if self.symbol == 'O' else 'O'



class GameFactory:
  @staticmethod
  def create_game(player1, player2):
      return Game(player1, player2)


class Game:
  _instance = None  # Singleton pattern

  def __new__(cls, player1=None, player2=None):
      if cls._instance is None:
          cls._instance = super().__new__(cls)
      return cls._instance

  def __init__(self, player1=None, player2=None):
      self.board = Board()
      self.player1 = player1
      self.player2 = player2
      self.current_player = self.player1

  def switch_player(self):
      if self.current_player == self.player1:
          self.current_player = self.player2
      else:
          self.current_player = self.player1

  def play_game(self):
      self.board.print_board()
      while not self.board.is_full():
          self.current_player.get_move(self.board)
          self.board.print_board()
          if self.board.check_winner(self.current_player.symbol):
              print(f"{self.current_player.symbol} wins!")
              return
          self.switch_player()
      print("It's a draw!")


def main():
  # Create players and game
  player1 = HumanPlayer('X')
  player2 = AIPlayer('O')
  game = GameFactory.create_game(player1, player2)

  # Play the game
  game.play_game()


if __name__ == "__main__":
  main()
