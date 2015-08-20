#!/usr/bin/env python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# user.py
# Version: 0.1.0
# By: Shawn Silva (ssilva at jatgam dot com)
# 
# Created: 07/05/2013
# Modified: 07/05/2013
# 
# Copyright (C) 2013  Shawn Silva
# -------------------------------
# This program is free software: you can redistribute it and/or modify
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
import re
import json
from api import ISteamUser, IPlayerService, ISteamUserStats

class UserInfo:
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

def get_user_info(user):
    userinfo = UserInfo()
    steamuser = ISteamUser()
    regex = re.compile('^\d{17}$')
    if regex.match(user):
        userinfo.steamid = user
    else:
        userinfo.steamid = json.loads(steamuser.resolve_vanity_url(user))['response']['steamid']
    usersummary = json.loads(steamuser.get_player_summaries(userinfo.steamid))['response']['players'][0]
    for key in list(usersummary.keys()):
        if isinstance(usersummary[key], int):
            exec('userinfo.' + key + ' = ' + str(usersummary[key]))
        else:
            exec('userinfo.' + key + ' = ' + '"' + usersummary[key] + '"')

    return userinfo

def main():
    user = get_user_info("vanityURLorSteamID")
    attrs = vars(user)
    print(attrs)
    #print ', '.join("%s: %s" % item for item in attrs.items())
if __name__ == "__main__":
    main()