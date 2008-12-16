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

	'CHROOT',		# 'str(pathname)\0'
	'CHDIR',		# 'str(pathname)\0'
	'MKDIR',		# 'str(pathname)\0'
	'MV',			# 'str(source_filename)\0str(dest_filename)\0'
	'RM',			# 'str(filename)\0'

	'MALLOC',		# 'short(memslot),int(size)'
	'FREE',			# 'short(memslot)'
	'MEMMOVE',		# 'short(memslot),int(source_offset),int(dest_offset),int(size)'
	'DOWNLOAD',		# 'short(memslot),int(offset),int(size)' + data

	'OPEN',			# 'short(fileslot),str(filename)\0'
	'CREATE',		# 'short(fileslot),str(filename)\0'
	'SEEK',			# 'short(fileslot),int(offset)'
	'READ',			# 'short(fileslot),short(memslot),int(offset),int(size)'
	'WRITE',		# 'short(fileslot),short(memslot),int(offset),int(size)'
	'CLOSE',		# 'short(fileslot)
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
RESULTS = (
#--------------------------------------------------------------------------
	'OK',					# ''

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

	if l_result in RESULTS:
		return  RESULTS.index(l_result)

	return None

#--------------------------------------------------------------------------
def result_string ( p_opcode ):
#--------------------------------------------------------------------------

	if p_opcode < len(RESULTS):
		return RESULTS[p_opcode]

	return None


#==========================================================================
# End
#==========================================================================
