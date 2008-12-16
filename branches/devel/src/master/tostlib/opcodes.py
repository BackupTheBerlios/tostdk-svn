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


#--------------------------------------------------------------------------
COMMANDS = (
#--------------------------------------------------------------------------
	'PING',							# ping
	'CHROOT',						# select project root
	'MKDIR',						# create new directories
	'MV',							# rename a file
	'RM',							# remove a file
	'MALLOC',						# allocate memory
	'FREE',							# free allocated memory
	'MEMMOVE',						# move memory within allocated memory
	'DOWNLOAD',						# download data inside allocated memory
	'OPEN',							# open a file for reading
	'CREATE',						# create a file for writing
	'SEEK',							# move current opened file absolute pointer
	'READ',							# read data from current file to allocated memory
	'WRITE',						# write data from allocated memory to current file
	'CLOSE',						# close current file
)

#--------------------------------------------------------------------------
COMMANDS_FMT = (
#--------------------------------------------------------------------------
	'PING'		: '',				#
	'CHROOT'	: 'S',				# pathname
	'MKDIR'		: 'S',				# pathname
	'MV'		: 'SS',				# source_filename,dest_filename
	'RM'		: 'S',				# filename
	'MALLOC'	: 'I',				# size
	'FREE'		: '',				#
	'MEMMOVE'	: 'III',			# source_offset,dest_offset,size
	'DOWNLOAD'	: 'IID',			# offset,size,data
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
	'PONG',							# pong
	'OK',							# no error
)

#--------------------------------------------------------------------------
RESULTS_OK_FMT = (
#--------------------------------------------------------------------------
	'PONG'		: '',				#
	'OK'		: '',				#
)

#--------------------------------------------------------------------------
RESULTS_ERROR = (
#--------------------------------------------------------------------------
	'CHROOT_ERROR',					#
	'CHDIR_ERROR',					#
	'CREATEDIR_ERROR',				#
	'OPENFILE_ERROR',				#
	'CREATEFILE_ERROR',				#
	'FILEIO_ERROR',					#
	'OUTOFMEMORY_ERROR',			#
)

#--------------------------------------------------------------------------
RESULTS_ERROR_FMT = (
#--------------------------------------------------------------------------
	'CHROOT_ERROR'		: 'S',		# pathname
	'CHDIR_ERROR'		: 'S',		# pathname
	'CREATEDIR_ERROR'	: 'S',		# pathname
	'OPENFILE_ERROR'	: 'S',		# filename
	'CREATEFILE_ERROR'	: 'S',		# filename
	'FILEIO_ERROR'		: 'S',		# filename
	'OUTOFMEMORY_ERROR'	: '',		#
)


#==========================================================================
# Commands
#==========================================================================


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
