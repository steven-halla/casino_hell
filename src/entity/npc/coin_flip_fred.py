class CoinFlipFred(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.current_message_index = -1
        self.messages = ["You need at least 50 Hell coins to play", "Did you hear I use a weighted coin? It's a lie. ", "Press the T key in order to start a battle with me."]
        self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)
        self.start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_delay = 500  # input delay in milliseconds
        self.input_time = 0  # time when input was last read

    def update(self, state):
        super().update(state)
        distance = math.sqrt(
            (state.player.collision.x - self.collision.x) ** 2 + (state.player.collision.y - self.collision.y) ** 2)

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # If the T key is pressed and the input delay has passed
        if self.isSpeaking and state.controller.isAPressed and current_time - self.input_time >= self.input_delay:

            self.input_time = current_time  # update the input time

            # Update the current message
            self.current_message_index += 1
            if self.current_message_index >= len(self.messages):
                self.current_message_index = 0
            self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)

        elif 48 >= distance <= state.player.collision.width + state.player.collision.height + self.collision.width + self.collision.height and state.controller.isTPressed and current_time - self.input_time >= self.input_delay and state.coinFlipScreen.coinFlipFredMoney > 0:
            state.currentScreen = state.coinFlipFredScreen
            state.coinFlipScreenFred.start(state)
        elif state.coinFlipScreenFred.coinFlipFredMoney <= 0:
            print("coin flip freddy is defeated already move on you vulture")

    def draw(self, state):
        pygame.draw.rect(state.DISPLAY, self.color, self.collision.toTuple())

        # Display the current message if self.isSpeaking is True
        if self.isSpeaking:
            message = pygame.display.get_surface().blit(self.message, (10, 10))
