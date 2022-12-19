import random
import pygame


# allow player to pick heads or tails

class CoinFlipGame:
    def __init__(self, min_bet: int, max_bet: int):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.balance = 0


    # Initialize Pygame
    pygame.init()

    # Set the window size and title
    screen = pygame.display.set_mode((1100, 600))
    pygame.display.set_caption("Coin Flip Game")

    # Set the font and font size
    font = pygame.font.Font(None, 36)

    def start_coin_game(self):
        while True:
            # Display the starting message
            text = self.font.render(
                f"Starting a new game of Coin Flip with a minimum bet of {self.min_bet} and a maximum bet of {self.max_bet}",
                True, (255, 255, 255))
            self.screen.fill((0, 0, 0))

            self.screen.blit(text, (10, 10))
            pygame.display.flip()

            # Get the player's bet
            bet = self.get_bet()

            while True:
                choice = input("Please pick 'heads' or 'tails': ")
                if choice.lower() in ["heads", "tails"]:
                    break
                else:
                    # Display the error message
                    text = font.render("Invalid choice. Please enter 'heads' or 'tails'.", True, (255, 255, 255))
                    screen.blit(text, (10, 50))
                    pygame.display.flip()

            # Flip the coin
            result = self.flip_coin()

            # Calculate the player's new balance
            self.balance += bet if result == choice else -bet

            # Display the result message
            text = self.font.render(f"The coin landed on {result}! Your new balance is {self.balance}", True,
                               (255, 255, 255))
            self.screen.blit(text, (10, 90))
            pygame.display.flip()

            # Ask the player if they want to play again
            # play_again = input("Do you want to play again (yes/no)? ").lower()






            is_play_again = self.prompt_is_play_again()
            if not is_play_again:
                break
    #
    def prompt_is_play_again(self) -> bool:
        while True:
            choice = input("Would you like to flip again (yes/y or no/n)? ")
            if choice.lower() in ["yes", "y"]:
                print("Let's go again!")
                return True
            elif choice.lower() in ["no", "n"]:
                print("Thank you for playing!")
                return False
            else:
                text = self.font.render("Wrong input. Please enter 'yes' or 'no'.", True, (255, 255, 255))
                screen.blit(text, (10, 130))
                pygame.display.flip()

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

    def draw(self,screen):
        screen.blit(self.text, self.text_rect)

# Create a new CoinFlipGame with a minimum bet of 10 and a maximum bet of 100
coin_flip_game = CoinFlipGame(50, 1000)

# Play the game
coin_flip_game.start_coin_game()