Change Log
~~~~~~~~~~

September 10, 2022 - v0.1.4
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Some PRs to fix bugs

November 2, 2016 - v0.1.3
^^^^^^^^^^^^^^^^^^^^^^^^^

Bugs
....

* Fixed passing API key when instantiating (`#1 <https://github.com/shawnsilva/steamwebapi/pull/1>`_)

December 29, 2015 - v0.1.2
^^^^^^^^^^^^^^^^^^^^^^^^^^

Mostly bug fixes as described below.

Changes
.......

* Switched to reST instead of markdown to work with pypi

Bugs
....

* Fixed issue with profile generation where there was no attribute 'games' if there was no game history
* Prevent an 'invalid' primaryclanid being set which is returned on some accounts. For example ID 103582791429521408 is returned, which is 0x170000000000000 in hex. The lower 32 bits are used for the actual group/clan id and in this case they are '0'.
* Not all responses for recently played games return attributes for 'name' or image paths. This seems to mostly be limited time betas.

November 27, 2015 - v0.1.1
^^^^^^^^^^^^^^^^^^^^^^^^^^

* API key must be set via the environment variable ``STEAM_API_KEY``
* When json format is requested, it is now automatically parsed

July 05, 2013 - v0.1.0
^^^^^^^^^^^^^^^^^^^^^^

* Initial script creation.
