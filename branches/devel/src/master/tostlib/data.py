#==========================================================================
# tostdk :: tostlib :: data.py
# Data packing / unpacking
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
# Format:
#--------------------------------------------------------------------------
# B : byte		= 1
# H : word		= 2
# I : long word	= 4
# S : string	= size.w + string (\0 terminated) [+ padd byte]
# D : data		= size.w + data [+ padd byte]
#==========================================================================


#==========================================================================
def pack ( p_format, p_args ):
#==========================================================================

	if len(p_format) != len(p_args):
		return None

	l_zip  = zip(p_format, p_args)
	l_data = ''

	for l_format, l_arg in l_zip:

		if l_format == 'B':
			l_data += struct.pack('>B', l_arg)

		elif l_format == 'H':
			l_data += struct.pack('>H', l_arg)

		elif l_format == 'I':
			l_data += struct.pack('>I', l_arg)

		elif l_format == 'S':
			l_len   = len(l_arg) + 1
			l_data += struct.pack('>H', l_len) + l_arg + '\0'
			if (l_len & 1):
				l_data += '\0'

		elif l_format == 'D':
			l_len   = len(l_arg)
			l_data += struct.pack('>H', l_len) + l_arg
			if (l_len & 1):
				l_data += '\0'

	return l_data

#==========================================================================
def unpack ( p_format, p_data ):
#==========================================================================

	l_unpack = []
	l_data   = p_data

	for l_format in p_format:

		if l_format == 'B':
			if len(l_data) < 1:
				return None
			l_unpack.extend(struct.unpack('>B', l_data[:1]))
			l_data = l_data[1:]

		elif l_format == 'H':
			if len(l_data) < 2:
				return None
			l_unpack.extend(struct.unpack('>H', l_data[:2]))
			l_data = l_data[2:]

		elif l_format == 'I':
			if len(l_data) < 4:
				return None
			l_unpack.extend(struct.unpack('>I', l_data[:4]))
			l_data = l_data[4:]

		elif l_format == 'S':
			if len(l_data) < 2:
				return None
			l_len  = struct.unpack('>H', l_data[:2])[0]
			if len(l_data) < (2 + l_len):
				return None
			l_str  = l_data[2: (2 + l_len)].rstrip('\0')
			l_unpack.append(l_str)
			if (l_len & 1): l_len += 1
			if len(l_data) < (2 + l_len):
				return None
			l_data = l_data[(2 + l_len):]

		elif l_format == 'D':
			if len(l_data) < 2:
				return None
			l_len  = struct.unpack('>H', l_data[:2])[0]
			if len(l_data) < (2 + l_len):
				return None
			l_dat  = l_data[2: (2 + l_len)]
			l_unpack.append(l_dat)
			if (l_len & 1): l_len += 1
			if len(l_data) < (2 + l_len):
				return None
			l_data = l_data[(2 + l_len):]

	return l_unpack

#==========================================================================
def unpack_readable ( p_format, p_data ):
#==========================================================================

	l_unpack = unpack(p_format, p_data)

	if l_unpack == None:
		return '* unpack error *'

	l_string = []
	l_zip    = zip(p_format, l_unpack)

	for l_format, l_data in l_zip:

		if l_format == 'B':
			l_string.append(str(l_data) + '.b')

		elif l_format == 'H':
			l_string.append(str(l_data) + '.w')

		elif l_format == 'I':
			l_string.append(str(l_data) + '.l')

		elif l_format == 'S':
			l_string.append(l_data)

		elif l_format == 'D':
			l_string.append('<data>')

	return ', '.join(l_string)


#==========================================================================
# End
#==========================================================================
