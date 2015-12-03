"""Builds user and group profiles using the steamwebapi"""

import re

from .api import ISteamUser, IPlayerService, ISteamUserStats
from .utils import gid_32_to_64_bit

class User:
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

class Group:
    def __init__(self):
        self.groupid = None #The Group's 64bit ID
        self.groupname = None
        self.groupurl = None
        self.headline = None
        self.summary = None
        self.avatar = None
        self.avatarmedium = None
        self.avatarfull = None
        self.membercount = None
        self.membersinchat = None
        self.membersingame = None
        self.membersonline = None


def get_user_profile(user):
    userinfo = User()
    steamuser = ISteamUser()
    playerservice = IPlayerService()
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

    recent_games = playerservice.get_recently_played_games(userinfo.steamid)['response']['games']
    steam_level = playerservice.get_steam_level(userinfo.steamid)['response']['player_level']
    userinfo.recentlyplayedgames = recent_games
    userinfo.steamlevel = steam_level
    return userinfo

def main():
    user = get_user_profile("vanityURL")
    attrs = vars(user)
    print(attrs)
    #print ', '.join("%s: %s" % item for item in attrs.items())
if __name__ == "__main__":
    main()
