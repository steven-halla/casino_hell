import sys
import unittest

# Add src to PYTHONPATH
sys.path.insert(0, './src')  # Adjust this path if necessary

from game_constants.equipment import Equipment
from game_state import GameState


class EquipmentToPlayerTest(unittest.TestCase):

    def setUp(self):
        # Initialize GameState
        self.game_state = GameState()
        self.player = self.game_state.player
        self.player.items = []  # Ensure player.items is empty before each test

    def test_add_equipment_to_player(self):
        """Test that equipment is correctly added to the player's items and no duplicates are created."""
        player = self.player

        # Ensure the player's items list is initially empty
        self.assertEqual(len(player.items), 0)

        # Add a piece of equipment to the player
        Equipment.add_equipment_to_player(player, Equipment.BLACK_JACK_HAT)
        self.assertIn(Equipment.BLACK_JACK_HAT.value, player.items)

        # Attempt to add the same equipment again
        Equipment.add_equipment_to_player(player, Equipment.BLACK_JACK_HAT)
        self.assertEqual(player.items.count(Equipment.BLACK_JACK_HAT.value), 1)

        # Add another piece of equipment
        Equipment.add_equipment_to_player(player, Equipment.HIPPO_SHOES)
        self.assertIn(Equipment.HIPPO_SHOES.value, player.items)
        self.assertEqual(len(player.items), 2)

if __name__ == '__main__':
    unittest.main()
