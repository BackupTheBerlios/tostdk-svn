#==========================================================================
# tostdk :: tostlib :: master.py
# Command generator
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


import pooky
import opcodes
import command


#==========================================================================
PACKET_MAX_DATA_SIZE = 4096
#--------------------------------------------------------------------------
PING_TIMEOUT		= 1.0	# FIXME: ugly harcoded timeouts
CHROOT_TIMEOUT		= 10.0
MV_TIMEOUT			= 10.0
RM_TIMEOUT			= 10.0
MALLOC_TIMEOUT		= 10.0
FREE_TIMEOUT		= 10.0
MEMMOVE_TIMEOUT		= 10.0
DOWNLOAD_TIMEOUT	= 60.0
UNPACK_TIMEOUT		= 60.0
OPEN_TIMEOUT		= 10.0
CREATE_TIMEOUT		= 10.0
SEEK_TIMEOUT		= 10.0
READ_TIMEOUT		= 60.0
WRITE_TIMEOUT		= 60.0
CLOSE_TIMEOUT		= 10.0
#==========================================================================


#==========================================================================
def make_project_commands ( p_slavepath ):
#==========================================================================

	return [
		command.Command.create(opcodes.PING,   [],            PING_TIMEOUT),
		command.Command.Create(opcodes.CHROOT, [p_slavepath], CHROOT_TIMEOUT)
	]

#==========================================================================
def make_add_commands ( p_guid, p_filename, p_filedata ):
#==========================================================================

	l_file_size = len(p_filedata)
	l_data      = pooky.pack(p_filedata)
	l_data_size = len(l_data)
	l_offset    = l_file_size - l_data_size

	l_seq  = [
		command.Command.create(opcodes.MALLOC, [l_file_size], MALLOC_TIMEOUT)
	]

	l_current = l_offset

	while l_data:
		l_packet      = l_data[:PACKET_MAX_DATA_SIZE]
		l_packet_size = len(l_packet)
		l_data        = l_data[l_packet_size:]

		l_seq.append(
			command.Command.create(opcodes.DOWNLOAD,
				[l_current, l_packet_size, l_packet], DOWNLOAD_TIMEOUT))

		l_current += l_packet_size

	l_seq.extend([
		command.Command.create(opcodes.UNPACK, [l_offset, 0],    UNPACK_TIMEOUT),
		command.Command.create(opcodes.CREATE, [p_filename],     CREATE_TIMEOUT),
		command.Command.create(opcodes.WRITE,  [0, l_file_size], WRITE_TIMEOUT),
		command.Command.create(opcodes.CLOSE,  [],               CLOSE_TIMEOUT),
		command.Command.create(opcodes.FREE,   [],               FREE_TIMEOUT, p_guid)
	])

	return l_seq

#==========================================================================
def make_remove_commands ( p_guid, p_filename ):
#==========================================================================

	return [
		command.Command.create(opcodes.RM, [p_filename], RM_TIMEOUT, p_guid)
	]

#==========================================================================
def make_rename_commands ( p_guid, p_old_filename, p_new_filename ):
#==========================================================================

	return [
		command.Command.create(opcodes.MV,
			[p_old_filename, p_new_filename],
			RM_TIMEOUT, p_guid)
	]

#==========================================================================
def make_update_commands ( p_guid, p_filename, p_diff ):
#==========================================================================

	l_orig_size, l_final_size, l_matcher = p_diff

	l_seq = [
		command.Command.create(opcodes.MALLOC, [l_final_size],   MALLOC_TIMEOUT),
		command.Command.create(opcodes.OPEN,   [p_filename],     OPEN_TIMEOUT),
		command.Command.create(opcodes.READ,   [0, l_orig_size], READ_TIMEOUT)
	]

	# TODO: read docs and implement...

	l_seq.extend([
		command.Command.create(opcodes.SEEK,  [0],               SEEK_TIMEOUT),
		command.Command.create(opcodes.WRITE, [0, l_final_size], WRITE_TIMEOUT),
		command.Command.create(opcodes.CLOSE, [],                CLOSE_TIMEOUT),
		command.Command.create(opcodes.FREE,  [],                FREE_TIMEOUT, p_guid)
	])

	return l_seq


#==========================================================================
# End
#==========================================================================
