import unittest
from carpark_manager import CarparkManager  # Adjust the import path if needed

class TestCarparkManager(unittest.TestCase):

    def setUp(self):
        self.manager = CarparkManager(total_capacity=10)

    def test_initial_spaces(self):
        self.assertEqual(self.manager.available_spaces, 10)

    def test_incoming_car_reduces_space(self):
        self.manager.incoming_car("ABC123")
        self.assertEqual(self.manager.available_spaces, 9)

    def test_outgoing_car_increases_space(self):
        self.manager.incoming_car("XYZ987")  # Occupy one space first
        self.manager.outgoing_car("XYZ987")
        self.assertEqual(self.manager.available_spaces, 10)

    def test_car_park_full(self):
        for i in range(10):  # Fill all spaces
            self.manager.incoming_car(f"CAR{i}")
        self.assertEqual(self.manager.available_spaces, 0)
        self.manager.incoming_car("OVERFLOW")
        self.assertEqual(self.manager.available_spaces, 0)  # Should not go negative

    def test_car_park_empty(self):
        self.manager.outgoing_car("LONE123")  # Already empty
        self.assertEqual(self.manager.available_spaces, 10)  # Should not exceed capacity

    def test_temperature_update(self):
        self.manager.temperature_reading(31.6)
        self.assertAlmostEqual(self.manager.temperature, 31.6, places=1)

if __name__ == "__main__":
    unittest.main()