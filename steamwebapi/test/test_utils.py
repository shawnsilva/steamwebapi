import unittest
from steamwebapi.utils import gid_32_to_64_bit

KNOWN_32_BIT_GID = 1606484
KNOWN_64_BIT_GID = 103582791431127892

class TestUtils(unittest.TestCase):
	def test_gid_32_to_64_bit(self):
		converted_id = gid_32_to_64_bit(KNOWN_32_BIT_GID)
		self.assertEqual(converted_id, KNOWN_64_BIT_GID)
