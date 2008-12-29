#==========================================================================
# tostdk :: tostlib :: project.py
# Project manager
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


import os
import sys

import logging
import configuration
import cache
import journal
import master
import queue


#==========================================================================
class Project:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_master_path, p_slave_path ):
	#----------------------------------------------------------------------

		l_config      = configuration.Configuration.get_instance()
		l_project_dir = l_config.get_option_value('general', 'project_dir')

		self.m_master_path  = os.path.abspath(p_master_path)
		self.m_slave_path   = p_slave_path

		self.m_project_path = os.path.join(self.m_master_path, l_project_dir)
		self.m_cache_path   = os.path.join(self.m_project_path, 'cache')

		self.m_cache   = cache.Cache(self.m_master_path, self.m_cache_path)
		self.m_journal = journal.Journal(self.m_project_path)

	#----------------------------------------------------------------------
	def get_master_path ( self ): return self.m_master_path
	def get_slave_path  ( self ): return self.m_slave_path
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def get_project_path ( self ): return self.m_project_path
	def get_cache_path   ( self ): return self.m_cache_path
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def get_cache   ( self ): return self.m_cache
	def get_journal ( self ): return self.m_journal
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	@classmethod
	def find_project_root ( cls, p_path ):
	#----------------------------------------------------------------------

		l_config = configuration.Configuration.get_instance()

		if not l_config.load():
			return None

		l_project_dir = l_config.get_option_value('general', 'project_dir')
		l_path = os.path.abspath(p_path)

		while l_path:
			l_project_path = os.path.join(l_path, l_project_dir)

			if os.path.exists(l_project_path):
				break

			l_parent = os.path.dirname(l_path)

			if l_parent == l_path:
				l_path = ''
			else:
				l_path = l_parent

		return l_path

	#----------------------------------------------------------------------
	@classmethod
	def open ( cls, p_master_path ):
	#----------------------------------------------------------------------

		l_master_path = cls.find_project_root(p_master_path)

		if not l_master_path:
			logging.error("Can't find project root: " + p_master_path)
			return None

		l_config = configuration.Configuration.get_instance()

		if not l_config.load(l_master_path):
			return None

		l_slave_path = l_config.get_option_value('project', 'slave_path')

		if l_slave_path == None:
			return None

		return cls(l_master_path, l_slave_path)

	#----------------------------------------------------------------------
	@classmethod
	def create ( cls, p_master_path, p_slave_path ):
	#----------------------------------------------------------------------

		l_master_path = os.path.abspath(p_master_path)

		l_config = configuration.Configuration.get_instance()

		if not l_config.load(l_master_path):
			return None

		l_project_dir  = l_config.get_option_value('general', 'project_dir')
		l_project_path = os.path.join(l_master_path, l_project_dir)
		l_cache_path   = os.path.join(l_project_path, 'cache')

		if not os.path.exists(l_project_path):
			try:
				os.makedirs(l_project_path)
			except:
				logging.error("Can't create directory: ", l_project_path)
				return None

		if not os.path.exists(l_cache_path):
			try:
				os.makedirs(l_cache_path)
			except:
				logging.error("Can't create directory: ", l_cache_path)
				return None

		if not l_config.set_option_value('project', 'slave_path', p_slave_path):
			return None

		if not l_config.save(l_master_path):
			return None

		return cls(l_master_path, p_slave_path)

	#----------------------------------------------------------------------
	def add_file ( self, p_file_path ):
	#----------------------------------------------------------------------

		l_file_path = os.path.abspath(p_file_path)

		if not l_file_path.startswith(self.m_master_path):
			logging.error("File isn't inside project root: " + l_file_path)
			return False

		if not os.path.exists(l_file_path):
			logging.error("File doesn't exists: ", l_file_path)
			return False

		l_file_path = self.__master_path(l_file_path)

		if not self.m_cache.add_entry(l_file_path, p_simulate=True):
			return False

		l_command = journal.CMD_ADD
		l_args    = [l_file_path]

		if self.m_journal.has_entry(l_command, l_args):
			return True

		return self.m_journal.add_entry(l_command, l_args)

	#----------------------------------------------------------------------
	def __post_add ( self, p_command, p_journal_entry ):
	#----------------------------------------------------------------------

		l_args = p_journal_entry.get_args()

		if not self.m_cache.add_entry(l_args[0]):
			logging.error("Can't update cache entry: " + l_args[0])

			p_journal_entry.unlock()
			return False

		return True

	#----------------------------------------------------------------------
	def remove_file ( self, p_file_path ):
	#----------------------------------------------------------------------

		l_file_path = os.path.abspath(p_file_path)

		if not l_file_path.startswith(self.m_master_path):
			logging.error("File isn't inside project base: " + l_file_path)
			return False

		if not os.path.exists(l_file_path):
			logging.error("File doesn't exists: ", l_file_path)
			return False

		l_file_path = self.__master_path(l_file_path)

		if not self.m_cache.remove_entry(l_file_path, p_simulate=True):
			return False

		l_command = journal.CMD_REMOVE
		l_args    = [l_file_path]

		if self.m_journal.has_entry(l_command, l_args):
			return True

		return self.m_journal.add_entry(l_command, l_args)

	#----------------------------------------------------------------------
	def __post_remove ( self, p_command, p_journal_entry ):
	#----------------------------------------------------------------------

		l_args = p_journal_entry.get_args()

		if not self.m_cache.remove_entry(l_args[0]):
			logging.error("Can't update cache entry: " + l_args[0])

			p_journal_entry.unlock()
			return False

		return True

	#----------------------------------------------------------------------
	def rename_file ( self, p_old_path, p_new_path ):
	#----------------------------------------------------------------------

		l_old_path = os.path.abspath(p_old_path)
		l_new_path = os.path.abspath(p_new_path)

		if not l_old_path.startswith(self.m_master_path):
			logging.error("File isn't inside project root: " + l_old_path)
			return False

		if not l_new_path.startswith(self.m_master_path):
			logging.error("File isn't inside project root: " + l_new_path)
			return False

		if not os.path.exists(l_old_path):
			logging.error("File doesn't exists: ", l_old_path)
			return False

		if os.path.exists(l_new_path):
			logging.error("File already exists: ", l_new_path)
			return False

		l_old_path = self.__master_path(l_old_path)
		l_new_path = self.__master_path(l_new_path)

		if not self.m_cache.rename_entry(l_old_path, l_new_path, p_simulate=True):
			return False

		try:
			shutil.move(p_old_path, p_new_path)
		except:
			logging.error("Can't move: " + p_old_path + " to " + p_new_path)
			return False

		l_command = journal.CMD_RENAME
		l_args    = [l_old_path, l_new_path]

		if self.m_journal.has_entry(l_command, l_args):
			return True

		return self.m_journal.add_entry(l_command, l_args)

	#----------------------------------------------------------------------
	def __post_rename ( self, p_command, p_journal_entry ):
	#----------------------------------------------------------------------

		l_args = p_journal_entry.get_args()

		if not self.m_cache.rename_entry(l_args[0], l_args[1]):
			logging.error("Can't update cache entry: " + l_args[0])

			p_journal_entry.unlock()
			return False

		return True

	#----------------------------------------------------------------------
	def update_files ( self ):
	#----------------------------------------------------------------------

		l_outdated = self.m_cache.get_outdated_entries()

		for l_file_path in l_outdated:

			l_command = journal.CMD_UPDATE
			l_args    = [l_file_path]

			if self.m_journal.has_entry(l_command, l_args):
				continue

			if not self.m_cache.update_entry(l_file_path, p_simulate=True):
				return False

			if not self.m_journal.add_entry(l_command, l_args):
				return False

		return True

	#----------------------------------------------------------------------
	def __post_update ( self, p_command, p_journal_entry ):
	#----------------------------------------------------------------------

		l_args = p_journal_entry.get_args()

		if not self.m_cache.update_entry(l_args[0]):
			logging.error("Can't update cache entry: " + l_args[0])

			p_journal_entry.unlock()
			return False

		return True

	#----------------------------------------------------------------------
	def commit ( self ):
	#----------------------------------------------------------------------

		l_commands = master.make_project_commands(self.m_slave_path)
		self.__schedule_commands(l_commands)

		while True:

			l_entry = self.m_journal.get_next_entry()
			if l_entry == None:
				break

			l_entry.lock()

			if l_entry.get_command() == journal.CMD_ADD:
				l_commands = self.__make_add_commands(l_entry)
				self.__schedule_commands(l_commands)

			elif l_entry.get_command() == journal.CMD_REMOVE:
				l_filename = l_entry.get_args()[0]
				l_commands = master.make_remove_commands(
					l_entry.get_guid(),
					l_filename)
				self.__schedule_commands(l_commands)

			elif l_entry.get_command() == journal.CMD_RENAME:
				l_old_filename, l_new_filename = l_entry.get_args()
				l_commands = master.make_rename_commands(
					l_entry.get_guid(),
					l_old_filename,
					l_new_filename)
				self.__schedule_commands(l_commands)

			elif l_entry.get_command() == journal.CMD_UPDATE:
				l_commands = self.__make_update_commands(l_entry)
				self.__schedule_commands(l_commands)

	#----------------------------------------------------------------------
	def __make_add_commands ( self, p_journal_entry ):
	#----------------------------------------------------------------------

		l_guid     = p_journal_entry.get_guid()
		l_filename = p_journal_entry.get_args()[0]
		l_filepath = os.path.join(self.m_master_path, l_filename)

		try:
			l_handle = open(l_filepath, 'rb')
			l_data   = l_handle.read()
			l_handle.close()
		except:
			p_journal_entry.unlock()
			logging.error("Can't find file: " + l_filename)
			return []

		return master.make_add_commands(l_guid, l_filename, l_data)

	#----------------------------------------------------------------------
	def __make_update_commands ( self, p_journal_entry ):
	#----------------------------------------------------------------------

		l_guid     = p_journal_entry.get_guid()
		l_filename = p_journal_entry.get_args()[0]
		l_diff     = self.m_cache.get_entry_diff(l_filename)

		if l_diff == None:
			p_journal_entry.unlock()
			logging.error("Can't get diffs: " + l_filename)
			return []

		return master.make_update_commands(l_guid, l_filename, l_diff)

	#----------------------------------------------------------------------
	def __schedule_commands ( self, p_commands ):
	#----------------------------------------------------------------------

		l_queue = queue.Queue.get_instance()

		l_callbacks = {
			'running' : self.__running_cb,
			'aborted' : self.__aborted_cb,
			'timeout' : self.__timeout_cb,
			'finished': self.__finished_cb
		}

		for l_command in p_commands:
			l_command.set_callbacks(l_callbacks)
			l_queue.append(l_command)

	#----------------------------------------------------------------------
	def __running_cb  ( self, p_command ):
	#----------------------------------------------------------------------

		l_string = self.__command_string(p_command)

		if l_string:
			logging.message("Running command: " + l_string)

	#----------------------------------------------------------------------
	def __aborted_cb  ( self, p_command ):
	#----------------------------------------------------------------------

		l_string = self.__command_string(p_command)

		if l_string:
			logging.message("Aborting command: " + l_string)

		l_journal_entry = self.__journal_entry(p_command)

		if l_journal_entry:
			l_journal_entry.unlock()

	#----------------------------------------------------------------------
	def __timeout_cb  ( self, p_command ):
	#----------------------------------------------------------------------

		l_string = self.__command_string(p_command)

		if l_string:
			logging.message("Command timeout: " + l_string)

		l_journal_entry = self.__journal_entry(p_command)

		if l_journal_entry:
			l_journal_entry.unlock()

		else:
			logging.message("Retrying...")
			p_command.cleanup()
			return command_queue.CommandQueue.get_instance().insert(p_command)

		return False

	#----------------------------------------------------------------------
	def __finished_cb ( self, p_command ):
	#----------------------------------------------------------------------

		if not p_command.has_result():
			logging.error("Command has no result")
			return False

		if p_command.get_result().is_error():
			return self.__post_error(p_command)

		l_journal_entry = self.__journal_entry(p_command)

		if l_journal_entry:
			l_command = l_journal_entry.get_command()

			if l_command == journal.CMD_ADD:
				if not self.__post_add(p_command, l_journal_entry):
					return False

			elif l_command == journal.CMD_REMOVE:
				if not self.__post_remove(p_command, l_journal_entry):
					return False

			elif l_command == journal.CMD_RENAME:
				if not self.__post_rename(p_command, l_journal_entry):
					return False

			elif l_command == journal.CMD_UPDATE:
				if not self.__post_update(p_command, l_journal_entry):
					return False

			l_guid = l_journal_entry.get_guid()
			if not self.m_journal.remove_entry(l_guid):
				logging.error("Can't remove entry from journal: " + l_guid)
				return False

		return True

	#----------------------------------------------------------------------
	def __post_error ( self, p_command ):
	#----------------------------------------------------------------------

		l_string = self.__command_string(p_command)

		if l_string:
			logging.message("Command failed: " + l_string)

		l_string = self.__result_string(p_command.get_result())

		if l_string:
			logging.message('\t' + l_string)

		l_journal_entry = self.__journal_entry(p_command)

		if l_journal_entry:
			l_journal_entry.unlock()

		else:
			logging.message("Retrying...")
			p_command.cleanup()
			return command_queue.CommandQueue.get_instance().insert(p_command)

		return False

	#----------------------------------------------------------------------
	def __journal_entry ( self, p_command ):
	#----------------------------------------------------------------------

		if p_command.has_guid():
			l_guid = p_command.get_guid()
			l_journal_entry = self.m_journal.get_entry(l_guid)

			if not l_journal_entry:
				logging.error("No journal entry: " + l_guid)

			return l_journal_entry

		return None

	#----------------------------------------------------------------------
	def __command_string ( self, p_command ):
	#----------------------------------------------------------------------

		l_string = ''

		l_name = p_command.get_name()
		l_args = p_command.get_args_readable()

		if l_name != None and l_args != None:
			l_string += l_name + '(' + l_args + ')'

		l_journal_entry = self.__journal_entry(p_command)

		if l_journal_entry:
			l_command = l_journal_entry.get_command()
			l_args    = l_journal_entry.get_args()
			l_string += os.linesep + '[' + ' '.join([l_command] + l_args) + ']'

		return l_string

	#----------------------------------------------------------------------
	def __result_string ( self, p_result ):
	#----------------------------------------------------------------------

		l_string = ''

		l_name = p_result.get_name()
		l_args = p_result.get_args_readable()

		if l_name != None and l_args != None:
			l_string = l_name + ': ' + l_args

		return l_string

	#----------------------------------------------------------------------
	def __master_path ( self, p_file_path ):
	#----------------------------------------------------------------------

		l_start = os.path.commonprefix([self.m_master_path, p_file_path])
		l_path  = p_file_path[len(l_start):]
		return l_path


#==========================================================================
# End
#==========================================================================
