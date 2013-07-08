#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# api.py
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
import sys

PYMAJORVER, PYMINORVER, PYMICROVER, PYRELEASELEVEL, PYSERIAL = sys.version_info
if PYMAJORVER == 3 and PYMINORVER >= 2:
    #Python >= 3.2
    from urllib.request import urlopen
    from urllib.parse import urlencode
elif PYMAJORVER == 2 and (PYMINORVER == 7 or PYMINORVER == 6):
    #Python 2.6 or 2.7
    from urllib2 import urlopen
    from urllib import urlencode
    import printfunction
else:
    raise PythonVersionError("Python Version 2.6 or greater required.")


APIKEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #Your Steam API Key
DEFAULTFORMAT = 'json' #Set to: xml, json, or vdf
DEFAULTLANG = 'en' #Default language

class _SteamWebAPI(object):
    def __init__(self):
        self.apikey = APIKEY
        self.format = DEFAULTFORMAT
        self.language = DEFAULTLANG

    def create_request_url(self, interface, method, version, parameters):
        """Create the URL to submit to the Steam Web API

        interface: Steam Web API interface containing methods.
        method: The method to call.
        version: The version of the method.
        paramters: Parameters to supply to the method.

        """
        if 'format' in parameters:
            parameters['key'] = self.apikey
        else:
            parameters.update({'key' : self.apikey, 'format' : self.format})
        version = "v%04d" % (version)
        url = "http://api.steampowered.com/%s/%s/%s/?%s" % (interface, method,
            version, urlencode(parameters))
        return url

    def retrieve_request(self, url):
        """Open the given url and decode and return the response

        url: The url to open.

        """
        try:
            data = urlopen(url)
        except:
            print("Error Retrieving Data from Steam")
            sys.exit(2)
        return data.read().decode('utf-8')

class ISteamUser(_SteamWebAPI):
    def __init__(self):
        self.interface = 'ISteamUser'
        super(ISteamUser, self).__init__()

    def get_friends_list(self, steamID, relationship='all', format=None):
        """Request the friends list of a given steam ID filtered by role.

        steamID: The user ID
        relationship: Type of friend to request (all, friend)
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID, 'relationship' : relationship}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetFriendsList', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

    def get_player_bans(self, steamIDS, format=None):
        """Request the communities a steam id is banned in.

        steamIDS: Comma-delimited list of SteamIDs
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'steamids' : steamIDS}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetPlayerBans', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

    def get_player_summaries(self, steamIDS, format=None):
        """
        Get summaries of steam accounts.

        steamIDS: Comma-delimited list of SteamIDs (max: 100)
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'steamids' : steamIDS}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetPlayerSummaries', 2,
            parameters)
        data = self.retrieve_request(url)
        return data

    def get_user_group_list(self, steamID, format=None):
        """Request a list of groups a user is subscribed to.

        steamID: User ID
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetUserGroupList', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

    def resolve_vanity_url(self, vanityURL, format=None):
        """Request the steam id associated with a vanity url.

        vanityURL: The users vanity URL
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'vanityurl' : vanityURL}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'ResolveVanityUrl', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

class ISteamUserStats(_SteamWebAPI):
    def __init__(self):
        self.interface = 'ISteamUserStats'
        super(ISteamUserStats, self).__init__()

    def get_global_achievement_percentages_for_app(self, gameID, format=None):
        """Request statistics showing global achievements that have been 
        unlocked.

        gameID: The id of the game.
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'gameid' : gameID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface,
            'GetGlobalAchievementPercentagesForApp', 2, parameters)
        data = self.retrieve_request(url)
        return data

    def get_global_stats_for_game(self, appID, count, names, startdate,
            enddate, format=None):
        """Request global stats for a give game.

        appID: The app ID
        count: Number of stats to get.
        names: A list of names of stats to get.
        startdate: The start time to gather stats. Unix timestamp
        enddate: The end time to gather stats. Unix timestamp
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {
            'appid' : appID,
            'count' : count,
            'startdate' : startdate,
            'enddate' : enddate
            }
        count = 0
        for name in names:
            param = "name[" + str(count) + "]"
            parameters[param] = name
            count += 1
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetGlobalStatsForGame', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

    def get_number_of_current_players(self, appID, format=None):
        """Request the current number of players for a given app.

        appID: The app ID
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'appid' : appID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface,
            'GetNumberOfCurrentPlayers', 1, parameters)
        data = self.retrieve_request(url)
        return data

    def get_player_achievements(self, steamID, appID, language=None,
            format=None):
        """Request the achievements for a given app and steam id.

        steamID: Users steam ID
        appID: The app id
        language: The language to return the results in. None uses defualt.
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID, 'appid' : appID}
        if format is not None:
            parameters['format'] = format
        if language is not None:
            parameters['l'] = language
        else:
            parameters['l'] = self.language
        url = self.create_request_url(self.interface, 'GetPlayerAchievements', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

    def get_schema_for_game(self, appID, language=None, format=None):
        """Request the available achievements and stats for a game.

        appID: The app id
        language: The language to return the results in. None uses defualt.
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'appid' : appID}
        if format is not None:
            parameters['format'] = format
        if language is not None:
            parameters['l'] = language
        else:
            parameters['l'] = self.language
        url = self.create_request_url(self.interface, 'GetSchemaForGame', 2,
            parameters)
        data = self.retrieve_request(url)
        return data

    def get_user_stats_for_game(self, steamID, appID, format=None):
        """Request the user stats for a given game.

        steamID: The users ID
        appID: The app id
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID, 'appid' : appID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetUserStatsForGame', 2,
            parameters)
        data = self.retrieve_request(url)
        return data

class IPlayerService(_SteamWebAPI):
    def __init__(self):
        self.interface = 'IPlayerService'
        super(IPlayerService, self).__init__()

    def get_recently_played_games(self, steamID, count=0, format=None):
        """Request a list of recently played games by a given steam id.

        steamID: The users ID
        count: Number of games to return. (0 is all recent games.)
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID, 'count' : count}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetRecentlyPlayedGames', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

    def get_owned_games(self, steamID, include_appinfo=1,
            include_played_free_games=0, appids_filter=None, format=None):
        """Request a list of games owned by a given steam id.

        steamID: The users id
        include_appinfo: boolean.
        include_played_free_games: boolean.
        appids_filter: a json encoded list of app ids.
        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {
                    'steamid' : steamID,
                    'include_appinfo' : include_appinfo,
                    'include_played_free_games' : include_played_free_games
                    }
        if format is not None:
            parameters['format'] = format
        if appids_filter is not None:
            parameters['appids_filter'] = appids_filter
        url = self.create_request_url(self.interface, 'GetOwnedGames', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

class ISteamWebAPIUtil(_SteamWebAPI):
    def __init__(self):
        self.interface = ISteamWebAPIUtil
        super(ISteamWebAPIUtil, self).__init__()

    def get_server_info(self, format=None):
        """Request the Steam Web API status and time.

        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetServerInfo', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

    def get_supported_API_list(self, format=None):
        """Request a list of APIs that can be accessed with your APIKEY

        format: Return format. None defualts to json. (json, xml, vdf)

        """
        parameters = {}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetSupportedAPIList', 1,
            parameters)
        data = self.retrieve_request(url)
        return data

def main():
    # Tests
    import json
    steamuser = ISteamUser()
    steamid = json.loads(steamuser.resolve_vanity_url("vanityurl"))['response']['steamid']
    #jsondata = json.loads(data)
    print(steamid)
    print(json.loads(steamuser.get_player_summaries(steamid))['response']['players'])

if __name__ == "__main__":
    main()