#==========================================================================
# tostdk :: tostlib :: cache.py
# Project cache manager
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
import time
import hashlib

import logging
import configuration


#==========================================================================
class JournalEntry:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_guid, p_command, p_args ):
	#----------------------------------------------------------------------

		self.m_guid    = p_guid
		self.m_command = p_command
		self.m_args    = p_args

	#----------------------------------------------------------------------
	def get_guid    ( self ): return self.m_guid
	def get_command ( self ): return self.m_command
	def get_args    ( self ): return self.m_args
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	@classmethod
	def from_string ( cls, p_string ):
	#----------------------------------------------------------------------

		l_split = p_string.strip().split('\t')

		if len(l_split) != 3:
			return None

		l_guid    = l_split[0].strip()
		l_command = l_split[1].strip()
		l_args    = l_split[2].strip().split(os.pathsep)

		return cls(l_guid, l_command, l_args)

	#----------------------------------------------------------------------
	def to_string ( self ):
	#----------------------------------------------------------------------

		l_args   = os.pathsep.join(self.m_args)
		l_string = '\t'.join((self.m_guid, self.m_command, l_args)) + '\n'

		return l_string


#==========================================================================
class Journal:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_project_path ):
	#----------------------------------------------------------------------

		self.m_project_path = p_project_path
		self.m_entries      = []

		self.m_hash = hashlib.md5()

		if not self.__load_journal():
			logging.error("Can't initialize journal")

	#----------------------------------------------------------------------
	def add_entry ( self, p_command, p_args ):
	#----------------------------------------------------------------------

		l_guid  = self.__guid(p_command, p_args)
		l_entry = JournalEntry(l_guid, p_command, p_args)

		self.m_entries.append(l_entry)
		return True

	#----------------------------------------------------------------------
	def remove_entry ( self, p_guid ):
	#----------------------------------------------------------------------

		for l_entry in self.m_entries:
			if l_entry.get_guid() == p_guid:
				self.m_entries.remove(l_entry)
				return True

		logging.error("Invalid guid: ", p_guid)
		return False

	#----------------------------------------------------------------------
	def get_top_entry ( self ):
	#----------------------------------------------------------------------

		if self.m_entries:
			return self.m_entries[0]

		return None

	#----------------------------------------------------------------------
	def __guid ( self, p_command, p_args ):
	#----------------------------------------------------------------------

		l_string = time.asctime() + p_command + ''.join(p_args)
		self.m_hash.update(l_string)
		return self.m_hash.hexdigest()

	#----------------------------------------------------------------------
	def __load_journal ( self ):
	#----------------------------------------------------------------------

		l_db_path = os.path.join(self.m_project_path, 'journal')

		self.m_entries = []

		if not os.path.exists(l_db_path):
			if os.path.exists(self.m_project_path):
				return True
			logging.error("No project found: " + self.m_project_path)
			return False

		try:
			l_handle = open(l_db_path, 'rU')
		except:
			logging.error("Can't open: " + l_db_path)
			return False

		for l_line in l_handle:
			l_entry = JournalEntry.from_string(l_line)

			if l_entry == None:
				logging.error("Invalid cache entry: " + l_line.strip())
				return False

			self.m_entries.append(l_entry)

		l_handle.close()
		return True

	#----------------------------------------------------------------------
	def __save_journal ( self ):
	#----------------------------------------------------------------------

		l_db_path = os.path.join(self.m_project_path, 'journal')

		l_lines = ''

		for l_entry in self.m_entries:
			l_lines += l_entry.to_string()

		try:
			l_handle = open(l_db_path, 'wb')
			l_handle.write(l_lines)
			l_handle.close()
		except:
			logging.error("Can't write: " + l_db_path)
			return False

		return True


#==========================================================================
# End
#==========================================================================
