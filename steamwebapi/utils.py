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

"""Various utilities for steamwebapi and helper classes"""

from collections import namedtuple

class MyEnum(object):
	def __init__(self):
		raise TypeError("Don't instantiate enums.")

class SteamUniverse(MyEnum):
	INVALID = 0
	PUBLIC = 1
	BETA = 2
	INTERNAL = 3
	DEV = 4

class SteamAccountType(MyEnum):
	__account_values = namedtuple('__account_values', ['id','character','url','instance'])
	INVALID = __account_values(**{'id':0,'character':'I','url':None,'instance':None})
	INDIVIDUAL = __account_values(**{'id':0,'character':'U','url':'id','instance':1})
	MULTISEAT = __account_values(**{'id':2,'character':'M','url':None,'instance':None})
	GAMESERVER = __account_values(**{'id':3,'character':'G','url':None,'instance':1})
	ANONGAMESERVER = __account_values(**{'id':4,'character':'A','url':None,'instance':None})
	PENDING = __account_values(**{'id':5,'character':'P','url':None,'instance':None})
	CONTENTSERVER = __account_values(**{'id':6,'character':'C','url':None,'instance':None})
	CLAN = __account_values(**{'id':7,'character':'g','url':'gid','instance':0})
	CHAT = __account_values(**{'id':8,'character':'T','url':None,'instance':None})
	CHAT_CLAN = __account_values(**{'id':8,'character':'c','url':None,'instance':0x00080000})
	CHAT_LOBBY = __account_values(**{'id':8,'character':'L','url':None,'instance':0x00040000})
	P2PSUPERSEEDER = __account_values(**{'id':9,'character':None,'url':None,'instance':None})
	ANONUSER = __account_values(**{'id':10,'character':'a','url':None,'instance':None})

# https://developer.valvesoftware.com/wiki/SteamID
def id_32_to_64_bit(universe, account_type_id, instance, account_id):
	id_64bit = ((universe << 56) | (account_type_id << 52) | (instance << 32) | account_id )
	return id_64bit

def gid_32_to_64_bit(gid):
	id_64bit = id_32_to_64_bit(SteamUniverse.PUBLIC, SteamAccountType.CLAN.id, SteamAccountType.CLAN.instance, gid)
	return id_64bit