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


#==========================================================================
# Commands
#==========================================================================


#--------------------------------------------------------------------------
COMMANDS = (
#--------------------------------------------------------------------------
	'PING',			# ''

	'CHROOT',		# 'str(pathname)'
	'CHDIR',		# 'str(pathname)'
	'MKDIR',		# 'str(pathname)'
	'MV',			# 'str(source_filename),str(dest_filename)'
	'RM',			# 'str(filename)'

	'MALLOC',		# 'int(size)'
	'FREE',			# ''
	'MEMMOVE',		# 'int(source_offset),int(dest_offset),int(size)'
	'DOWNLOAD',		# 'int(offset),int(size),data'

	'OPEN',			# 'str(filename)'
	'CREATE',		# 'str(filename)'
	'SEEK',			# 'int(offset)'
	'READ',			# 'int(offset),int(size)'
	'WRITE',		# 'int(offset),int(size)'
	'CLOSE',		# ''
)

#--------------------------------------------------------------------------
def command_opcode ( p_string ):
#--------------------------------------------------------------------------

	l_command = p_string.upper()

	if l_command in COMMANDS:
		return  COMMANDS.index(l_command)

	return None

#--------------------------------------------------------------------------
def command_string ( p_opcode ):
#--------------------------------------------------------------------------

	if p_opcode < len(COMMANDS):
		return COMMANDS[p_opcode]

	return None


#==========================================================================
# Results
#==========================================================================


#--------------------------------------------------------------------------
RESULTS_OK = (
#--------------------------------------------------------------------------
	'PONG',					# ''
	'OK',					# ''
)

#--------------------------------------------------------------------------
RESULTS_ERROR = (
#--------------------------------------------------------------------------
	'INVALID_PATHNAME',		# 'str(pathname)\0'
	'INVALID_FILENAME',		# 'str(pathname)\0'
	'NOT_ENOUGH_MEMORY',	# 'short(memslot)'
	'INVALID_BUFFER',		# 'short(memslot)'
	'INVALID_FILE',			# 'short(fileslot)'
	'FILE_IO_ERROR',		# 'short(fileslot)'
)

#--------------------------------------------------------------------------
def result_opcode ( p_string ):
#--------------------------------------------------------------------------

	l_result = p_string.upper()

	if l_result in RESULTS_OK:
		return  RESULTS_OK.index(l_result)
	elif l_result in RESULTS_ERROR:
		return RESULTS_ERROR.index(l_result) + 128

	return None

#--------------------------------------------------------------------------
def result_string ( p_opcode ):
#--------------------------------------------------------------------------

	if p_opcode < 128 and p_opcode < len(RESULTS_OK):
		return RESULTS_OK[p_opcode]
	elif p_opcode > 127 and (p_opcode - 128) < len(RESULTS_ERROR):
		return RESULTS_ERROR[p_opcode - 128]

	return None

#--------------------------------------------------------------------------
def is_ok_result ( p_opcode ):
#--------------------------------------------------------------------------

	return (p_opcode < 128)

#--------------------------------------------------------------------------
def is_error_result ( p_opcode ):
#--------------------------------------------------------------------------

	return (p_opcode > 127)


#==========================================================================
# End
#==========================================================================
