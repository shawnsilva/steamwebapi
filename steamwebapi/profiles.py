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

"""Builds user and group profiles using the steamwebapi"""

import re
import xml.etree.ElementTree as ET

from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats, SteamCommunityXML
from steamwebapi.utils import gid_32_to_64_bit

class User(object):
    VisibilityState = {1 : "Private", 2 : "Friends Only", 3 : "Friends of Friends", 4 : "Users Only", 5 : "Public"}
    PersonaState = {0 : "Offline", 1 : "Online", 2 : "Busy", 3 : "Away", 4 : "Snooze", 5 : "Looking to Trade", 6 : "Looking to Play"}

    def __init__(self):
        self.steamid = None #The user's 64 bit ID
        self._communityvisibilitystate = None #An integer that describes the access setting of the profile
        self.profilestate = None #If set to 1 the user has configured the profile.
        self.personaname = None #User's display name.
        self.lastlogoff = None #A unix timestamp of when the user was last online.
        self.profileurl = None #The URL to the user's Steam Community profile.
        self.avatar = None #A 32x32 image
        self.avatarmedium = None #A 64x64 image
        self.avatarfull = None #A 184x184 image
        self._personastate = None #The user's status
        #The Following may not be present
        self.commentpermission = None #If present the profile allows public comments.
        self.realname = None #The user's real name.
        self.primaryclanid = None #The 64 bit ID of the user's primary group.
        self.timecreated = None #A unix timestamp of the date the profile was created.
        self.loccountrycode = None #ISO 3166 code of where the user is located.
        self.locstatecode = None #Variable length code representing the state the user is located in.
        self.loccityid = None #An integer ID internal to Steam representing the user's city.
        self.gameid = None #If the user is in game this will be set to it's app ID as a string.
        self.gameextrainfo = None #The title of the game.
        self.gameserverip = None #The server URL given as an IP address and port number separated by a colon, this will not be present or set to "0.0.0.0:0" if none is available.

        self.profileurlname = None

        self.steamlevel = None
        self.recentlyplayedgames = None

    @property
    def communityvisibilitystate(self):
        """Return the Visibility State of the Users Profile"""
        if self._communityvisibilitystate == None:
            return None
        elif self._communityvisibilitystate in self.VisibilityState:
            return self.VisibilityState[self._communityvisibilitystate]
        else:
            #Invalid State
            return None

    @communityvisibilitystate.setter
    def communityvisibilitystate(self, value):
        self._communityvisibilitystate = value

    @property
    def personastate(self):
        """Return the Persona State of the Users Profile"""
        if self._personastate == None:
            return None
        elif self._personastate in self.PersonaState:
            return self.PersonaState[self._personastate]
        else:
            #Invalid State
            return None

    @personastate.setter
    def personastate(self, value):
        self._personastate = value

class Group(object):
    def __init__(self):
        self.groupid = None #The Group's 64bit ID
        self.groupname = None
        self.groupurl = None
        self.headline = None
        self.summary = None
        self.avataricon = None
        self.avatarmedium = None
        self.avatarfull = None
        self.membercount = None
        self.membersinchat = None
        self.membersingame = None
        self.membersonline = None


def get_user_profile(user, steam_api_key=None):
    userinfo = User()
    steamuser = ISteamUser(steam_api_key=steam_api_key)
    playerservice = IPlayerService(steam_api_key=steam_api_key)
    regex = re.compile('^\d{17}$')
    if regex.match(user):
        userinfo.steamid = user
    else:
        userinfo.steamid = steamuser.resolve_vanity_url(user)['response']['steamid']
    usersummary = steamuser.get_player_summaries(userinfo.steamid)['response']['players'][0]
    for key in list(usersummary.keys()):
        if isinstance(usersummary[key], int):
            exec('userinfo.' + key + ' = ' + str(usersummary[key]))
        else:
            exec('userinfo.' + key + ' = ' + '"' + usersummary[key] + '"')

    # Group ID '103582791429521408' is often encountered.
    # In hex, that ID is '0x170000000000000' which has 0 in the
    # lower 32bits. There is no actual group ID, just the universe,
    # account type identifiers, and the instance.
    # https://developer.valvesoftware.com/wiki/SteamID
    if userinfo.primaryclanid:
        if (int(userinfo.primaryclanid) & 0x00000000FFFFFFFF) == 0:
            userinfo.primaryclanid = None

    games_response = playerservice.get_recently_played_games(userinfo.steamid)['response']
    if 'games' in games_response:
        recent_games = games_response['games']
    else:
        recent_games = []
    steam_level = playerservice.get_steam_level(userinfo.steamid)['response']['player_level']
    for game in recent_games:
        # Sometimes, games don't have keys for 'name', or 'img_*_url' apparently.
        if 'img_icon_url' in game and 'appid' in game:
            game['img_icon_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg".format(appid=game['appid'], hash=game['img_icon_url'])
            # Some games don't have keys for 'img_logo_url' and do have for 'img_icon_url'.
            if 'img_logo_url' in game:
                game['img_logo_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg".format(appid=game['appid'], hash=game['img_logo_url'])
    userinfo.recentlyplayedgames = recent_games
    userinfo.steamlevel = steam_level

    try:
        userinfo.profileurlname = re.search(r"id\/(.*)\/", userinfo.profileurl).groups()[0]
    except:
        pass

    return userinfo

def get_group_profile(group, steam_api_key=None):
    groupinfo = Group()
    steamcomm = SteamCommunityXML(steam_api_key=steam_api_key)
    re_id64 = re.compile('^\d{18}$')
    re_id32 = re.compile('^\d{7}$')
    # if re_id64.match(group):
    #     groupinfo.groupid = group
    if re_id32.match(str(group)):
        group = gid_32_to_64_bit(group)
    data = steamcomm.get_group_info(str(group))
    # Try
    group_xml = ET.ElementTree(ET.fromstring(data))
    groupinfo.groupid = group_xml.findtext("groupID64")
    group_details = group_xml.find("groupDetails")
    groupinfo.groupname = group_details.findtext("groupName")
    groupinfo.groupurl = group_details.findtext("groupURL")
    groupinfo.headline = group_details.findtext("headline")
    groupinfo.summary = group_details.findtext("summary")
    groupinfo.avataricon = group_details.findtext("avatarIcon")
    groupinfo.avatarmedium = group_details.findtext("avatarMedium")
    groupinfo.avatarfull = group_details.findtext("avatarFull")
    groupinfo.membercount = group_details.findtext("memberCount")
    groupinfo.membersinchat = group_details.findtext("membersInChat")
    groupinfo.membersingame = group_details.findtext("membersInGame")
    groupinfo.membersonline = group_details.findtext("membersOnline")
    return groupinfo


def main():
    user = get_user_profile("vanityURL")
    attrs = vars(user)
    print(attrs)
    #print ', '.join("%s: %s" % item for item in attrs.items())
if __name__ == "__main__":
    main()
