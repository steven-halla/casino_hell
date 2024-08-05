

class CutSceneMovement:
    def __init__(self):
        pass

    def move_up(self, character):
        character.setPosition(character.position.x, character.position.y - 1)
        # Add any additional logic or parameters if needed


