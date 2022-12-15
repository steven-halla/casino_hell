import random

class CoinFlipGame:
  def __init__(self, min_bet: int, max_bet: int):
    self.min_bet = min_bet
    self.max_bet = max_bet
    self.balance = 0

  def start_game(self):
    while True:
        print(f"Starting a new game of Coin Flip with a minimum bet of {self.min_bet} and a maximum bet of {self.max_bet}")

        # Get the player's bet
        bet = self.get_bet()

        # Flip the coin
        result = self.flip_coin()

        # Calculate the player's new balance
        self.balance += bet if result == "heads" else -bet

        # Print the result
        print(f"The coin landed on {result}! Your new balance is {self.balance}")

        # Ask the player if they want to play again
        # play_again = input("Do you want to play again (yes/no)? ").lower()

        choice = input("Would you like to flip again (yes/y or no/n)? ")
        if choice.lower() in ["yes", "y"]:
          print("lets go again!")
          continue
        elif choice.lower() in ["no", "n"]:
          print("Thank you for playing!")
          break


  def get_bet(self):
    while True:
      try:
        bet = int(input("How much would you like to bet? "))
        # Check if the bet is within the minimum and maximum limits
        if self.min_bet <= bet <= self.max_bet:
          return bet
        else:
          print(f"Please enter a bet between {self.min_bet} and {self.max_bet}")
      except ValueError:
        print("Please enter a valid bet amount")

  def flip_coin(self):
    return "heads" if random.randint(0, 1) == 0 else "tails"

# Create a new CoinFlipGame with a minimum bet of 10 and a maximum bet of 100
game = CoinFlipGame(50, 1000)

# Play the game
game.start_game()
