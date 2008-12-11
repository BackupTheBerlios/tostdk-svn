#==========================================================================
# tostdk :: tostlib :: drivers :: packet.py
# Binary packet helpers
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
PACKET_FMT = '>BH'
#==========================================================================


#==========================================================================
def pack ( p_opcode, p_data ):
#==========================================================================

	return struct.pack(PACKET_FMT, p_opcode, len(p_data)) + p_data

#==========================================================================
def unpack ( p_packet ):
#==========================================================================

	l_packet_length = len(p_packet)

	if l_packet_length < 3:
		return None

	l_opcode, l_data_length = struct.unpack(PACKET_FMT, p_packet[:3])

	if l_packet_length != (l_data_length + 3):
		return None

	return (l_opcode, l_packet[3:])

#==========================================================================
def is_valid ( p_packet ):
#==========================================================================

	l_packet_length = len(p_packet)

	if l_packet_length < 3:
		return False

	l_opcode, l_data_length = struct.unpack(PACKET_FMT, p_packet[:3])

	if l_packet_length != (l_data_length + 3):
		return False

	return True


#==========================================================================
# End
#==========================================================================
