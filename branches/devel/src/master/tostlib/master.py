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


import configuration
import pooky
import opcodes
import command


#==========================================================================
def make_project_commands ( p_slavepath ):
#==========================================================================

	l_config = configuration.Configuration.get_instance()
	l_ping_timeout   = l_config.get_option_value('protocol', 'ping_timeout')
	l_chroot_timeout = l_config.get_option_value('protocol', 'chroot_timeout')

	return [
		command.Command.create(opcodes.PING,   [],            l_ping_timeout),
		command.Command.Create(opcodes.CHROOT, [p_slavepath], l_chroot_timeout)
	]

#==========================================================================
def make_add_commands ( p_guid, p_filename, p_filedata ):
#==========================================================================

	l_config = configuration.Configuration.get_instance()
	l_malloc_timeout   = l_config.get_option_value('protocol', 'malloc_timeout')
	l_create_timeout   = l_config.get_option_value('protocol', 'create_timeout')
	l_write_timeout    = l_config.get_option_value('protocol', 'write_timeout')
	l_close_timeout    = l_config.get_option_value('protocol', 'close_timeout')
	l_free_timeout     = l_config.get_option_value('protocol', 'free_timeout')

	l_file_size = len(p_filedata)

	l_seq  = [
		command.Command.create(opcodes.MALLOC, [l_file_size], l_malloc_timeout)
	]

	l_seq.extend(__download_commands(0, p_filedata))

	l_seq.extend([
		command.Command.create(opcodes.CREATE, [p_filename],     l_create_timeout),
		command.Command.create(opcodes.WRITE,  [0, l_file_size], l_write_timeout),
		command.Command.create(opcodes.CLOSE,  [],               l_close_timeout),
		command.Command.create(opcodes.FREE,   [],               l_free_timeout, p_guid)
	])

	return l_seq

#==========================================================================
def make_remove_commands ( p_guid, p_filename ):
#==========================================================================

	l_config = configuration.Configuration.get_instance()
	l_rm_timeout = l_config.get_option_value('protocol', 'rm_timeout')

	return [
		command.Command.create(opcodes.RM, [p_filename], l_rm_timeout, p_guid)
	]

#==========================================================================
def make_rename_commands ( p_guid, p_old_filename, p_new_filename ):
#==========================================================================

	l_config = configuration.Configuration.get_instance()
	l_mv_timeout = l_config.get_option_value('protocol', 'mv_timeout')

	return [
		command.Command.create(opcodes.MV,
			[p_old_filename, p_new_filename],
			l_mv_timeout, p_guid)
	]

#==========================================================================
def make_update_commands ( p_guid, p_filename, p_diff, p_filedata ):
#==========================================================================

	l_config = configuration.Configuration.get_instance()
	l_malloc_timeout   = l_config.get_option_value('protocol', 'malloc_timeout')
	l_open_timeout     = l_config.get_optiob_value('protocol', 'open_timeout')
	l_seek_timeout     = l_config.get_option_value('protocol', 'seek_timeout')
	l_read_timeout     = l_config.get_option_value('protocol', 'read_timeout')
	l_write_timeout    = l_config.get_option_value('protocol', 'write_timeout')
	l_close_timeout    = l_config.get_option_value('protocol', 'close_timeout')
	l_free_timeout     = l_config.get_option_value('protocol', 'free_timeout')

	l_orig_size, l_final_size, l_matcher = p_diff

	l_seq = [
		command.Command.create(opcodes.MALLOC, [l_final_size], l_malloc_timeout),
		command.Command.create(opcodes.OPEN,   [p_filename],   l_open_timeout),
	]

	l_file_offset = 0
	l_mem_offset  = 0

	for l_tag, l_i1, l_i2, l_j1, l_j2 in p_diff:

		if l_tag == 'replace':

			l_file_offset += l_i2 - l_i1
			l_seq.append(
				command.Command.create(opcodes.SEEK, [l_file_offset], l_seek_timeout))

			l_data = p_filedata[l_j1:l_j2]
			l_seq.extend(__download_commands(l_mem_offset, l_data))

			l_mem_offset += l_j2 - l_j1

		elif l_tag == 'delete':

			l_file_offset += l_i2 - l_i1
			l_seq.append(
				command.Command.create(opcodes.SEEK, [l_file_offset], l_seek_timeout))

		elif l_tag == 'insert':

			l_data = p_filedata[l_j1:l_j2]
			l_seq.extend(__download_commands(l_mem_offset, l_data))

			l_mem_offset += l_j2 - l_j1

		elif l_tag == 'equal':

			l_length = l_i2 - l_i1
			l_seq.append(
				command.Command.create(opcodes.READ, [l_mem_offset, l_length], l_read_timeout))

			l_file_offset += l_length
			l_mem_offset  += l_length

	l_seq.extend([
		command.Command.create(opcodes.SEEK,  [0],               l_seek_timeout),
		command.Command.create(opcodes.WRITE, [0, l_final_size], l_write_timeout),
		command.Command.create(opcodes.CLOSE, [],                l_close_timeout),
		command.Command.create(opcodes.FREE,  [],                l_free_timeout, p_guid)
	])

	return l_seq

#==========================================================================
def __download_commands ( p_offset, p_data ):
#==========================================================================

	l_config = configuration.Configuration.get_instance()
	l_max_data_size    = l_config.get_option_value('protocol', 'packet_size')
	l_download_timeout = l_config.get_option_value('protocol', 'download_timeout')
	l_unpack_timeout   = l_config.get_option_value('protocol', 'unpack_timeout')

	l_seq = []

	l_size      = len(p_data)
	l_data      = pooky.pack(p_data)
	l_data_size = len(l_data)
	l_offset    = p_offset + (l_size - l_data_size)
	l_current   = l_offset

	while l_data:
		l_packet      = l_data[:l_max_data_size]
		l_packet_size = len(l_packet)
		l_data        = l_data[l_packet_size:]

		l_seq.append(
			command.Command.create(opcodes.DOWNLOAD,
				[l_current, l_packet_size, l_packet], l_download_timeout))

		l_current += l_packet_size

	l_seq.append(
		command.Command.create(opcodes.UNPACK, [l_offset, p_offset], l_unpack_timeout))

	return l_seq


#==========================================================================
# End
#==========================================================================
