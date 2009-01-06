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
FIRST_COMMAND	= 0
#--------------------------------------------------------------------------
PING			= FIRST_COMMAND + 0
CHROOT			= FIRST_COMMAND + 1
MV				= FIRST_COMMAND + 2
RM				= FIRST_COMMAND + 3
MALLOC			= FIRST_COMMAND + 4
FREE			= FIRST_COMMAND + 5
DOWNLOAD		= FIRST_COMMAND + 6
UNPACK			= FIRST_COMMAND + 7
OPEN			= FIRST_COMMAND + 8
CREATE			= FIRST_COMMAND + 9
SEEK			= FIRST_COMMAND + 10
READ			= FIRST_COMMAND + 11
WRITE			= FIRST_COMMAND + 12
CLOSE			= FIRST_COMMAND + 13
#==========================================================================
FIRST_OK		= 0
#--------------------------------------------------------------------------
PONG			= FIRST_OK + 0
OK				= FIRST_OK + 1
#==========================================================================
FIRST_ERROR		= 128
#--------------------------------------------------------------------------
FILENOTFOUND	= FIRST_ERROR + 0
FILEIO			= FIRST_ERROR + 1
OUTOFMEMORY		= FIRST_ERROR + 2
#==========================================================================


#--------------------------------------------------------------------------
COMMANDS = (
#--------------------------------------------------------------------------
	PING,
	CHROOT,
	MV,
	RM,
	MALLOC,
	FREE,
	DOWNLOAD,
	UNPACK,
	OPEN,
	CREATE,
	SEEK,
	READ,
	WRITE,
	CLOSE
)

#--------------------------------------------------------------------------
RESULTS_OK = (
#--------------------------------------------------------------------------
	PONG,
	OK
)

#--------------------------------------------------------------------------
RESULTS_ERROR = (
#--------------------------------------------------------------------------
	FILENOTFOUND,
	FILEIO,
	OUTOFMEMORY
)

#--------------------------------------------------------------------------
COMMANDS_NAME = {
#--------------------------------------------------------------------------
	PING			: 'ping',
	CHROOT			: 'chroot',
	MV				: 'mv',
	RM				: 'rm',
	MALLOC			: 'malloc',
	FREE			: 'free',
	DOWNLOAD		: 'download',
	UNPACK			: 'unpack',
	OPEN			: 'open',
	CREATE			: 'create',
	SEEK			: 'seek',
	READ			: 'read',
	WRITE			: 'write',
	CLOSE			: 'close'
}

#--------------------------------------------------------------------------
RESULTS_NAME = {
#--------------------------------------------------------------------------
	PONG			: 'pong',
	OK				: 'ok',
	FILENOTFOUND	: 'filenotfound',
	FILEIO			: 'fileio',
	OUTOFMEMORY		: 'outofmemory'
}

#--------------------------------------------------------------------------
COMMANDS_OPCODE = dict(map(lambda x: (x[1], x[0]), COMMANDS_NAME.iteritems()))
RESULTS_OPCODE  = dict(map(lambda x: (x[1], x[0]), RESULTS_NAME.iteritems()))
#--------------------------------------------------------------------------

# see data.py for formats specifications

#--------------------------------------------------------------------------
COMMANDS_FORMAT = {
#--------------------------------------------------------------------------
	PING			: '',		#
	CHROOT			: 'S',		# pathname
	MV				: 'SS',		# source_filename,dest_filename
	RM				: 'S',		# filename
	MALLOC			: 'I',		# size
	FREE			: '',		#
	DOWNLOAD		: 'IHD',	# offset,size,data
	UNPACK			: 'II',		# source_offset,dest_offset
	OPEN			: 'S',		# filename
	CREATE			: 'S',		# filename
	SEEK			: 'I',		# offset
	READ			: 'II',		# offset,size
	WRITE			: 'II',		# offset,size
	CLOSE			: '',		#
}

#--------------------------------------------------------------------------
RESULTS_FORMAT = {
#--------------------------------------------------------------------------
	PONG			: '',		#
	OK				: '',		#
	FILENOTFOUND	: 'S',		# filename
	FILEIO			: 'S',		# filename
	OUTOFMEMORY		: 'I',		# biggest block available
}


#==========================================================================
# Commands
#==========================================================================


#--------------------------------------------------------------------------
def command_opcode ( p_name ):
#--------------------------------------------------------------------------

	l_name = p_name.lower()

	if COMMANDS_OPCODE.has_key(l_name):
		return COMMANDS_OPCODES[l_name]

	return None

#--------------------------------------------------------------------------
def command_name ( p_opcode ):
#--------------------------------------------------------------------------

	if COMMANDS_NAME.has_key(p_opcode):
		return COMMANDS_NAME[p_opcode]

	return None

#--------------------------------------------------------------------------
def command_format ( p_opcode ):
#--------------------------------------------------------------------------

	if COMMANDS_FORMAT.has_key(p_opcode):
		return COMMANDS_FORMAT[p_opcode]

	return None


#==========================================================================
# Results
#==========================================================================


#--------------------------------------------------------------------------
def result_opcode ( p_name ):
#--------------------------------------------------------------------------

	l_name = p_name.lower()

	if RESULTS_OPCODE.has_key(l_name):
		return RESULTS_OPCODE[l_name]

	return None

#--------------------------------------------------------------------------
def result_name ( p_opcode ):
#--------------------------------------------------------------------------

	if RESULTS_NAME.has_key(p_opcode):
		return RESULTS_NAME[p_opcode]

	return None

#--------------------------------------------------------------------------
def result_format ( p_opcode ):
#--------------------------------------------------------------------------

	if RESULTS_FORMAT.has_key(p_opcode):
		return RESULTS_FORMAT[p_opcode]

	return None

#--------------------------------------------------------------------------
def is_ok_result ( p_opcode ):
#--------------------------------------------------------------------------

	return (p_opcode in RESULTS_OK)

#--------------------------------------------------------------------------
def is_error_result ( p_opcode ):
#--------------------------------------------------------------------------

	return (p_opcode in RESULTS_ERROR)


#==========================================================================
# End
#==========================================================================
