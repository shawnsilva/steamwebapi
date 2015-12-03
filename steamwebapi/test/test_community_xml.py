import unittest
import xml.etree.ElementTree as ET
from steamwebapi.api import SteamCommunityXML

# Current Steam ID for user 'vanityURL'
STEAM_USER_ID = '76561198148848265'
# Current Steam Group ID for 'Slackware'
STEAM_GROUP_ID = '103582791431127892'

class TestCommunityXml(unittest.TestCase):
	def test_user_xml(self):
		steamcomm = SteamCommunityXML()
		data = steamcomm.get_user_info('vanityURL')
		xml = ET.ElementTree(ET.fromstring(data))
		self.assertEqual(xml.getroot().tag, 'profile')
		self.assertEqual(xml.findtext("steamID64"), STEAM_USER_ID)

	def test_group_xml(self):
		steamcomm = SteamCommunityXML()
		data = steamcomm.get_group_info('slackware')
		xml = ET.ElementTree(ET.fromstring(data))
		self.assertEqual(xml.getroot().tag, 'memberList')
		self.assertEqual(xml.findtext("groupID64"), STEAM_GROUP_ID)
