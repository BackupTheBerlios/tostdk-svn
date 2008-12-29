#==========================================================================
# tostdk :: tostlib :: pooky.py
# Data packer
#--------------------------------------------------------------------------
# Copyright 2009 Jean-Baptiste Berlioz
#--------------------------------------------------------------------------
# This file is part of Tostdk.
#
# Tostdk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tostdk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tostdk.  If not, see <http://www.gnu.org/licenses/>.
#==========================================================================


import struct


#==========================================================================
PAK_BIT = 15
STR_BIT =  7
CNT_BIT =  4
#-------------------------------------------------------------------------------
IDX_BIT = PAK_BIT - CNT_BIT
MIN_CNT = ((PAK_BIT + 1) >> 3) + 1
MAX_CNT = (1 << CNT_BIT) - 1
MAX_IDX = (1 << IDX_BIT) - 1
MAX_STR = (1 << STR_BIT) - 1
CNT_MAX = MAX_CNT + MIN_CNT
STR_MAX = MAX_STR + 1
#==========================================================================


#-------------------------------------------------------------------------------
def pack ( p_data ):
#-------------------------------------------------------------------------------

	def find_string ( p_data, p_string ):
		l_size = len(p_string)
		while (l_size >= MIN_CNT):
			l_idx = p_data.find(p_string[:l_size])
			if (l_idx > -1):
				return (-(len(p_data) - l_idx)), l_size
			l_size -= 1
		return 0, 0

	def store_string ( p_string ):
		l_tag = (len(p_string) - 1) & MAX_STR
		return struct.pack('>B', l_tag) + p_string

	def store_code ( p_idx, p_cnt ):
		l_tag = (p_idx << CNT_BIT) | ((p_cnt - MIN_CNT) & MAX_CNT)
		return struct.pack('>H', l_tag & 0xFFFF)

	l_total  = len(p_data)
	l_size   = 0

	l_code   = struct.pack('>L', l_total)
	l_store  = ''
	l_data   = ''
	l_string = p_data

	while (l_string):
		l_idx, l_cnt = find_string(l_data[-MAX_IDX:], l_string[:CNT_MAX])

		if (l_cnt):
			l_data += l_string[:l_cnt]
			if (l_store):
				l_size += len(l_store)
				l_code += store_string(l_store)
				l_store = ''
			l_code  += store_code(l_idx, l_cnt)
			l_string = l_string[l_cnt:]
			l_size  += l_cnt

		else:
			l_data += l_string[0]
			if (len(l_store) == STR_MAX):
				l_code  += store_string(l_store)
				l_store  = l_string[0]
				l_size  += STR_MAX
			else:
				l_store += l_string[0]
			l_string = l_string[1:]

	if (l_store):
		l_code += store_string(l_store)
		l_size += len(l_store)

	if (len(l_code) & 1):
		l_code += struct.pack('>B', 0)

	l_data = '.POO' + l_code

	if len(l_data) >= l_total:
		l_data = p_data

	return l_data


#==========================================================================
# End
#==========================================================================
