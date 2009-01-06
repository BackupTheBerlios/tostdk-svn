#==========================================================================
# tostdk :: tostlib :: drivers :: packet.py
# Low level packet library
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
import array


#==========================================================================
PACKET_TAG = 0xA5
#==========================================================================

#==========================================================================
PACKET_HEADER = (
#==========================================================================
	('tag',			'B'),	# PACKET_TAG
	('opcode',		'B'),	# command|result opcode
	('checksum',	'B'),	# header checksum % 256
	('crc8',		'B'),	# data crc8
	('length',		'H')	# data length
)

#==========================================================================
PACKET_FMT      = reduce(lambda x, y: x + y[1], PACKET_HEADER, '>')
PACKET_FMT_SIZE = struct.calcsize(PACKET_FMT)
#==========================================================================

#==========================================================================
CCITT8_TABLE = (
#==========================================================================
	0x00, 0x31, 0x62, 0x53, 0xC4, 0xF5, 0xA6, 0x97,
	0xB9, 0x88, 0xDB, 0xEA, 0x7D, 0x4C, 0x1F, 0x2E,
	0x43, 0x72, 0x21, 0x10, 0x87, 0xB6, 0xE5, 0xD4,
	0xFA, 0xCB, 0x98, 0xA9, 0x3E, 0x0F, 0x5C, 0x6D,
	0x86, 0xB7, 0xE4, 0xD5, 0x42, 0x73, 0x20, 0x11,
	0x3F, 0x0E, 0x5D, 0x6C, 0xFB, 0xCA, 0x99, 0xA8,
	0xC5, 0xF4, 0xA7, 0x96, 0x01, 0x30, 0x63, 0x52,
	0x7C, 0x4D, 0x1E, 0x2F, 0xB8, 0x89, 0xDA, 0xEB,
	0x3D, 0x0C, 0x5F, 0x6E, 0xF9, 0xC8, 0x9B, 0xAA,
	0x84, 0xB5, 0xE6, 0xD7, 0x40, 0x71, 0x22, 0x13,
	0x7E, 0x4F, 0x1C, 0x2D, 0xBA, 0x8B, 0xD8, 0xE9,
	0xC7, 0xF6, 0xA5, 0x94, 0x03, 0x32, 0x61, 0x50,
	0xBB, 0x8A, 0xD9, 0xE8, 0x7F, 0x4E, 0x1D, 0x2C,
	0x02, 0x33, 0x60, 0x51, 0xC6, 0xF7, 0xA4, 0x95,
	0xF8, 0xC9, 0x9A, 0xAB, 0x3C, 0x0D, 0x5E, 0x6F,
	0x41, 0x70, 0x23, 0x12, 0x85, 0xB4, 0xE7, 0xD6,
	0x7A, 0x4B, 0x18, 0x29, 0xBE, 0x8F, 0xDC, 0xED,
	0xC3, 0xF2, 0xA1, 0x90, 0x07, 0x36, 0x65, 0x54,
	0x39, 0x08, 0x5B, 0x6A, 0xFD, 0xCC, 0x9F, 0xAE,
	0x80, 0xB1, 0xE2, 0xD3, 0x44, 0x75, 0x26, 0x17,
	0xFC, 0xCD, 0x9E, 0xAF, 0x38, 0x09, 0x5A, 0x6B,
	0x45, 0x74, 0x27, 0x16, 0x81, 0xB0, 0xE3, 0xD2,
	0xBF, 0x8E, 0xDD, 0xEC, 0x7B, 0x4A, 0x19, 0x28,
	0x06, 0x37, 0x64, 0x55, 0xC2, 0xF3, 0xA0, 0x91,
	0x47, 0x76, 0x25, 0x14, 0x83, 0xB2, 0xE1, 0xD0,
	0xFE, 0xCF, 0x9C, 0xAD, 0x3A, 0x0B, 0x58, 0x69,
	0x04, 0x35, 0x66, 0x57, 0xC0, 0xF1, 0xA2, 0x93,
	0xBD, 0x8C, 0xDF, 0xEE, 0x79, 0x48, 0x1B, 0x2A,
	0xC1, 0xF0, 0xA3, 0x92, 0x05, 0x34, 0x67, 0x56,
	0x78, 0x49, 0x1A, 0x2B, 0xBC, 0x8D, 0xDE, 0xEF,
	0x82, 0xB3, 0xE0, 0xD1, 0x46, 0x77, 0x24, 0x15,
	0x3B, 0x0A, 0x59, 0x68, 0xFF, 0xCE, 0x9D, 0xAC
)

#==========================================================================
def pack_header ( p_header ):
#==========================================================================

	l_args = []

	for l_member in PACKET_HEADER:
		l_key = l_member[0]

		if not p_header.has_key(l_key):
			return None

		l_args.append(p_header[l_key])

	try:
		l_data = struct.pack(PACKET_FMT, *l_args)
	except:
		return None

	return l_data

#==========================================================================
def unpack_header ( p_data ):
#==========================================================================

	if len(p_data) < PACKET_FMT_SIZE:
		return None

	try:
		l_values = struct.unpack(PACKET_FMT, p_data[:PACKET_FMT_SIZE])
	except:
		return None

	if len(l_values) != len(PACKET_HEADER):
		return None

	l_header = {}

	for l_member, l_value in zip(PACKET_HEADER, l_values):
		l_key = l_member[0]
		l_header[l_key] = l_value

	return l_header

#==========================================================================
def is_header_valid ( p_header ):
#==========================================================================

	if p_header['tag'] != PACKET_TAG:
		return False

	l_checksum = __checksum(p_header)

	return (l_checksum == p_header['checksum'])

#==========================================================================
def pack ( p_opcode, p_data ):
#==========================================================================

	l_header = {
		'tag'		: PACKET_TAG,
		'opcode'	: p_opcode,
		'crc8'		: __crc8(p_data),
		'length'	: len(p_data)
	}

	l_header['checksum'] = __checksum(l_header)

	l_data = pack_header(l_header)

	if l_data == None:
		return None

	return l_data + p_data

#==========================================================================
def unpack ( p_packet ):
#==========================================================================

	l_header = unpack_header(p_packet)

	if l_header == None:
		return None

	if not is_header_valid(l_header):
		return None

	if l_header['length'] > (len(p_packet) - PACKET_FMT_SIZE):
		return None

	l_data = p_packet[PACKET_FMT_SIZE : PACKET_FMT_SIZE + l_header['length']]

	l_crc8 = __crc8(l_data)
	if l_header['crc8'] != l_crc8:
		l_data = None

	return (l_header['opcode'], l_data)

#==========================================================================
def is_valid ( p_packet ):
#==========================================================================

	l_header = unpack_header(p_packet)

	if l_header == None:
		return False

	if not is_header_valid(l_header):
		return False

	if l_header['length'] > (len(p_packet) - PACKET_FMT_SIZE):
		return False

	return True

#==========================================================================
def __crc8 ( p_data ):
#==========================================================================

	l_data = array.array('B', p_data)
	return reduce(lambda x, y: CCITT8_TABLE[(x ^ y) & 0xFF], l_data, 0)

#==========================================================================
def __checksum ( p_header ):
#==========================================================================

	l_sum = p_header['tag'] + p_header['opcode'] + p_header['crc8'] + \
			(p_header['length'] >> 8) + (p_header['length'] & 0xFF)

	return l_sum & 0xFF


#==========================================================================
# End
#==========================================================================
