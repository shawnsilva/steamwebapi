import unittest
import xml.etree.ElementTree as ET
from steamwebapi.api import SteamCommunityXML

# Current Steam ID for user 'vanityURL'
STEAMID = '76561198148848265'

class TestCommunityXml(unittest.TestCase):
	def test_community_xml(self):
		steamcomm = SteamCommunityXML()
		data = steamcomm.get_community_info('vanityURL')
		xml = ET.ElementTree(ET.fromstring(data))
		self.assertEqual(xml.getroot().tag, 'profile')
		self.assertEqual(xml.findtext("steamID64"), STEAMID)