# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright (C) 2013-2015  Shawn Silva
# ------------------------------------
# This file is part of steamwebapi.
#
# steamwebapi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
