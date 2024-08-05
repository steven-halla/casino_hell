import time

class CutSceneMovement:
    def __init__(self):
        self.stop_movement_flag = False  # Flag to control movement
        self.movement_duration = 0  # Duration to control movement
        self.movement_start_time = None  # Start time for the movement

    def move_up(self, character, duration):
        if not self.stop_movement_flag:
            if self.movement_start_time is None:
                self.movement_start_time = time.time()

            elapsed_time = time.time() - self.movement_start_time
            if elapsed_time < duration:
                character.setPosition(character.position.x, character.position.y - 1)
            else:
                self.stop_movement_flag = True

    def move_down(self, character, duration):
        if not self.stop_movement_flag:
            if self.movement_start_time is None:
                self.movement_start_time = time.time()

            elapsed_time = time.time() - self.movement_start_time
            if elapsed_time < duration:
                character.setPosition(character.position.x, character.position.y + 1)
            else:
                self.stop_movement_flag = True

    def move_left(self, character, duration):
        if not self.stop_movement_flag:
            if self.movement_start_time is None:
                self.movement_start_time = time.time()

            elapsed_time = time.time() - self.movement_start_time
            if elapsed_time < duration:
                character.setPosition(character.position.x - 1, character.position.y)
            else:
                self.stop_movement_flag = True

    def move_right(self, character, duration):
        if not self.stop_movement_flag:
            if self.movement_start_time is None:
                self.movement_start_time = time.time()

            elapsed_time = time.time() - self.movement_start_time
            if elapsed_time < duration:
                character.setPosition(character.position.x + 1, character.position.y)
            else:
                self.stop_movement_flag = True

    def reset_movement(self):
        self.stop_movement_flag = False
        self.movement_start_time = None
