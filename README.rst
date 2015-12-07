Steam Web API 
-------------

|buildstatus|

This script will connect to the Steam API to retrieve information about
users/games/groups. 

How to use
~~~~~~~~~~

Install
^^^^^^^

To install, git clone the repository or download the archive from GitHub.
Then, run ``python setup.py install`` to have the package installed. You can also
get the latest release by using ``pip install steamwebapi``.

Use
^^^

Currently, to use steamwebapi you must supply a Steam API key. There are two
ways to do that currently. First, you can set an environment variable called
``STEAM_API_KEY`` to your specific key value and the steamwebapi will use that.
Otherwise, when instantiating an steam interface object you can pass 
``steam_api_key`` in with the API key as its value. For example:

.. code:: python

    steamuserinfo = ISteamUser(steam_api_key='YOURAPIKEY')


The following example will assume that JSON data is being returned, and you
want access to the data as returned by Valve.

.. code:: python

    from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
    steamuserinfo = ISteamUser()
    steamid = steamuserinfo.resolve_vanity_url("profileURL")['response']['steamid']
    usersummary = steamuserinfo.get_player_summaries(steamid)['response']['players'][0]


The Steam Web API has multiple inferfaces (e.g., ISteamUser, IPlayerService)
that provide different functions. After instantiating one of the interfaces
the functions can be called with the appropriate paramenters. Each function 
returns a string of either json, xml, or vdf (valve data format). This can be
set by the ``DEFAULTFORMAT`` variable or changed in the paramters of the
function: ``steamuserinfo.resolve_vanity_url("profileURL", format="xml")``.

Alternatively, there is a helper function available to build a "user profile".
At the moment, to use the profile module the STEAM_API_KEY environment variable
must be set.

.. code:: python

    from steamwebapi import profiles
    user_profile = profiles.get_user_profile("VanityURLOrSteamID")

    print(vars(user_profile))


Steam Web API Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `Steam Web API <https://developer.valvesoftware.com/wiki/Steam_Web_API>`_
* `WebAPI Team Fortress Wiki <http://wiki.teamfortress.com/wiki/WebAPI>`_
* `Steam Community Data <https://partner.steamgames.com/documentation/community_data>`_

REQUIREMENTS
~~~~~~~~~~~~

* Python
    * 3.5.*
    * 3.4.*
    * 3.3.*
    * 3.2.*
    * 2.7.*
    * 2.6.*

.. |buildstatus| image:: https://travis-ci.org/shawnsilva/steamwebapi.svg?branch=master
    :target: https://travis-ci.org/shawnsilva/steamwebapi

