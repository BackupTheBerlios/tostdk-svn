#==========================================================================
# tostdk :: tostlib :: opcodes.py
# Opcodes enumerations
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


# see data.py for formats specifications


#--------------------------------------------------------------------------
COMMANDS = (
#--------------------------------------------------------------------------
	'PING'		: '',				#
	'CHROOT'	: 'S',				# pathname
	'MV'		: 'SS',				# source_filename,dest_filename
	'RM'		: 'S',				# filename
	'MALLOC'	: 'I',				# size
	'FREE'		: '',				#
	'MEMMOVE'	: 'III',			# source_offset,dest_offset,size
	'DOWNLOAD'	: 'IHD',			# offset,size,data
	'OPEN'		: 'S',				# filename
	'CREATE'	: 'S',				# filename
	'SEEK'		: 'I',				# offset
	'READ'		: 'II',				# offset,size
	'WRITE'		: 'II',				# offset,size
	'CLOSE'		: '',				#
)

#--------------------------------------------------------------------------
RESULTS_OK = (
#--------------------------------------------------------------------------
	'PONG'		: '',				#
	'OK'		: '',				#
)

#--------------------------------------------------------------------------
RESULTS_SPLIT = 128
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
RESULTS_ERROR = (
#--------------------------------------------------------------------------
	'FILENOTFOUND'		: 'S',		# filename
	'FILEIO'			: 'S',		# filename
	'OUTOFMEMORY'		: 'I',		# biggest block available
)


#==========================================================================
# Commands
#==========================================================================


#--------------------------------------------------------------------------
def command_opcode ( p_name ):
#--------------------------------------------------------------------------

	l_name = p_name.upper()

	if COMMANDS.has_key(l_name):
		return sorted(COMMANDS.keys()).index(l_name)

	return None

#--------------------------------------------------------------------------
def command_name ( p_opcode ):
#--------------------------------------------------------------------------

	if p_opcode < len(COMMANDS.keys()):
		return sorted(COMMANDS.keys())[p_opcode]

	return None

#--------------------------------------------------------------------------
def command_format ( p_name ):
#--------------------------------------------------------------------------

	l_name = p_name.upper()

	if COMMANDS.has_key(l_name):
		return COMMANDS[l_name]

	return None


#==========================================================================
# Results
#==========================================================================


#--------------------------------------------------------------------------
def result_opcode ( p_name ):
#--------------------------------------------------------------------------

	l_name = p_name.upper()

	if RESULTS_OK.has_key(l_name):
		return sorted(RESULTS_OK.keys()).index(l_name)

	elif RESULTS_ERROR.has_key(l_name):
		return sorted(RESULTS_ERROR.keys()).index(l_name) + RESULTS_SPLIT

	return None

#--------------------------------------------------------------------------
def result_name ( p_opcode ):
#--------------------------------------------------------------------------

	if p_opcode < RESULTS_SPLIT and \
			p_opcode < len(RESULTS_OK.keys()):
		return sorted(RESULTS_OK.keys())[p_opcode]

	elif p_opcode >= RESULTS_SPLIT and \
			(p_opcode - RESULTS_SPLIT) < len(RESULTS_ERROR.keys()):
		return sorted(RESULTS_ERROR.keys())[p_opcode - RESULTS_SPLIT]

	return None

#--------------------------------------------------------------------------
def result_format ( p_name ):
#--------------------------------------------------------------------------

	l_name = p_name.upper()

	if RESULTS_OK.has_key(l_name):
		return RESULTS_OK[l_name]

	elif RESULTS_ERROR.has_key(l_name):
		return RESULTS_ERROR[l_name]

	return None

#--------------------------------------------------------------------------
def is_ok_result ( p_opcode ):
#--------------------------------------------------------------------------

	return (p_opcode < RESULTS_SPLIT)

#--------------------------------------------------------------------------
def is_error_result ( p_opcode ):
#--------------------------------------------------------------------------

	return (p_opcode >= RESULTS_SPLIT)


#==========================================================================
# End
#==========================================================================
