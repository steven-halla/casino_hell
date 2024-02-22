fix screen speed for messages so they are all consistant
THE BELOW IS WHAT THE ISSUE WAS, IT WAS THE DEMON.UPDATE(STATE) CALL
       # for demon in state.demons:
        #     demon.update(state)
        #     if demon.move_player_down:
        #         state.player.collision.y += 100  # Move player down by 100 pixels
        #         demon.move_player_down = False

The above made my messages slower, because of the update(state) call. This meant that some 
screens would have different message speeds, in this case the calls were being made faster with this in.

in the future we need to make sure that all screens operate at the same speed, for messages, movement,everything
        the below sets speed for our game loop, the below goes in init 
        self.clock = pygame.time.Clock()  # Initialize the clock

        the below goes in update
        self.clock.tick(60)

i need start screns
i need give exp function for every screen to make it easier to change exp gains
i need give money function as well to make things easier



