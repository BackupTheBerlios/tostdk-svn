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
import shutil
import hashlib
import difflib

import logging


#==========================================================================
CACHE_VERSION = 1
#==========================================================================


#==========================================================================
class CacheEntry:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_id, p_path, p_md5):
	#----------------------------------------------------------------------

		self.m_id   = p_id
		self.m_path = p_path
		self.m_md5  = p_md5

	#----------------------------------------------------------------------
	def get_id   ( self ): return self.m_id
	def get_path ( self ): return self.m_path
	def get_md5  ( self ): return self.m_md5
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def set_md5 ( self, p_md5 ): self.m_md5 = p_md5
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	@classmethod
	def from_string_1 ( cls, p_string ):
	#----------------------------------------------------------------------

		l_split = p_string.split(os.pathsep)

		if len(l_split) != 3:
			return None

		l_id   = l_split[0].strip()
		l_path = l_split[1].strip()
		l_md5  = l_split[2].strip()

		return cls(l_id, l_path, l_md5)

	#----------------------------------------------------------------------
	def to_string ( self ):
	#----------------------------------------------------------------------

		return os.pathsep.join((self.m_id, self.m_path, self.m_md5)) + os.linesep


#==========================================================================
class Cache:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_master_path, p_cache_path ):
	#----------------------------------------------------------------------

		self.m_master_path = p_master_path
		self.m_cache_path  = p_cache_path
		self.m_entries     = {}

		if not self.__load_db():
			logging.error("Can't initialize cache")

	#----------------------------------------------------------------------
	def entries_iterator ( self ):
	#----------------------------------------------------------------------

		return self.m_entries.itervalues()

	#----------------------------------------------------------------------
	def has_entry ( self, p_file_path ):
	#----------------------------------------------------------------------

		return self.m_entries.has_key(p_file_path.lower())

	#----------------------------------------------------------------------
	def get_entry ( self, p_file_path ):
	#----------------------------------------------------------------------

		l_key = p_file_path.lower()

		if not self.m_entries.has_key(l_key):
			return None

		return self.m_entries[l_key]

	#----------------------------------------------------------------------
	def __store_entry ( self, p_entry ):
	#----------------------------------------------------------------------

		self.m_entries[p_entry.get_path().lower()] = p_entry

	#----------------------------------------------------------------------
	def __del_entry ( self, p_file_path ):
	#----------------------------------------------------------------------

		l_key = p_file_path.lower()

		if self.m_entries.has_key(l_key):
			del self.m_entries[l_key]

	#----------------------------------------------------------------------
	def add_entry ( self, p_file_path, p_simulate = False ):
	#----------------------------------------------------------------------

		if self.has_entry(p_file_path):
			logging.warning("Already in cache: " + p_file_path)
			return False

		if not self.__save_db():
			return False

		l_file_path = os.path.join(self.m_master_path, p_file_path)

		if not os.path.exists(l_file_path):
			logging.error("Can't find file: " + l_file_path)
			return False

		if p_simulate:
			return True

		l_id  = self.__id(p_file_path)
		l_md5 = self.__md5(p_file_path)

		if l_md5 == None:
			return False

		l_cache_path = self.__cache_path(p_file_path)

		try:
			shutil.copy(l_file_path, l_cache_path)
		except:
			logging.error("Can't copy: " + l_file_path + " to " + l_cache_path)
			return False

		l_entry = CacheEntry(l_id, p_file_path, l_md5)
		self.__store_entry(l_entry)

		return self.__save_db()

	#----------------------------------------------------------------------
	def remove_entry ( self, p_file_path, p_force = False, p_simulate = False ):
	#----------------------------------------------------------------------

		if not self.has_entry(p_file_path):
			logging.warning("Not in cache: " + p_file_path)
			return False

		if not self.__save_db():
			return False

		if p_simulate:
			return True

		l_cache_path = self.__cache_path(p_file_path)

		try:
			os.remove(l_cache_path)
		except:
			logging.error("Can't delete file: " + l_cache_path)
			if not p_force:
				return False

		self.__del_entry(p_file_path)

		return self.__save_db()

	#----------------------------------------------------------------------
	def rename_entry ( self, p_old_path, p_new_path, p_simulate = False ):
	#----------------------------------------------------------------------

		if not self.has_entry(p_old_path):
			logging.error("Not in cache: " + p_old_path)
			return False

		if self.has_entry(p_new_path):
			logging.error("Already in cache: " + p_new_path)
			return False

		if not self.__save_db():
			return False

		if p_simulate:
			return True

		l_id  = self.__id(p_new_path)
		l_md5 = self.get_entry(p_old_path).get_md5()

		l_old_cache_path = self.__cache_path(p_old_path)
		l_new_cache_path = os.path.join(self.m_cache_path, l_id)

		try:
			shutil.move(l_old_cache_path, l_new_cache_path)
		except:
			logging.error("Can't move: " + l_old_cache_path + " to " + l_new_cache_path)
			return False

		self.__del_entry(p_old_path)

		l_new_entry = CacheEntry(l_id, p_new_path, l_md5)
		self.__store_entry(l_new_entry)

		return self.__save_db()

	#----------------------------------------------------------------------
	def update_entry ( self, p_file_path, p_simulate = False ):
	#----------------------------------------------------------------------

		if not self.has_entry(p_file_path):
			logging.warning("Not in cache: " + p_file_path)
			return False

		if not self.__save_db():
			return False

		l_file_path = os.path.join(self.m_master_path, p_file_path)

		if not os.path.exists(l_file_path):
			logging.error("Can't find file: " + l_file_path)
			return False

		l_md5 = self.__md5(p_file_path)

		if l_md5 == None:
			return False

		if p_simulate:
			return True

		l_cache_path = self.__cache_path(p_file_path)

		try:
			shutil.copy(l_file_path, l_cache_path)
		except:
			logging.error("Can't copy: " + l_file_path + " to " + l_cache_path)
			return False

		self.get_entry(p_file_path).set_md5(l_md5)

		return self.__save_db()

	#----------------------------------------------------------------------
	def is_entry_uptodate ( self, p_file_path ):
	#----------------------------------------------------------------------

		if not self.has_entry(p_file_path):
			logging.error("Not in cache: " + p_file_path)
			return None

		l_file_path = os.path.join(self.m_master_path, p_file_path)
		if not os.path.exists(l_file_path):
			logging.error("Can't find file: " + l_file_path)
			return None

		l_cache_md5 = self.get_entry(p_file_path).get_md5()
		l_file_md5  = self.__md5(p_file_path)

		if l_file_md5 == None:
			return None

		return (l_cache_md5 == l_file_md5)

	#----------------------------------------------------------------------
	def get_outdated_entries ( self ):
	#----------------------------------------------------------------------

		l_list = []

		for l_entry in self.m_entries.itervalues():

			if not self.is_entry_uptodate(l_entry.get_path()):
				l_list.append(l_file_path)

		return l_list

	#----------------------------------------------------------------------
	def get_entry_diff ( self, p_file_path ):
	#----------------------------------------------------------------------

		if not self.has_entry(p_file_path):
			logging.error("Not in cache: " + p_file_path)
			return None

		l_cache_path = self.__cache_path(p_file_path)

		try:
			l_handle = open(l_cache_path, 'rb')
			l_cache_data = l_handle.read()
			l_handle.close()
		except:
			logging.error("Can't read file: " + l_cache_path)
			return None

		l_file_path  = os.path.join(self.m_master_path, p_file_path)

		try:
			l_handle = open(l_file_path, 'rb')
			l_file_data = l_handle.read()
			l_handle.close()
		except:
			logging.error("Can't read file: " + l_file_path)
			return None

		l_matcher = difflib.SequenceMatcher(None, l_cache_data, l_file_data)
		l_orig_size  = len(l_cache_data)
		l_final_size = len(l_file_data)

		return (l_orig_size, l_final_size, l_matcher.get_opcodes())

	#----------------------------------------------------------------------
	def __cache_path ( self, p_file_path ):
	#----------------------------------------------------------------------

		if not self.has_entry(p_file_path):
			return None

		l_id = self.get_entry(p_file_path).get_id()

		return os.path.join(self.m_cache_path, l_id)

	#----------------------------------------------------------------------
	def __load_db ( self ):
	#----------------------------------------------------------------------

		l_db_path = os.path.join(self.m_cache_path, 'cache')

		self.m_entries = {}

		if not os.path.exists(l_db_path):
			if os.path.exists(self.m_cache_path):
				return True
			logging.error("No cache found: " + self.m_cache_path)
			return False

		try:
			l_handle = open(l_db_path, 'rU')
		except:
			logging.error("Can't open: " + l_db_path)
			return False

		try:
			l_version = int(l_handle.readline().strip())
		except:
			logging.error("Can't read cache version tag: " + self.m_cache_path)
			return False

		if l_version == 1:
			l_result = self.__load_db_1(l_handle)

		else:
			logging.error("Unsupported cache version: " + self.m_cache_path)
			l_result = False

		l_handle.close()
		return l_result

	#----------------------------------------------------------------------
	def __load_db_1 ( self, p_handle ):
	#----------------------------------------------------------------------

		for l_line in p_handle:
			l_entry = CacheEntry.from_string_1(l_line)

			if l_entry == None:
				logging.error("Invalid cache entry: " + l_line.strip())
				return False

			self.m_entries[l_entry.get_path().lower()] = l_entry

		return True

	#----------------------------------------------------------------------
	def __save_db ( self ):
	#----------------------------------------------------------------------

		l_db_path = os.path.join(self.m_cache_path, 'cache')

		l_lines = str(CACHE_VERSION) + os.linesep

		for l_entry in self.m_entries.itervalues():
			l_lines += l_entry.to_string()

		try:
			l_handle = open(l_db_path, 'wb')
			l_handle.write(l_lines)
			l_handle.close()
		except:
			logging.error("Can't write: " + l_db_path)
			return False

		return True

	#----------------------------------------------------------------------
	def __id ( self, p_file_path ):
	#----------------------------------------------------------------------

		l_md5 = hashlib.md5()
		l_md5.update(p_file_path.lower())

		return lmd5.hexdigest()

	#----------------------------------------------------------------------
	def __md5 ( self, p_file_path ):
	#----------------------------------------------------------------------

		l_file_path = os.path.join(self.m_master_path, p_file_path)

		try:
			l_handle = open(l_file_path, 'rb')
		except:
			logging.error("Can't open: " + l_file_path)
			return None

		l_md5 = hashlib.md5()

		while True:

			l_data = l_handle.read(4096)
			l_md5.update(l_data)

			if len(l_data) < 4096:
				break

		l_handle.close()
		return l_md5.hexdigest()


#==========================================================================
# End
#==========================================================================
