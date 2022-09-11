# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright (C) 2013-2016  Shawn Silva
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

"""Steam Web API interaction"""

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
else:
    raise PythonVersionError("Python Version 2.6 or greater required.")

import json
import os
import re

APIKEY = os.environ.get('STEAM_API_KEY')
DEFAULTFORMAT = 'json' #Set to: xml, json, or vdf
DEFAULTLANG = 'en' #Default language

class _SteamWebAPI(object):
    def __init__(self, steam_api_key=None):
        if steam_api_key:
            self.apikey = steam_api_key
        elif not APIKEY:
            print("Steam Web API key environment variable not set, and the key wasn't supplied elsewhere.")
            sys.exit(1)
        else:
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

    def return_data(self, data, format=None):
        """Format and return data appropriate to the requested API format.

        data: The data retured by the api request

        """
        if format is None:
            format = self.format
        if format == "json":
            formatted_data = json.loads(data)
        else:
            formatted_data = data
        return formatted_data

class ISteamUser(_SteamWebAPI):
    def __init__(self, **kwargs):
        self.interface = 'ISteamUser'
        super(ISteamUser, self).__init__(**kwargs)

    def get_friends_list(self, steamID, relationship='all', format=None):
        """Request the friends list of a given steam ID filtered by role.

        steamID: The user ID
        relationship: Type of friend to request (all, friend)
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID, 'relationship' : relationship}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetFriendsList', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def get_player_bans(self, steamIDS, format=None):
        """Request the communities a steam id is banned in.

        steamIDS: Comma-delimited list of SteamIDs
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamids' : steamIDS}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetPlayerBans', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def get_player_summaries(self, steamIDS, format=None):
        """
        Get summaries of steam accounts.

        steamIDS: Comma-delimited list of SteamIDs (max: 100)
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamids' : steamIDS}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetPlayerSummaries', 2,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def get_user_group_list(self, steamID, format=None):
        """Request a list of groups a user is subscribed to.

        steamID: User ID
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetUserGroupList', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def resolve_vanity_url(self, vanityURL, url_type=1, format=None):
        """Request the steam id associated with a vanity url.

        vanityURL: The users vanity URL
        url_type: The type of vanity URL. 1 (default): Individual profile,
                    2: Group, 3: Official game group
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'vanityurl' : vanityURL, "url_type" : url_type}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'ResolveVanityUrl', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

class ISteamUserStats(_SteamWebAPI):
    def __init__(self, **kwargs):
        self.interface = 'ISteamUserStats'
        super(ISteamUserStats, self).__init__(**kwargs)

    def get_global_achievement_percentages_for_app(self, gameID, format=None):
        """Request statistics showing global achievements that have been
        unlocked.

        gameID: The id of the game.
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'gameid' : gameID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface,
            'GetGlobalAchievementPercentagesForApp', 2, parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def get_global_stats_for_game(self, appID, count, names, startdate,
            enddate, format=None):
        """Request global stats for a give game.

        appID: The app ID
        count: Number of stats to get.
        names: A list of names of stats to get.
        startdate: The start time to gather stats. Unix timestamp
        enddate: The end time to gather stats. Unix timestamp
        format: Return format. None defaults to json. (json, xml, vdf)

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
        return self.return_data(data, format=format)

    def get_number_of_current_players(self, appID, format=None):
        """Request the current number of players for a given app.

        appID: The app ID
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'appid' : appID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface,
            'GetNumberOfCurrentPlayers', 1, parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def get_player_achievements(self, steamID, appID, language=None,
            format=None):
        """Request the achievements for a given app and steam id.

        steamID: Users steam ID
        appID: The app id
        language: The language to return the results in. None uses default.
        format: Return format. None defaults to json. (json, xml, vdf)

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
        return self.return_data(data, format=format)

    def get_schema_for_game(self, appID, language=None, format=None):
        """Request the available achievements and stats for a game.

        appID: The app id
        language: The language to return the results in. None uses default.
        format: Return format. None defaults to json. (json, xml, vdf)

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
        return self.return_data(data, format=format)

    def get_user_stats_for_game(self, steamID, appID, format=None):
        """Request the user stats for a given game.

        steamID: The users ID
        appID: The app id
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID, 'appid' : appID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetUserStatsForGame', 2,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

class IPlayerService(_SteamWebAPI):
    def __init__(self, **kwargs):
        self.interface = 'IPlayerService'
        super(IPlayerService, self).__init__(**kwargs)

    # RecordOfflinePlaytime, requires auth ticket

    def get_recently_played_games(self, steamID, count=0, format=None):
        """Request a list of recently played games by a given steam id.

        steamID: The users ID
        count: Number of games to return. (0 is all recent games.)
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID, 'count' : count}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetRecentlyPlayedGames', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def get_owned_games(self, steamID, include_appinfo=1,
            include_played_free_games=0, appids_filter=None, format=None):
        """Request a list of games owned by a given steam id.

        steamID: The users id
        include_appinfo: boolean.
        include_played_free_games: boolean.
        appids_filter: a json encoded list of app ids.
        format: Return format. None defaults to json. (json, xml, vdf)

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
        return self.return_data(data, format=format)

    def get_steam_level(self, steamID, format=None):
        """Returns the Steam Level of a user.

        steamID: The users ID
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetSteamLevel', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def get_badges(self, steamID, format=None):
        """Gets badges that are owned by a specific user

        steamID: The users ID
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetBadges', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def get_community_badge_progress(self, steamID, badgeID, format=None):
        """Gets all the quests needed to get the specified badge, and which are completed.

        steamID: The users ID
        badgeID: The badge we're asking about
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID, 'badgeid' : badgeID}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetCommunityBadgeProgress', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def is_playing_shared_game(self, steamID, appid_playing, format=None):
        """Returns valid lender SteamID if game currently played is borrowed.

        steamID: The users ID
        appid_playing: The game player is currently playing
        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {'steamid' : steamID, 'appid_playing' : appid_playing}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'IsPlayingSharedGame', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

class ISteamWebAPIUtil(_SteamWebAPI):
    def __init__(self, **kwargs):
        self.interface = 'ISteamWebAPIUtil'
        super(ISteamWebAPIUtil, self).__init__(**kwargs)

    def get_server_info(self, format=None):
        """Request the Steam Web API status and time.

        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetServerInfo', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

    def get_supported_API_list(self, format=None):
        """Request a list of APIs that can be accessed with your APIKEY

        format: Return format. None defaults to json. (json, xml, vdf)

        """
        parameters = {}
        if format is not None:
            parameters['format'] = format
        url = self.create_request_url(self.interface, 'GetSupportedAPIList', 1,
            parameters)
        data = self.retrieve_request(url)
        return self.return_data(data, format=format)

class SteamCommunityXML(_SteamWebAPI):
    USER = 0
    GROUP = 1

    def __init__(self, **kwargs):
        super(SteamCommunityXML, self).__init__(**kwargs)

    def create_request_url(self, profile_type, steamID):
        """Create the url to submit to the Steam Community XML feed."""
        regex = re.compile('^\d{17,}$')
        if regex.match(steamID):
            if profile_type == self.USER:
                url = "http://steamcommunity.com/profiles/%s/?xml=1" % (steamID)
            if profile_type == self.GROUP:
                url = "http://steamcommunity.com/gid/%s/memberslistxml/?xml=1" % (steamID)
        else:
            if profile_type == self.USER:
                url = "http://steamcommunity.com/id/%s/?xml=1" % (steamID)
            if profile_type == self.GROUP:
                url = "http://steamcommunity.com/groups/%s/memberslistxml/?xml=1" % (steamID)
        return url

    def retrieve_request(self, url):
        """Open the given url and return the response

        url: The url to open.

        """
        try:
            data = urlopen(url)
        except:
            print("Error Retrieving Data from Steam")
            sys.exit(2)
        return data.read()

    def get_user_info(self, steamID):
        """Request the Steam Community XML feed for a specific user."""
        url = self.create_request_url(self.USER, steamID)
        data = self.retrieve_request(url)
        return self.return_data(data, format='xml')

    def get_group_info(self, steamID):
        """Request the Steam Community XML feed for a specific group."""
        url = self.create_request_url(self.GROUP, steamID)
        data = self.retrieve_request(url)
        return self.return_data(data, format='xml')

def main():
    # Tests
    import json
    steamuser = ISteamUser()
    steamid = steamuser.resolve_vanity_url("vanityURL")['response']['steamid']
    #jsondata = json.loads(data)
    print(steamid)
    print(steamuser.get_player_summaries(steamid)['response']['players'])

    pserv = IPlayerService()
    print(pserv.get_recently_played_games(steamid))
    print(steamuser.get_user_group_list(steamid))
    steamcomm = SteamCommunityXML()
    print(steamcomm.get_user_info('vanityURL'))
    # sapi = ISteamWebAPIUtil()
    # print(sapi.get_supported_API_list())

if __name__ == "__main__":
    main()
