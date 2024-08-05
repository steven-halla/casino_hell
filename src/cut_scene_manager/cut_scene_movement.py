
import time
class CutSceneMovement:
    def __init__(self):
        self.timer_start = time.time()  # Initialize timer start with the current time
        self.stop_movement_flag = False  # Flag to control movement

    def move_up(self, character):
        if not self.stop_movement_flag:  # Only move if the flag is not set
            character.setPosition(character.position.x, character.position.y - 1)

    def stop_movement(self, current_time, event_timer):
        """
        Stop movement after the specified duration.

        :param current_time: The current time.
        :param event_timer: The duration after which to stop movement.
        """
        if self.timer_start is not None and current_time - self.timer_start >= event_timer:
            # Stop all movement
            self.stop_movement_flag = True  # Set the flag to stop movement
            self.timer_start = None  # Reset timer to avoid repetitive stopping
