# Steam Web API
## README

### Description
This script will connect to the Steam Web API to retrieve information about
users/games/groups. 

### How to use

The following example will assume that JSON data is being returned.

```python
from api import ISteamUser, IPlayerService, ISteamUserStats
steamuserinfo = ISteamUser()
steamid = json.loads(steamuserinfo.resolve_vanity_url("profileURL"))['response']['steamid']
usersummary = json.loads(steamuserinfo.get_player_summaries(steamid))['response']['players'][0]
```

The Steam Web API has multiple inferfaces (e.g., ISteamUser, IPlayerService)
that provide different functions. After instantiating one of the interfaces
the functions can be called with the appropriate paramenters. Each function 
returns a string of either json, xml, or vdf (valve data format). This can be
set by the `DEFAULTFORMAT` variable or changed in the paramters of the
function: `steamuserinfo.resolve_vanity_url("profileURL", format="xml")`.

### Steam Web API Documentation
https://developer.valvesoftware.com/wiki/Steam_Web_API
http://wiki.teamfortress.com/wiki/WebAPI
https://partner.steamgames.com/documentation/community_data

###REQUIREMENTS
* Python
    * 3.3.*
    * 3.2.*
    * 2.7.*
    * 2.6.*