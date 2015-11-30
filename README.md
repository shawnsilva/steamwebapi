# Steam Web API [![Build Status](https://travis-ci.org/shawnsilva/steamwebapi.svg?branch=master)](https://travis-ci.org/shawnsilva/steamwebapi)
## README

### Description
This script will connect to the Steam API to retrieve information about
users/games/groups. 

### How to use

#### Install

To install, git clone the repository or download the archive from GitHub.
Then, run `python setup.py install` to have the package installed. After 
finishing the planned features the package will be available via pip.

#### Use

The following example will assume that JSON data is being returned, and you
want access to the data as returned by Valve.

```python
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
steamuserinfo = ISteamUser()
steamid = steamuserinfo.resolve_vanity_url("profileURL")['response']['steamid']
usersummary = steamuserinfo.get_player_summaries(steamid)['response']['players'][0]
```

The Steam Web API has multiple inferfaces (e.g., ISteamUser, IPlayerService)
that provide different functions. After instantiating one of the interfaces
the functions can be called with the appropriate paramenters. Each function 
returns a string of either json, xml, or vdf (valve data format). This can be
set by the `DEFAULTFORMAT` variable or changed in the paramters of the
function: `steamuserinfo.resolve_vanity_url("profileURL", format="xml")`.

Alternatively, there is a helper function available to build a "user profile".

```python
from steamwebapi import profiles
user_profile = profiles.get_user_profile("VanityURLOrSteamID")

print(vars(user_profile))
```

### Steam Web API Documentation
	* https://developer.valvesoftware.com/wiki/Steam_Web_API
	* http://wiki.teamfortress.com/wiki/WebAPI
	* https://partner.steamgames.com/documentation/community_data

###REQUIREMENTS
* Python
	* 3.5.*
	* 3.4.*
    * 3.3.*
    * 3.2.*
    * 2.7.*
    * 2.6.*
